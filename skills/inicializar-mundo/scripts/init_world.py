#!/usr/bin/env python3
"""Inicializa una bóveda de Obsidian para worldbuilding a partir de las respuestas de la
entrevista. Idempotente: solo crea lo que falta y nunca sobrescribe."""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
UNDEFINED = "Por definir."
NOT_APPLICABLE = "No aplica."
EMPTY_VALUES = {"", "por definir", "por_definir", "pendiente", "-"}
DECIDE_VALUES = {"decide", "decide tu", "decide tú"}

created, skipped, warnings = [], [], []

# Bitácora: la crónica del mundo para su autor. Es la misma nota que escriben después los scripts de
# crear-entidad (report.py --log, log_entry.py): mismo encabezado y misma marca para las entradas nuevas
CHRONICLE_MARKER = "<!-- Las entradas nuevas se añaden debajo de esta línea -->"
CHRONICLE_HEADER = f"""---
tipo: meta
---

# Bitácora

Cómo ha ido creciendo el mundo: qué se creó y qué cambió en cada tarea, de lo más reciente a lo más antiguo. La escriben las skills al terminar (`report.py --log`, `log_entry.py`); lo que se cambia a mano en Obsidian no queda aquí.
- Las notas creadas van enlazadas; los enlaces pendientes, como texto.
- El detalle técnico de cada ciclo del motor está en el Registro de Generación.

{CHRONICLE_MARKER}
"""


