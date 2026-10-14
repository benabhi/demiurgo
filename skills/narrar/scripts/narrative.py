#!/usr/bin/env python3
"""Las narraciones del mundo (relatos, escenas, crónicas y documentos): su sitio en la bóveda, su comprobación y
su lista. No son entidades: cuentan el mundo, no lo cambian. Viven en 90_Narrativa, una subcarpeta por forma.

  prepare FORMA          Deja lista la estructura para una narración de esa forma (relato, escena, cronica o
                         documento): 90_Narrativa con su README y su índice (enlazado desde MOC_Inicio), la
                         subcarpeta de la forma, la plantilla y sus filas en la Guía de Organización. Dice en qué
                         carpeta va la narración. Solo crea lo que falta.
  check NOTA             Comprueba una narración: su frontmatter y su carpeta; que sus enlaces lleven a notas que
                         existen (nada pendiente; un secreto, solo con `usa_secretos: true`); que sus personajes
                         vivan y sus lugares existan en `cuando`; y que tenga su resumen y sus notas.
  list [--about NOTA] [--serie SERIE]
                         Las narraciones, con su forma, su momento, su serie y su resumen; con --about, las que
                         usan esa entidad; con --serie, las de una serie, en orden.

Ejemplos:  narrative.py prepare escena
           narrative.py check 90_Narrativa/Escenas/La_noche_del_cometa.md
           narrative.py list --about Puerto_Gris"""
import argparse
import os
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
# La lógica común vive en los scripts de crear-entidad
sys.path.insert(0, str(SKILL.parent / "crear-entidad" / "scripts"))
from vault_lib import (ARCHIVED_FOLDER, ATTACHMENT_RE, LINK_RE, NARRATIVE_FOLDER, NARRATIVE_TYPE,  # noqa: E402
                       SECRET_TYPE, date_keys, first, format_year, index_vault, int_value, link_value, load_calendars,
                       load_index, load_modules, normalize, parse_frontmatter, read_world, reference_calendar,
                       split_note, strip_links, unquote)
from vault_lib import vault_path  # noqa: E402

FORMS = {"relato": "Relatos", "escena": "Escenas", "cronica": "Cronicas", "documento": "Documentos"}
FORM_TEXT = {
    "relato": "Relatos: historias con principio y final.",
    "escena": "Escenas: un momento, sin una trama completa.",
    "cronica": "Crónicas: hechos contados con la voz de un cronista del mundo.",
    "documento": "Documentos: escritos del mundo, como cartas, diarios, informes, sermones o canciones.",
}
STATES = ("borrador", "terminada")
GUIDE = "00_Sistema/04_Convenciones/Guia_de_Organizacion.md"
HOME = "00_Sistema/MOC_Inicio.md"
TEMPLATE = "00_Sistema/01_Plantillas/Plantilla_Narracion.md"
MOC = "MOC_Narrativa"
HOME_LINE = f"- [[{MOC}]] — Relatos, escenas, crónicas y documentos ambientados en el mundo."
SUMMARY_CHARS = 140

ROOT_README = f"""# Narrativa

Relatos, escenas, crónicas y documentos ambientados en el mundo, escritos con `/narrar`. No son entidades: cuentan el mundo, no lo cambian. Sus enlaces solo van a lo que ya tiene nota, y lo que inventan se queda en ellas.

## Qué va aquí
Una subcarpeta por forma, que se crea la primera vez que se usa:
- **Relatos:** historias con principio y final.
- **Escenas:** un momento, sin una trama completa.
- **Crónicas:** hechos contados con la voz de un cronista del mundo.
- **Documentos:** escritos del mundo, como cartas, diarios, informes, sermones o canciones.

## Qué no va aquí
Las obras que existen dentro del mundo (un libro, un cantar o una crónica que sus personajes conocen) son entidades de tipo `obra`. Una narración puede citarlas o atribuirse a ellas.

## Índice
Índice automático de la sección: [[{MOC}]].
"""

