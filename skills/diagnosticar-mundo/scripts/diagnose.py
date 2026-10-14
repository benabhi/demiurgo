#!/usr/bin/env python3
"""El diagnóstico de una bóveda: su salud (lo que está mal), si está al día con las skills (lo que cambió en ellas
desde que se creó la bóveda) y lo que pide atención sin ser un error. Usa las mismas comprobaciones que el cierre
del mundo (health.py), en el nivel de un mundo abierto: los enlaces pendientes y los borradores no son un error.

Sin opciones, solo diagnostica. Los arreglos:
  --fix         los seguros: rehace el registro de enlaces pendientes y las Estadísticas, crea la Bitácora si
                falta, pone `estado_mundo` en la Ficha si falta, copia las tablas del motor que falten y añade al grafo
                los colores de los tipos nuevos (sin un grafo abierto en Obsidian).
  --templates   añade a las plantillas instaladas (01_Plantillas) las propiedades y las secciones nuevas de su
                tipo.
  --migrate     añade a las notas las propiedades nuevas de su tipo, vacías (las que check_note da por faltantes).
  --tidy        aparta a 02_Activos/Anteriores, con `_suelta`, las imágenes que ninguna nota usa.
El CLAUDE.md y las guías no se tocan: el diagnóstico dice cuántas líneas de su versión actual les faltan, --details
las muestra enteras y con su sitio, y Claude las incorpora con el visto bueno del usuario.

Ejemplos:  diagnose.py
           diagnose.py --fix
           diagnose.py --templates --migrate
           diagnose.py --details"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]
# La lógica común vive en los scripts de crear-entidad
sys.path.insert(0, str(SKILLS / "crear-entidad" / "scripts"))
from graph_colors import configure_graph, type_colors  # noqa: E402
from health import (Health, broken_images, drafts, inbox, loose_images, map_states, missing_images,  # noqa: E402
                    open_questions, pending, tidy_images, undefined_pillars)
from map_key import frontmatter_end  # noqa: E402
from pending_links import build as build_registry  # noqa: E402
from pending_links import link_from_home as link_registry  # noqa: E402
from vault_lib import (CHRONICLE, ITEM_LINE_RE, KEY_LINE_RE, PENDING_NOTE, STATS_NOTE, WORLD_CLOSED,  # noqa: E402
                       WORLD_CLOSING, WORLD_OPEN, WORLD_SHEET, add_chronicle_entry, ensure_chronicle, find_gaps,
                       load_index, load_modules, parse_frontmatter, read_world, split_note, strip_links, world_state)
from vault_lib import vault_path  # noqa: E402
from world_stats import build_note, collect, plural, write_stats  # noqa: E402

TEMPLATES = "00_Sistema/01_Plantillas"
GUIDES = "00_Sistema/04_Convenciones"
GENERATION = "00_Sistema/06_Generacion"
GRAPH_FILE = ".obsidian/graph.json"
INIT_ASSETS = SKILLS / "inicializar-mundo" / "assets"
MOTOR_ASSETS = SKILLS / "expandir-mundo" / "assets"
EMPTY_ROW_RE = re.compile(r"^\|(\s*\|)+\s*$")
MISSING_PROP_RE = re.compile(r"falta la propiedad `([\w-]+)`")
# El motor se detiene con más borradores suyos sin revisar (el `--review-limit` por defecto de select_target)
MOTOR_LIMIT = 20
MAX_SHOWN = 6
STATE_TEXT = {WORLD_OPEN: "abierto", WORLD_CLOSING: "en cierre (sigue con /finalizar-mundo)", WORLD_CLOSED: "cerrado"}


def listed(items, limit=MAX_SHOWN):
    return ", ".join(items[:limit]) + (f" y {len(items) - limit} más" if len(items) > limit else "")


def short(text, size):
    """Un texto sin la sintaxis de los enlaces y, si es largo, recortado con «…»."""
    text = strip_links(text)
    return text if len(text) <= size else text[:size - 1].rstrip() + "…"


def agree(count, singular, plural_form):
    """El verbo que concuerda con la cantidad: «falta» o «faltan»."""
    return singular if count == 1 else plural_form


def line(ok, name, detail):
    return f"  {'✓' if ok else '✗'} {name}: {detail}"


# --- Al día con las skills --------------------------------------------------------------

def render(text, world):
    """Una plantilla de inicializar-mundo con los datos de este mundo (los que no cambian con las respuestas)."""
    props = world["props"]
    return (text.replace("{{MUNDO}}", str(props.get("mundo") or "")).replace("{{BOVEDA}}", world["boveda"])
            .replace("{{idioma}}", str(props.get("idioma") or "Español")))


def missing_lines(template, current, skip_section=None):
    """[(línea, su sección, la línea anterior de la plantilla)] de las líneas de la plantilla que no están en el
    archivo, sin las vacías, las de datos del mundo y las de una sección que se rellena con las respuestas."""
    present = {item.strip() for item in current.splitlines()}
    found, skipping, section, previous = [], False, "", ""
    for raw in template.splitlines():
        text = raw.strip()
        if raw.startswith("## "):
            section, skipping = text[3:], text[3:] == skip_section
        if skipping or not text or "{{" in text or EMPTY_ROW_RE.match(text):
            continue
        if text not in present:
            found.append((text, section, previous))
        previous = text
    return found


def claude_md(vault, world):
    path = vault.resolve().parent / "CLAUDE.md"
    if not path.is_file():
        return None
    template = render((INIT_ASSETS / "CLAUDE.md.tpl").read_text(encoding="utf-8"), world)
    return missing_lines(template, path.read_text(encoding="utf-8"), skip_section="Reglas de contenido")


def guides(vault, world):
    found = {}
    for source in sorted((INIT_ASSETS / "convenciones").glob("*.md")):
        target = vault / GUIDES / source.name
        found[source.stem] = (None if not target.is_file() else
                              missing_lines(render(source.read_text(encoding="utf-8"), world),
                                            target.read_text(encoding="utf-8")))
    return found


def template_sources():
    """{nombre de la plantilla instalada: la plantilla de la skill}."""
    sources = {f"Plantilla_{folder.name.capitalize()}.md": folder / "plantilla.md"
               for folder in sorted((SKILLS / "crear-entidad" / "tipos").iterdir()) if (folder / "plantilla.md").is_file()}
    sources["Plantilla_Narracion.md"] = SKILLS / "narrar" / "assets" / "plantilla.md"
    return sources


def frontmatter_blocks(text):
    """[(propiedad, [sus líneas])] del frontmatter, en orden."""
    frontmatter, _ = split_note(text)
    blocks = []
    for raw in frontmatter or []:
        key = KEY_LINE_RE.match(raw)
        if key:
            blocks.append((key.group(1), [raw]))
        elif blocks and ITEM_LINE_RE.match(raw):
            blocks[-1][1].append(raw)
    return blocks


def outdated_templates(vault):
    """[(plantilla instalada, propiedades que le faltan, secciones que le faltan)]."""
    found = []
    for name, source in template_sources().items():
        installed = vault / TEMPLATES / name
        if not installed.is_file() or not source.is_file():
            continue
        new, old = source.read_text(encoding="utf-8"), installed.read_text(encoding="utf-8")
        have = {key for key, _ in frontmatter_blocks(old)}
        keys = [key for key, _ in frontmatter_blocks(new) if key not in have]
        headers = {title for title, _, _ in section_blocks(old.splitlines())}
        sections = [title for title, _, _ in section_blocks(new.splitlines()) if title not in headers]
        if keys or sections:
            found.append((name, keys, sections))
    return found


def section_blocks(lines):
    """[(título, inicio, fin)] de las secciones `## ` de unas líneas; el fin es donde empieza la siguiente."""
    starts = [i for i, text in enumerate(lines) if text.startswith("## ")]
    return [(lines[s].strip()[3:], s, starts[k + 1] if k + 1 < len(starts) else len(lines))
            for k, s in enumerate(starts)]


def missing_keys(errors):
    """Las propiedades que check_note da por faltantes, de sus errores."""
    return [m.group(1) for error in errors for m in [MISSING_PROP_RE.match(error)] if m]


def missing_properties(health):
    """{tipo: {propiedad: cuántas notas no la tienen}}."""
    found = {}
    for entry, errors, _ in health.note_checks():
        for key in missing_keys(errors):
            found.setdefault(entry["tipo"], {}).setdefault(key, 0)
            found[entry["tipo"]][key] += 1
    return found


def graph_missing(vault):
    path = vault / GRAPH_FILE
    if not path.is_file():
        return None
    try:
        groups = json.loads(path.read_text(encoding="utf-8")).get("colorGroups", [])
    except json.JSONDecodeError:
        return None
    present = {g.get("query", "").replace("tag:#", "").strip() for g in groups}
    return [tipo for tipo, _ in type_colors() if tipo not in present]


def system_notes(vault, health):
    """[(nota, qué le pasa)] de las notas del sistema que faltan o están atrasadas."""
    found = []
    if not (vault / CHRONICLE).is_file():
        found.append(("Bitácora", "falta"))
    stats = vault / STATS_NOTE
    if not stats.is_file():
        found.append(("Estadísticas", "faltan"))
    else:
        _, numbers = build_note(collect(vault), "")
        frontmatter, _ = split_note(stats.read_text(encoding="utf-8"))
        current = {k: str(v[0]).strip('"') for k, v in parse_frontmatter(frontmatter or [], []).items() if v}
        if any(current.get(k) != str(v) for k, v in numbers.items()):
            found.append(("Estadísticas", "atrasadas"))
    gaps = health.gaps
    if gaps and not (vault / PENDING_NOTE).is_file():
        found.append(("Registro de enlaces pendientes", "falta"))
    elif any("registro de enlaces pendientes está desactualizado" in w for w in health.audit()["avisos"]):
        found.append(("Registro de enlaces pendientes", "desactualizado"))
    return found


def generation_tables(vault):
    """Los archivos del motor (tablas, paquetes, registro) que faltan en una bóveda donde ya se usó: los mismos que
    copia setup_generation.py. Si el motor no se usó todavía, nada."""
    folder = vault / GENERATION
    if not folder.is_dir():
        return []
    return [p.relative_to(MOTOR_ASSETS).as_posix() for p in sorted(MOTOR_ASSETS.rglob("*.md"))
            if not (folder / p.relative_to(MOTOR_ASSETS)).exists()]


def unlinked_skills(vault):
    places = [vault.resolve().parent / ".claude" / "skills", Path.home() / ".claude" / "skills"]
    return [p.name for p in sorted(SKILLS.iterdir()) if (p / "SKILL.md").is_file()
            and not any((place / p.name).exists() for place in places)]


# --- Arreglos ----------------------------------------------------------------------

def add_blocks(text, blocks, only=None):
    """El texto con las propiedades de `blocks` que le faltan (solo las de `only`, si se da), cada una con sus
    líneas y en su sitio según el orden de `blocks` (el de la plantilla): tras la anterior que ya tiene. Devuelve
    (texto, las que añadió)."""
    lines = text.splitlines()
    end = frontmatter_end(lines)
    if end is None:
        return text, []
    added = []
    for position, (key, block) in enumerate(blocks):
        present = {m.group(1): i for i in range(1, end) for m in [KEY_LINE_RE.match(lines[i])] if m}
        if key in present or (only is not None and key not in only):
            continue
        previous = next((present[k] for k, _ in reversed(blocks[:position]) if k in present), None)
        at = end
        if previous is not None:
            at = previous + 1
            while at < end and ITEM_LINE_RE.match(lines[at]):
                at += 1
        lines[at:at] = block
        end += len(block)
        added.append(key)
    return "\n".join(lines) + "\n", added


def add_sections(text, source):
    """El texto con las secciones de `source` que le faltan, cada una tras la anterior que tiene (o antes de la
    siguiente, o al final). Devuelve (texto, las que añadió)."""
    lines, model = text.splitlines(), source.splitlines()
    wanted = section_blocks(model)
    added = []
    for position, (title, start, end) in enumerate(wanted):
        have = {t: (s, e) for t, s, e in section_blocks(lines)}
        if title in have:
            continue
        previous = next((have[t][1] for t, _, _ in reversed(wanted[:position]) if t in have), None)
        following = next((have[t][0] for t, _, _ in wanted[position + 1:] if t in have), None)
        at = previous if previous is not None else following if following is not None else len(lines)
        block = model[start:end]
        if block and block[-1].strip():
            block = block + [""]
        if at > 0 and lines[at - 1].strip():
            block = [""] + block
        lines[at:at] = block
        added.append(title)
    return "\n".join(lines).rstrip("\n") + "\n", added


def fix_safe(vault, health):
    """Los arreglos seguros. Devuelve (líneas del resumen, líneas para la Bitácora)."""
    out, log = [], []
    behind = dict(system_notes(vault, health))
    sheet = vault / WORLD_SHEET
    lines = sheet.read_text(encoding="utf-8").splitlines()
    if "estado_mundo" not in health.world["props"]:
        end = frontmatter_end(lines)
        at = next((i + 1 for i in range(1, end) if lines[i].startswith("mundo:")), end)
        lines.insert(at, "estado_mundo: abierto")
        sheet.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        out.append("Ficha: `estado_mundo: abierto`.")
        log.append("**Ficha:** con su estado, `estado_mundo: abierto`.")
    if "Bitácora" in behind:
        # Antes que el registro: el enlace que le hace MOC_Inicio no debe contar como pendiente
        out += ["Bitácora creada."] + [f"AVISO: {w}" for w in ensure_chronicle(vault)]
        log.append("**Bitácora:** creada.")
    registry = vault / PENDING_NOTE
    gaps, _ = find_gaps(vault)
    if gaps or registry.is_file():
        if not registry.is_file():
            # Primero existe, para que el enlace que le hace MOC_Inicio no cuente como pendiente
            registry.write_text("", encoding="utf-8")
            gaps, _ = find_gaps(vault)
        registry.write_text(build_registry(vault, gaps, load_modules(), load_index(vault)),
                            encoding="utf-8", newline="\n")
        out.append(f"Registro de enlaces pendientes rehecho ({len(gaps)}).")
        if "Registro de enlaces pendientes" in behind:
            log.append(f"**Registro de enlaces pendientes:** rehecho ({len(gaps)}).")
        linked = link_registry(vault)
        if linked:
            out.append(linked)
    missing = generation_tables(vault)
    if missing:
        result = subprocess.run([sys.executable, str(SKILLS / "expandir-mundo" / "scripts" / "setup_generation.py"),
                                 "--vault", str(vault)], capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0:
            out.append(f"Archivos del motor que faltaban, copiados: {listed(missing, 4)}.")
            log.append(f"**Archivos del motor** que faltaban: {listed(missing, 4)}.")
        else:
            out.append(f"AVISO: setup_generation.py falló: {(result.stderr or result.stdout).strip()[:200]}")
    colors = graph_missing(vault)
    if colors:
        out += configure_graph(vault)
        out.append("Si en Obsidian había un grafo abierto, habrá guardado el suyo encima: ciérralo y abre el marcador "
                   "«Grafo completo».")
        log.append(f"**Grafo:** con el color de {plural(len(colors), 'tipo')} más.")
    if "Estadísticas" in behind:
        log.append("**Estadísticas:** rehechas.")
    return out, log


def fix_templates(vault):
    """Pone al día las plantillas instaladas. Devuelve (líneas del resumen, líneas para la Bitácora)."""
    out = []
    for name, _, _ in outdated_templates(vault):
        installed = vault / TEMPLATES / name
        source = template_sources()[name].read_text(encoding="utf-8")
        text, keys = add_blocks(installed.read_text(encoding="utf-8"), frontmatter_blocks(source))
        text, sections = add_sections(text, source)
        installed.write_text(text, encoding="utf-8", newline="\n")
        out.append(f"{name}: " + "; ".join(part for part in (
            f"{agree(len(keys), 'añadida la propiedad', 'añadidas las propiedades')} {', '.join(keys)}" if keys else "",
            f"{agree(len(sections), 'añadida la sección', 'añadidas las secciones')} {', '.join(sections)}"
            if sections else "") if part))
    log = [f"**Plantillas instaladas** al día: {listed([item.split(':')[0][:-3] for item in out], 8)}."] if out else []
    return out or ["Las plantillas instaladas ya estaban al día."], log


def fix_migrate(vault, health):
    """Añade a las notas las propiedades nuevas de su tipo, vacías. Devuelve (líneas del resumen, líneas para la
    Bitácora)."""
    out, by_type = [], {}
    sources = {path.parent.name: path for path in (SKILLS / "crear-entidad" / "tipos").glob("*/plantilla.md")}
    for entry, errors, _ in health.note_checks():
        wanted = missing_keys(errors)
        if not wanted or entry["tipo"] not in sources:
            continue
        # Vacías: una lista (`[]`, o con sus elementos debajo) como `[]`; lo demás, como ""
        order = frontmatter_blocks(sources[entry["tipo"]].read_text(encoding="utf-8"))
        blocks = [(key, [f"{key}: []" if lines[0].split(":", 1)[1].strip() in ("[]", "") else f'{key}: ""'])
                  for key, lines in order]
        path = vault / entry["path"]
        text, added = add_blocks(path.read_text(encoding="utf-8"), blocks, only=set(wanted))
        if added:
            path.write_text(text, encoding="utf-8", newline="\n")
            out.append(f"{entry['name']}: {agree(len(added), 'añadida', 'añadidas')} {', '.join(added)}")
            notes, keys = by_type.setdefault(entry["tipo"], [0, set()])
            by_type[entry["tipo"]] = [notes + 1, keys | set(added)]
    log = [f"**Propiedades nuevas**, vacías, en {plural(len(out), 'nota')}: "
           + "; ".join(f"{tipo} ({', '.join(sorted(keys))})" for tipo, (_, keys) in sorted(by_type.items())) + "."] \
        if out else []
    return out or ["Ninguna nota necesitaba propiedades nuevas."], log


def tidy_lines(vault):
    """Aparta las imágenes sueltas. Devuelve (líneas del resumen, líneas para la Bitácora)."""
    lines = tidy_images(vault)
    moved = sum(1 for item in lines if item.startswith("Apartada:"))
    return lines, [f"**Imágenes sueltas** apartadas a `02_Activos/Anteriores`: {moved}."] if moved else []


# --- El diagnóstico ----------------------------------------------------------------

def diagnose(vault):
    health = Health(vault)
    world = dict(health.world, boveda=vault.name)
    out = [f"Bóveda «{world['props'].get('mundo') or vault.name}» · estado del mundo: "
           f"{STATE_TEXT.get(world_state(vault), world_state(vault))}"]

    out.append("Salud:")
    # Las propiedades que faltan porque la nota es anterior a su plantilla van en «Al día» (--migrate)
    errored = [(entry, others) for entry, errors, _ in health.note_checks()
               for others in [[e for e in errors if not MISSING_PROP_RE.match(e)]] if others]
    out.append(line(not errored, "Notas", "todas pasan check_note sin errores" if not errored else
                    f"{plural(len(errored), 'nota')} con errores: "
                    + listed([f"{e['name']} ({short(errors[0], 60)})" for e, errors in errored], 4)))
    broken = broken_images(health)
    out.append(line(not broken, "Imágenes enlazadas", "todas existen" if not broken else
                    f"{len(broken)} no {agree(len(broken), 'existe', 'existen')}: "
                    + listed([f"{n} → {img}" for n, img in broken], 4)))
    audit = health.audit()
    out.append(line(not audit["errores"], "Auditor", plural(len(audit["errores"]), "error", "errores")
                    + (f": {listed([short(e, 70) for e in audit['errores']], 3)}" if audit["errores"] else "")))
    loose = loose_images(vault)
    out.append(line(not loose, "Imágenes sueltas", "ninguna" if not loose else
                    f"{len(loose)} que ninguna nota usa: {listed([p.name for p in loose], 4)} (--tidy las aparta)"))

    out.append("Al día con las skills:")
    claude = claude_md(vault, world)
    out.append(line(claude == [], "CLAUDE.md", "al día" if claude == [] else "no lo encuentro" if claude is None else
                    f"le {agree(len(claude), 'falta', 'faltan')} {plural(len(claude), 'línea')} de su versión actual: "
                    + listed([short(text, 60) for text, _, _ in claude], 2) + " (--details)"))
    stale_guides = {name: lines for name, lines in guides(vault, world).items() if lines != []}
    out.append(line(not stale_guides, "Guías", "al día" if not stale_guides else
                    "; ".join(f"{name}: " + ("no está" if lines is None else
                                             f"le {agree(len(lines), 'falta', 'faltan')} {plural(len(lines), 'línea')}")
                              for name, lines in stale_guides.items()) + " (--details)"))
    templates = outdated_templates(vault)
    out.append(line(not templates, "Plantillas instaladas", "al día" if not templates else
                    listed([f"{name} (le {agree(len(keys) + len(sections), 'falta', 'faltan')} "
                            + ", ".join(keys + [f"la sección {title}" for title in sections]) + ")"
                            for name, keys, sections in templates], 3) + " (--templates)"))
    props = missing_properties(health)
    out.append(line(not props, "Propiedades nuevas en las notas", "ninguna por añadir" if not props else
                    listed([f"{tipo}: " + ", ".join(f"{key} ({plural(n, 'nota')})" for key, n in keys.items())
                            for tipo, keys in props.items()], 3) + " (--migrate)"))
    sheet = [key for key in ("estado_mundo",) if key not in health.world["props"]]
    out.append(line(not sheet, "Ficha", "al día" if not sheet else f"le falta {', '.join(sheet)} (--fix)"))
    graph = graph_missing(vault)
    out.append(line(not graph, "Grafo", "sin configurar (graph_colors.py)" if graph is None else "al día" if not graph
                    else "sin los colores de los tipos (--fix)" if len(graph) == len(type_colors())
                    else f"sin color: {listed(graph)} (--fix)"))
    notes = system_notes(vault, health)
    out.append(line(not notes, "Notas del sistema", "al día" if not notes else
                    listed([f"{n}: {what}" for n, what in notes]) + " (--fix)"))
    tables = generation_tables(vault)
    out.append(line(not tables, "Archivos del motor", "al día" if not tables else
                    f"{agree(len(tables), 'falta', 'faltan')} {len(tables)}: {listed(tables, 4)} (--fix)"))
    skills = unlinked_skills(vault)
    out.append(line(not skills, "Skills instaladas", "todas" if not skills else
                    f"{agree(len(skills), 'falta', 'faltan')} {listed(skills)} (ver la instalación en el README de "
                    f"Demiurgo: github.com/benabhi/demiurgo)"))

    out.append("Atención:")
    unrevised = drafts(health)
    if unrevised:
        motor = sum(1 for e in unrevised if e["origen"] == "procedural")
        out.append(f"  - Borradores: {len(unrevised)} ({motor} del motor, que se detiene con más de {MOTOR_LIMIT})"
                   f" → /revisar-mundo")
    links = pending(health)
    if links["all"]:
        ready, waiting = len(links["ready"]), len(links["waiting"])
        out.append(f"  - Enlaces pendientes: {len(links['all'])} ({ready} {agree(ready, 'se puede', 'se pueden')} "
                   f"crear, {waiting} {agree(waiting, 'espera', 'esperan')} una confirmación tuya, "
                   f"{len(links['untyped'])} sin tipo, {len(links['no_module'])} sin módulo)")
    questions = open_questions(vault)
    if questions:
        confirmations = sum(1 for q in questions if q[1])
        out.append(f"  - Preguntas abiertas: {len(questions)} "
                   f"({plural(confirmations, 'confirmación', 'confirmaciones')})")
    pillars = undefined_pillars(vault)
    if pillars:
        out.append(f"  - Pilares por definir: {listed(pillars)}")
    stale, _ = map_states(health)
    if stale:
        out.append(f"  - Mapas por dibujar: {listed([f'{n} ({why})' for n, why in stale], 3)}"
                   f" → /generar-imagen <Nota> mapa")
    missing = missing_images(health)
    if missing:
        out.append(f"  - Sin imagen: {listed(missing)} → /generar-imagen")
    warnings = [w for w in audit["avisos"] if "registro de enlaces pendientes" not in w]
    if warnings:
        out.append(f"  - Avisos del auditor: {len(warnings)}: {listed([short(w, 70) for w in warnings], 3)}")
    box = inbox(vault)
    if box:
        out.append(f"  - Bandeja de Entrada: {len(box)}: {listed(box, 4)}")
    if out[-1] == "Atención:":
        out.append("  - Nada.")
    return out


def details(vault):
    """Las líneas que les faltan al CLAUDE.md y a las guías, enteras y con su sitio, para que Claude las incorpore."""
    world = dict(read_world(vault), boveda=vault.name)
    files = [("CLAUDE.md", claude_md(vault, world), INIT_ASSETS / "CLAUDE.md.tpl")]
    files += [(f"{GUIDES}/{name}.md", lines, INIT_ASSETS / "convenciones" / f"{name}.md")
              for name, lines in guides(vault, world).items()]
    out = []
    for name, lines, source in files:
        model = source.relative_to(SKILLS).as_posix()
        if lines is None:
            out.append(f"{name}: no está. Rehazlo desde {model}, con los datos de la Ficha en sus marcadores.")
        elif lines:
            out.append(f"{name}: le {agree(len(lines), 'falta', 'faltan')} {plural(len(lines), 'línea')} "
                       f"(de {model}):")
            for text, section, previous in lines:
                place = f"en «{section}»" if section else "al principio"
                out.append(f"  - {place}, tras «{short(previous, 70)}»:" if previous else f"  - {place}:")
                out.append(f"      {text}")
    return out or ["El CLAUDE.md y las guías tienen todas las líneas de su versión actual."]


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--fix", action="store_true", help="Aplica los arreglos seguros")
    parser.add_argument("--templates", action="store_true", help="Pone al día las plantillas instaladas")
    parser.add_argument("--migrate", action="store_true", help="Añade a las notas las propiedades nuevas de su tipo")
    parser.add_argument("--tidy", action="store_true", help="Aparta las imágenes sueltas")
    parser.add_argument("--details", action="store_true",
                        help="Solo muestra, enteras y con su sitio, las líneas que les faltan al CLAUDE.md y a las guías")
    args = parser.parse_args()

    vault = vault_path(args.vault).resolve()
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    if not (vault / WORLD_SHEET).is_file():
        sys.exit(f"Error: {vault.name} no tiene Ficha del Mundo: créala con /inicializar-mundo.")
    if args.details:
        print("\n".join(details(vault)))
        return
    if args.migrate and world_state(vault) == WORLD_CLOSED:
        sys.exit("El mundo está cerrado: sus notas ya no cambian, y --migrate no se aplica. Para migrarlas, "
                 "reábrelo con /finalizar-mundo reabrir.")
    done, log = [], []
    for wanted, fix in ((args.templates, lambda: fix_templates(vault)),
                        (args.migrate, lambda: fix_migrate(vault, Health(vault))),
                        (args.tidy, lambda: tidy_lines(vault)),
                        (args.fix, lambda: fix_safe(vault, Health(vault)))):
        if wanted:
            lines, entry = fix()
            done += lines
            log += entry
    if log:
        warnings = add_chronicle_entry(vault, "Diagnóstico de la bóveda", [f"- {item}" for item in log])
        done += [f"AVISO: {w}" for w in warnings]
    if done:
        _, warnings = write_stats(vault)
        print("Arreglos:")
        print("\n".join(f"  - {item}" for item in done + ["Estadísticas rehechas."] + [f"AVISO: {w}" for w in warnings]))
        print()
    print("\n".join(diagnose(vault)))


if __name__ == "__main__":
    main()