def write_file(path, content):
    """Escribe solo si el archivo no existe."""
    if path.exists():
        skipped.append(path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    created.append(path)


def ensure_dir(path):
    if not path.exists():
        path.mkdir(parents=True)
        created.append(path)


def title_from_name(name):
    return re.sub(r"^\d+_", "", name).replace("_", " ")


def display_title(node):
    """Título visible: el campo 'titulo' (con tildes) o el derivado del nombre de la carpeta."""
    return node.get("titulo") or title_from_name(node["nombre"])


def moc_name(name):
    return "MOC_" + re.sub(r"^\d+_", "", name)


def fill_placeholders(text, placeholders, source):
    for key, value in placeholders.items():
        text = text.replace("{{" + key + "}}", value)
    for leftover in sorted(set(re.findall(r"\{\{(\w+)\}\}", text))):
        warnings.append(f"{source}: placeholder sin valor {{{{{leftover}}}}}")
    return text


def load_asset(name):
    return json.loads((ASSETS / name).read_text(encoding="utf-8"))


# --- Respuestas -------------------------------------------------------------

def is_empty(value):
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().rstrip(".").lower() in EMPTY_VALUES
    if isinstance(value, list):
        return all(is_empty(v) for v in value)
    if isinstance(value, dict):
        return is_empty(value.get("texto"))
    return False


def applies(question, answers):
    condition = question.get("condicion")
    if not condition:
        return True
    value = answers.get(condition["pregunta"])
    return condition["incluye"] in (value if isinstance(value, list) else [value])


def with_value(template, value):
    return template.replace("{valor}", value.rstrip(". ")) if template else None


def interpret_value(question, value):
    """Devuelve (texto legible, valor para frontmatter, regla) de un único valor."""
    template = question.get("regla")
    if isinstance(value, dict):  # respuesta libre ("Other") en una pregunta de opciones
        text = str(value["texto"]).strip()
        rule = value.get("regla") or with_value(template, text)
        if not rule and question.get("opciones"):
            warnings.append(f"'{question['id']}': respuesta propia sin regla; añade 'regla' en respuestas.json")
        return text, text, rule
    if str(value).strip().lower() in DECIDE_VALUES:
        warnings.append(f"'{question['id']}': quedó como 'decide tú' sin resolver; Claude debe elegir un valor concreto")
        return str(value), str(value), None
    if question["formato"] == "texto":
        text = str(value).strip()
        if question.get("numerico"):
            # Las respuestas numéricas (como el año actual) van como número en el frontmatter
            number = text.lstrip("-").isdigit() and int(text)
            if number is False:
                warnings.append(f"'{question['id']}': se esperaba un número y llegó '{text}'")
                return text, text, with_value(template, text)
            return text, number, with_value(template, text)
        return text, text, with_value(template, text)
    option = next((o for o in question.get("opciones", []) if o["valor"] == value), None)
    if option is None:
        warnings.append(f"'{question['id']}': valor no reconocido '{value}', se usa como texto libre")
        return str(value), str(value), with_value(template, str(value))
    text = f"{option['etiqueta']} — {option['descripcion']}"
    return text, option["valor"], option.get("regla") or with_value(template, option["etiqueta"])


def interpret_answer(question, value):
    """Devuelve {texto, fm, reglas} o None si la pregunta quedó por definir."""
    if is_empty(value):
        if "defecto" not in question:
            return None
        value = question["defecto"]
    values = value if isinstance(value, list) else [value]
    parts = [interpret_value(question, v) for v in values if not is_empty(v)]
    if question["formato"] == "multiple":
        text = ", ".join(t.split(" — ")[0] for t, _, _ in parts)
        frontmatter_value = [f for _, f, _ in parts]
    else:
        text, frontmatter_value = parts[0][0], parts[0][1]
    return {"texto": text, "fm": frontmatter_value, "reglas": [r for _, _, r in parts if r]}


def validate_questionnaire(questionnaire):
    """Avisa si el cuestionario no cabe en AskUserQuestion (4 preguntas, 4 opciones, header de 12)
    o si una pregunta que admite «Decide tú» no le deja sitio."""
    modes = {r["id"]: r["modo"] for r in questionnaire["rondas"]}
    by_round = {}
    for q in questionnaire["preguntas"]:
        by_round.setdefault(q["ronda"], []).append(q["id"])
        if len(q.get("opciones", [])) > 4:
            warnings.append(f"cuestionario: '{q['id']}' tiene más de 4 opciones")
        if len(q.get("encabezado", "")) > 12:
            warnings.append(f"cuestionario: el encabezado de '{q['id']}' supera 12 caracteres")
        if q["formato"] in ("opcion", "multiple") and q.get("permite_decidir", True) and len(q.get("opciones", [])) > 3:
            warnings.append(f"cuestionario: '{q['id']}' tiene más de 3 opciones y no deja sitio para «Decide tú»")
    for round_id, ids in by_round.items():
        if modes.get(round_id) == "opciones" and len(ids) > 4:
            warnings.append(f"cuestionario: la ronda {round_id} tiene más de 4 preguntas de opciones")


# --- Generadores ------------------------------------------------------------

def build_readme(node, is_section):
    lines = [f"# {display_title(node)}", "", node["desc"], ""]
    if node.get("va"):
        lines += ["## Qué va aquí", node["va"], ""]
    if node.get("no_va"):
        lines += ["## Qué no va aquí", node["no_va"], ""]
    if node.get("hijos"):
        lines += ["## Contenido"]
        lines += [f"- **{display_title(child)}**: {child['desc']}" for child in node["hijos"]]
        lines.append("")
    if node.get("nota"):
        lines += ["## Nota", node["nota"], ""]
    if is_section:
        index = "MOC_Inicio" if node["nombre"].startswith("00_") else moc_name(node["nombre"])
        lines += ["## Índice", f"Índice automático de la sección: [[{index}]].", ""]
    lines += ["## Convenciones",
              "Sigue las guías de `00_Sistema/04_Convenciones/`; si existe una plantilla del tipo en "
              "`00_Sistema/01_Plantillas/`, úsala.", ""]
    return "\n".join(lines)


def create_node(node, parent, is_section=False):
    folder = parent / node["nombre"]
    ensure_dir(folder)
    write_file(folder / "README.md", build_readme(node, is_section))
    for child in node.get("hijos", []):
        create_node(child, folder)


def base_block(filters, view_name, columns):
    # Bloque de Obsidian Bases: tabla agrupada por carpeta
    lines = ["```base", "filters:", "  and:"]
    lines += ["    " + f for f in filters]
    lines += ["views:", "  - type: table", f"    name: {view_name}",
              "    groupBy:", "      property: file.folder", "      direction: ASC", "    order:"]
    lines += [f"      - {c}" for c in columns]
    lines.append("```")
    return lines


NOTES_ONLY = ['- file.ext == "md"',
              "- not:", '    - file.basename == "README"',
              "- not:", '    - file.basename.startsWith("MOC_")']


def section_moc(section):
    lines = ["---", "tipo: moc", "---", "", f"# {display_title(section)}", "", section["desc"], "",
             "Volver a [[MOC_Inicio]].", "", "## Notas"]
    lines += base_block([f'- file.inFolder("{section["nombre"]}")'] + NOTES_ONLY, "Notas",
                        ["file.name", "note.tipo", "note.estado", "note.ultima_revision"])
    lines.append("")
    if section.get("hijos"):
        lines += ["## Subcarpetas"]
        lines += [f"- **{display_title(child)}**: {child['desc']}" for child in section["hijos"]]
        lines.append("")
    return "\n".join(lines)


def home_moc(world, sections, results):
    lines = ["---", "tipo: moc", "---", "", f"# {world} — Inicio", ""]
    if results.get("premisa"):
        lines += [f"> {results['premisa']['texto']}", ""]
    lines += ["## El mundo",
              "- [[Ficha_del_Mundo]] — identidad y pilares (fuente de verdad).",
              "- [[Preguntas_Abiertas]] — decisiones pendientes.",
              "- [[Bitacora|Bitácora]] — cómo ha ido creciendo el mundo: qué se creó y cuándo.", "",
              "## Secciones"]
    lines += [f"- [[{moc_name(s['nombre'])}]] — {s['desc']}"
              for s in sections if not s["nombre"].startswith("00_")]
    lines += ["", "## Borradores pendientes de revisión"]
    lines += base_block(['- file.ext == "md"', '- note.estado == "borrador"',
                         "- not:", '    - file.inFolder("00_Sistema")'],
                        "Borradores", ["file.name", "note.tipo", "note.ultima_revision"])
    lines += ["", "## Convenciones",
              "- [[Guia_de_Organizacion]] — dónde va cada cosa, frontmatter y tipos registrados.",
              "- [[Guia_de_Nombres]] — nombres de archivo y del mundo.",
              "- [[Guia_de_Canon]] — estados, verdad y creencia.",
              "- [[Guia_de_Estilo_y_Tono]] — género, tono, voz y formato.",
              "- [[Glosario]] — términos del mundo.",
              "- [[Registro_de_Canon]] — historial de decisiones.", ""]
    return "\n".join(lines)


def world_sheet(world, questionnaire, results, today):
    lines = ["---", "tipo: ficha_mundo", "estado: canon", f"mundo: {json.dumps(world, ensure_ascii=False)}"]
    for q in questionnaire["preguntas"]:
        if q["id"] not in results or (q["formato"] == "texto" and not q.get("en_frontmatter")):
            continue
        result = results[q["id"]]
        lines.append(f"{q['id']}: {json.dumps(result['fm'] if result else 'por_definir', ensure_ascii=False)}")
    lines += [f"ultima_revision: {today}", "---", "", f"# {world} — Ficha del Mundo", ""]
    premise = results.get("premisa")
    lines += [f"> {premise['texto'] if premise else 'Premisa por definir.'}", "",
              "Fuente de verdad de la identidad y los pilares del mundo; Claude la carga siempre en su "
              "contexto. Para cambiar un pilar, edítalo aquí, actualiza las reglas de contenido de "
              "`CLAUDE.md` y deja constancia en [[Registro_de_Canon]].", ""]
    for section in questionnaire["secciones_ficha"]:
        lines.append(f"## {section}")
        for q in questionnaire["preguntas"]:
            if q.get("seccion") == section and q["id"] in results:
                result = results[q["id"]]
                lines.append(f"- **{q['titulo']}:** {result['texto'] if result else UNDEFINED}")
        lines.append("")
    return "\n".join(lines)


def setup_graph(vault, warnings):
    """El grafo de Obsidian, con el script de crear-entidad: un color por tipo de entidad, un filtro sin las
    notas del sistema, los nombres visibles desde más lejos y los marcadores «Grafo completo» y
    «Grafo sin secretos». Devuelve las líneas del resumen; si crear-entidad no está, avisa."""
    scripts = Path(__file__).resolve().parents[2] / "crear-entidad" / "scripts"
    if not (scripts / "graph_colors.py").is_file():
        warnings.append("no encuentro la skill crear-entidad: el grafo de Obsidian queda sin colores por tipo "
                        "(ejecuta su graph_colors.py cuando esté)")
        return []
    sys.path.insert(0, str(scripts))
    from graph_colors import configure_graph
    return configure_graph(vault)


def add_chronicle_entry(path, title, lines, today):
    """Añade la entrada arriba de la Bitácora (la crea si no existe). No sobrescribe nada: solo inserta."""
    text = path.read_text(encoding="utf-8") if path.exists() else CHRONICLE_HEADER
    rows = text.splitlines()
    at = next((i + 1 for i, line in enumerate(rows) if line.strip() == CHRONICLE_MARKER), len(rows))
    while at < len(rows) and not rows[at].strip():
        at += 1
    rows[at:at] = [f"## {today} · {title}", *lines, ""]
    marker = next((i for i, line in enumerate(rows) if line.strip() == CHRONICLE_MARKER), None)
    if marker is not None and marker + 1 < len(rows) and rows[marker + 1].strip():
        rows.insert(marker + 1, "")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(rows).rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def open_questions(undefined):
    lines = ["---", "tipo: meta", "---", "", "# Preguntas Abiertas", "",
             "Decisiones pendientes sobre el mundo. Claude anota aquí los huecos importantes en lugar de "
             "inventar la respuesta. Marca `[x]` al resolver una y enlaza la nota donde quedó decidida.", "",
             "## Pilares por definir (inicialización)"]
    lines += [f"- [ ] {t}" for t in undefined] or ["Ninguno."]
    lines += ["", "## Otras preguntas", "<!-- Añade aquí nuevas preguntas como: - [ ] ¿...? -->", ""]
    return "\n".join(lines)


# --- Principal --------------------------------------------------------------

def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answers", required=True, help="JSON con las respuestas de la entrevista")
    parser.add_argument("--root", default=".", help="Raíz del proyecto (donde va CLAUDE.md)")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda, relativa a la raíz")
    parser.add_argument("--verbose", action="store_true", help="Lista cada archivo creado u omitido")
    args = parser.parse_args()

    payload = json.loads(Path(args.answers).read_text(encoding="utf-8"))
    world = str(payload.get("nombre") or "").strip()
    if not world:
        sys.exit("Error: falta 'nombre' en las respuestas.")
    answers = payload.get("respuestas", {})

    questionnaire = load_asset("cuestionario.json")
    validate_questionnaire(questionnaire)
    questions = [q for q in questionnaire["preguntas"] if q["id"] != "nombre"]
    ids = {q["id"] for q in questions}
    warnings.extend(f"Respuesta desconocida ignorada: '{key}'" for key in answers if key not in ids)

    results = {q["id"]: interpret_answer(q, answers.get(q["id"]))
               for q in questions if applies(q, answers)}
    rules = [r for q in questions if results.get(q["id"]) for r in results[q["id"]]["reglas"]]
    undefined = [q["titulo"] for q in questions if q["id"] in results and results[q["id"]] is None]

    root = Path(args.root).resolve()
    vault = root / args.vault
    sections = load_asset("estructura.json")["secciones"]
    today = datetime.date.today().isoformat()

    # Los nombres de los placeholders son los de las plantillas de assets/
    placeholders = {
        "MUNDO": world, "BOVEDA": args.vault, "FECHA": today,
        "REGLAS": "\n".join(f"- {r}" for r in rules) or "- Ninguna todavía: los pilares están por definir.",
        "POR_DEFINIR": (f"\n\n**Pilares por definir:** {', '.join(undefined)}. No los decidas tú: "
                        "pregunta o regístralos en `Preguntas_Abiertas`.") if undefined else "",
        "MAPA_SECCIONES": "\n".join(f"| `{s['nombre']}` | {s['desc']} |" for s in sections)}
    for q in questions:
        result = results.get(q["id"])
        placeholders[q["id"]] = result["texto"] if result else (UNDEFINED if q["id"] in results else NOT_APPLICABLE)

    ensure_dir(vault)
    for section in sections:
        create_node(section, vault, is_section=True)
        if not section["nombre"].startswith("00_"):
            write_file(vault / section["nombre"] / (moc_name(section["nombre"]) + ".md"), section_moc(section))

    system_dir = vault / "00_Sistema"
    write_file(system_dir / "MOC_Inicio.md", home_moc(world, sections, results))
    write_file(system_dir / "Ficha_del_Mundo.md", world_sheet(world, questionnaire, results, today))
    write_file(system_dir / "Preguntas_Abiertas.md", open_questions(undefined))
    for source in sorted((ASSETS / "convenciones").glob("*.md")):
        write_file(system_dir / "04_Convenciones" / source.name,
                   fill_placeholders(source.read_text(encoding="utf-8"), placeholders, source.name))
    write_file(root / "CLAUDE.md",
               fill_placeholders((ASSETS / "CLAUDE.md.tpl").read_text(encoding="utf-8"), placeholders, "CLAUDE.md.tpl"))
    graph = setup_graph(vault, warnings)

    files = [p for p in created if p.is_file()]
    # Bitácora: la creación del mundo es su primera entrada; si la bóveda ya existía, se anota lo que se completó
    chronicle = system_dir / "Bitacora.md"
    defined = [q["titulo"] for q in questions if results.get(q["id"])]
    if not chronicle.exists():
        lines = []
        for key, label in (("genero", "Género"), ("foco", "Foco"), ("tono", "Tono")):
            if results.get(key):
                lines.append(f"- **{label}:** {results[key]['texto']}")
        lines += [f"- **Ficha del Mundo:** [[Ficha_del_Mundo|Ficha del Mundo]], con {len(defined)} pilares definidos"
                  + (f" y {len(undefined)} por definir (en [[Preguntas_Abiertas|Preguntas Abiertas]])." if undefined
                     else "."),
                  f"- **Bóveda:** {len(files) + 1} archivos y {len(created) - len(files)} carpetas: las secciones, las guías "
                  f"de convenciones, los índices y `CLAUDE.md`, con {len(rules)} reglas de contenido."]
        add_chronicle_entry(chronicle, f"Se creó el mundo «{world}»", lines, today)
        created.append(chronicle)
        files.append(chronicle)
    elif files:
        add_chronicle_entry(chronicle, "Se completó la estructura del mundo",
                            [f"- **Bóveda:** {len(files)} archivos y {len(created) - len(files)} carpetas que faltaban."],
                            today)
    print(f"Mundo: {world}")
    print(f"Creados: {len(files)} archivos y {len(created) - len(files)} carpetas | "
          f"Ya existían (sin tocar): {len(skipped)}")
    if args.verbose:
        for path in created:
            print("  + " + str(path.relative_to(root)))
    for path in skipped if (args.verbose or len(skipped) <= 20) else []:
        print("  = " + str(path.relative_to(root)))
    print(f"Reglas de contenido: {len(rules)}")
    print("Pilares por definir: " + (", ".join(undefined) if undefined else "ninguno"))
    for line in graph:
        print(line)
    for warning in warnings:
        print("AVISO: " + warning)


if __name__ == "__main__":
    main()