MOC_TEXT = f"""---
tipo: moc
---

# Narrativa

Relatos, escenas, crónicas y documentos ambientados en el mundo. No son entidades: cuentan el mundo, no lo cambian.

Volver a [[MOC_Inicio]].

## Narraciones
```base
filters:
  and:
    - file.inFolder("{NARRATIVE_FOLDER}")
    - file.ext == "md"
    - not:
        - file.basename == "README"
    - not:
        - file.basename.startsWith("MOC_")
views:
  - type: table
    name: Narraciones
    groupBy:
      property: note.forma
      direction: ASC
    order:
      - file.name
      - note.momento
      - note.serie
      - note.estado
      - note.ultima_revision
```
"""


def write_new(path, text, created):
    """Escribe solo si no existe."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        created.append(path)


def add_row(text, heading, row):
    """La tabla bajo `## heading`, con `row` al final si su primera celda no está ya. Devuelve (texto, si cambió)."""
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == f"## {heading}"), None)
    if start is None:
        return text, False
    rows, i = [], start + 1
    while i < len(lines) and not lines[i].startswith("## "):
        if lines[i].strip().startswith("|"):
            rows.append(i)
        i += 1
    key = row.split("|")[1].strip().strip("`")
    if not rows or any(lines[j].split("|")[1].strip().strip("`") == key for j in rows):
        return text, False
    lines.insert(rows[-1] + 1, row)
    return "\n".join(lines) + "\n", True


def link_home(vault):
    """Enlaza el índice de la narrativa desde MOC_Inicio, al final de sus secciones, si falta."""
    path = vault / HOME
    if not path.is_file():
        return False
    lines = path.read_text(encoding="utf-8").splitlines()
    if any(f"[[{MOC}]]" in line for line in lines):
        return False
    start = next((i for i, line in enumerate(lines) if line.strip() == "## Secciones"), None)
    if start is None:
        return False
    at = start + 1
    while at < len(lines) and lines[at].startswith("- "):
        at += 1
    lines.insert(at, HOME_LINE)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return True


def prepare(vault, form):
    created, notes = [], []
    root = vault / NARRATIVE_FOLDER
    write_new(root / "README.md", ROOT_README, created)
    write_new(root / f"{MOC}.md", MOC_TEXT, created)
    folder = root / FORMS[form]
    write_new(folder / "README.md", f"# {FORMS[form]}\n\n{FORM_TEXT[form]} Ver [[{MOC}]].\n", created)
    write_new(vault / TEMPLATE, (SKILL / "assets" / "plantilla.md").read_text(encoding="utf-8"), created)
    if link_home(vault):
        notes.append(f"Índice enlazado desde {HOME}.")
    guide = vault / GUIDE
    if guide.is_file():
        text = guide.read_text(encoding="utf-8")
        rows = [("Tipos registrados", f"| {NARRATIVE_TYPE} | `{NARRATIVE_FOLDER}/<Forma>` (Relatos, Escenas, Cronicas, "
                                      f"Documentos) | Plantilla_Narracion | narrar |"),
                ("Carpetas añadidas por skills", f"| `{NARRATIVE_FOLDER}` | Narraciones ambientadas en el mundo (no son "
                                                 f"entidades), con su índice {MOC} | narrar |"),
                ("Carpetas añadidas por skills", f"| `{NARRATIVE_FOLDER}/{FORMS[form]}` | {FORM_TEXT[form]} | narrar |")]
        changed = False
        for heading, row in rows:
            text, added = add_row(text, heading, row)
            changed |= added
        if changed:
            guide.write_text(text, encoding="utf-8", newline="\n")
            notes.append("Registrado en la Guía de Organización (tipo y carpetas).")
    else:
        notes.append(f"AVISO: no encuentro {GUIDE}; registra a mano el tipo {NARRATIVE_TYPE} y sus carpetas.")
    print(f"Carpeta de la narración: {NARRATIVE_FOLDER}/{FORMS[form]}")
    print(f"Plantilla: {TEMPLATE}")
    for path in created:
        print(f"Creado: {path.relative_to(vault).as_posix()}")
    for line in notes:
        print(line)


def note_parts(path):
    """(propiedades, cuerpo, título, resumen) de una narración."""
    frontmatter, body = split_note(path.read_text(encoding="utf-8"))
    props = parse_frontmatter(frontmatter or [], [])
    heading = next((line for line in body if line.startswith("# ")), "")
    title = heading.lstrip("# ").strip()
    title = title.split(" ", 1)[1] if " " in title and not title.split(" ", 1)[0].isalnum() else title
    after = body[body.index(heading) + 1:] if heading else body
    quote = next((line for line in after if line.strip().startswith("> ")), "")
    return props, body, title, strip_links(quote.strip()[2:].strip())


def check(vault, path):
    errors, warnings = [], []
    props, body, title, summary = note_parts(path)
    relative = path.relative_to(vault).as_posix()
    value = lambda key: unquote(first(props.get(key)) or "").strip()
    if value("tipo") != NARRATIVE_TYPE:
        errors.append(f"`tipo` debe ser `{NARRATIVE_TYPE}`")
    form = value("forma")
    if form not in FORMS:
        errors.append(f"`forma` debe ser una de: {', '.join(FORMS)}")
    elif not relative.startswith(f"{NARRATIVE_FOLDER}/{FORMS[form]}/"):
        errors.append(f"una narración de forma «{form}» va en {NARRATIVE_FOLDER}/{FORMS[form]}")
    if value("estado") not in STATES:
        errors.append(f"`estado` debe ser {' o '.join(STATES)}")
    tags = [unquote(t).lstrip("#") for t in props.get("tags", [])]
    secrets_used = value("usa_secretos").lower() == "true"
    if NARRATIVE_TYPE not in tags:
        errors.append(f"falta la etiqueta `{NARRATIVE_TYPE}` en `tags`")
    if secrets_used and SECRET_TYPE not in tags:
        errors.append(f"usa secretos: lleva también la etiqueta `{SECRET_TYPE}` (así queda fuera del «Grafo sin secretos»)")
    if not summary:
        errors.append("falta el resumen en cita bajo el título")
    if not any(line.strip() == "## Notas" for line in body):
        errors.append("falta la sección «Notas» (cuándo y dónde, lo del mundo que usa, lo inventado, la voz)")
    elif not any("Inventado aquí" in line for line in body):
        warnings.append("en «Notas» falta «Inventado aquí» (lo que la narración inventa y no está en el mundo)")

    names, _ = index_vault(vault)
    index = load_index(vault)
    by_name = {e["name"].lower(): e for e in index}
    archive = vault / ARCHIVED_FOLDER
    archived = {p.stem.lower() for p in archive.rglob("*.md")} if archive.is_dir() else set()
    stories = {p.stem.lower() for p in (vault / NARRATIVE_FOLDER).rglob("*.md")}
    text = path.read_text(encoding="utf-8")
    for target in sorted({m.group(1).strip() for m in LINK_RE.finditer(text)}):
        key = target.lower()
        if ATTACHMENT_RE.search(target):
            if key not in names:
                warnings.append(f"la imagen [[{target}]] no existe")
            continue
        if key in archived:
            warnings.append(f"enlaza a [[{target}]], que está archivada")
        elif key not in names:
            errors.append(f"enlaza a [[{target}]], que no tiene nota: en una narración solo se enlaza lo que ya existe "
                          f"(lo inventado va sin enlace, en «Inventado aquí»)")
        elif key in by_name and by_name[key]["tipo"] == SECRET_TYPE and not secrets_used:
            errors.append(f"enlaza al secreto [[{target}]] sin `usa_secretos: true`")

    families = {t: m.get("familia", t) for t, m in load_modules().items()}
    for key, wanted in (("donde", "lugar"), ("personajes", "personaje")):
        for target in (link_value(v) for v in props.get(key, [])):
            entry = by_name.get((target or "").lower())
            if entry and wanted not in (entry["tipo"], families.get(entry["tipo"])):
                warnings.append(f"`{key}` nombra a [[{target}]], que es {entry['tipo']}")
    previous = link_value(first(props.get("sigue_a")) or "")
    if previous and previous.lower() not in stories:
        errors.append(f"`sigue_a` debe ser otra narración, y [[{previous}]] no lo es")

    when = int_value(value("cuando"))
    if when is not None:
        modules = load_modules()
        now = read_world(vault)["ano_actual"]
        if now is not None and when > now:
            warnings.append(f"transcurre en {when}, después del presente del mundo ({now})")
        for key in ("personajes", "donde"):
            for target in (link_value(v) for v in props.get(key, [])):
                entry = by_name.get((target or "").lower())
                if not entry:
                    continue
                begin_key, end_key = date_keys(modules.get(entry["tipo"], {}))
                begin = int_value(first(entry["props"].get(begin_key))) if begin_key else None
                end = int_value(first(entry["props"].get(end_key))) if end_key else None
                if begin is not None and when < begin:
                    (errors if key == "personajes" else warnings).append(
                        f"[[{target}]] aún no {'había nacido' if key == 'personajes' else 'existía'} en {when} "
                        f"({begin_key} {begin})")
                if end is not None and when > end:
                    warnings.append(f"[[{target}]] ya {'había muerto' if key == 'personajes' else 'no existía'} en {when} "
                                    f"({end_key} {end}): salvo que sea un recuerdo, una aparición o un lugar en ruinas")
    # El texto de la narración: entre el resumen y la raya que abre sus notas
    start = next((i + 1 for i, line in enumerate(body) if line.strip().startswith("> ")), 0)
    end = next((i for i in range(start, len(body)) if body[i].strip() == "---"), len(body))
    words = len(re.findall(r"\w+", strip_links("\n".join(body[start:end]))))
    print(f"{relative} ({title or 'sin título'}) · {words} palabras")
    for message in errors:
        print(f"  ERROR: {message}")
    for message in warnings:
        print(f"  AVISO: {message}")
    if not errors and not warnings:
        print("  Correcta.")
    return 1 if errors else 0


def md_link(vault, path, text):
    target = Path(os.path.relpath(path, Path.cwd())).as_posix()
    return f"[{text}]({target.replace(' ', '%20')})"


def listing(vault, about, series):
    folder = vault / NARRATIVE_FOLDER
    calendar = reference_calendar(load_calendars(vault))
    rows = []
    for path in sorted(folder.rglob("*.md")) if folder.is_dir() else []:
        if path.name == "README.md" or path.name.startswith("MOC_"):
            continue
        props, body, title, summary = note_parts(path)
        value = lambda key: unquote(first(props.get(key)) or "").strip()
        if series and normalize(value("serie")) != normalize(series):
            continue
        links = {m.group(1).strip().lower() for m in LINK_RE.finditer(path.read_text(encoding="utf-8"))}
        if about and about.strip("[]").lower() not in links:
            continue
        when = int_value(value("cuando"))
        rows.append((value("serie").lower(), when if when is not None else 10 ** 9, title.lower(), path, props, title,
                     summary, value))
    rows.sort(key=lambda row: row[:3])
    print(f"Narraciones: {len(rows)}" + (f" que usan {about}" if about else "") + (f" de la serie «{series}»" if series else ""))
    for *_, path, props, title, summary, value in rows:
        when = int_value(value("cuando"))
        moment = value("momento") or (format_year(calendar, when) if calendar and when is not None
                                      else (f"año {when}" if when is not None else ""))
        extra = " · ".join(part for part in (value("forma"), moment, f"serie: {value('serie')}" if value("serie") else "",
                                             value("estado")) if part)
        text = summary if len(summary) <= SUMMARY_CHARS else summary[:SUMMARY_CHARS].rsplit(" ", 1)[0] + "…"
        print(f"- {md_link(vault, path, title)} · {extra} — {text}")


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare", help="Deja lista la estructura para una narración")
    prep.add_argument("form", choices=sorted(FORMS), help="La forma de la narración")
    chk = sub.add_parser("check", help="Comprueba una narración")
    chk.add_argument("note", help="Ruta o nombre de la narración")
    lst = sub.add_parser("list", help="Las narraciones")
    lst.add_argument("--about", help="Solo las que usan esta entidad")
    lst.add_argument("--serie", help="Solo las de esta serie")
    args = parser.parse_args()

    vault = vault_path(args.vault).resolve()
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    if args.command == "prepare":
        prepare(vault, args.form)
    elif args.command == "check":
        candidates = [Path(args.note), vault / args.note]
        candidates += sorted((vault / NARRATIVE_FOLDER).rglob(f"{Path(args.note).stem}.md"))
        path = next((p for p in candidates if p.is_file()), None)
        if not path:
            sys.exit(f"Error: no encuentro la narración '{args.note}'.")
        sys.exit(check(vault, path.resolve()))
    else:
        listing(vault, args.about, args.serie)


if __name__ == "__main__":
    main()
