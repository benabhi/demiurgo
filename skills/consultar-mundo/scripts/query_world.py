#!/usr/bin/env python3
"""Consultas sobre el mundo sin leer la bóveda: lo que hace falta para responder una pregunta, con el estado
de cada cosa (canon, borrador, pendiente) y los enlaces en Markdown, para citarlos en el chat.

  --about NOTA            Qué es una entidad: su estado, dónde está, sus fechas, sus relaciones (con su
                          propiedad y el estado de cada una), quién la nombra y cómo, sus secretos (🔒,
                          aparte), las preguntas abiertas que la nombran y sus secciones. Si es un enlace
                          pendiente, lo que dicen de él las notas que lo nombran.
  --in LUGAR              Lo que hay dentro de un lugar (también en sus barrios, sus lugares y sus comarcas),
                          por tipo y con cómo se relaciona cada cosa con él, y lo que se nombra dentro y
                          aún no tiene nota.
  --timeline              Lo que tiene fecha, en orden (eras, eventos, nacimientos, fundaciones…), con los
                          años del calendario de referencia; --from y --to acotan (años del eje de la Ficha),
                          --type filtra.
  --outline NOTA          Las secciones de una nota, con sus líneas, para leer solo la que hace falta.
  --section NOTA SECCIÓN  El texto de una o varias secciones (basta el principio del título).
  --no-secrets            Sin secretos: ni los muestra ni dice que existen (para enseñar el mundo).

Ejemplos:  query_world.py --about Aldric_Voss
           query_world.py --in Puerto_Gris
           query_world.py --timeline --from 300 --to 420 --type evento
           query_world.py --section Puerto_Gris "Gobierno" "Problemas"
           query_world.py --about Gremio_del_Puerto --no-secrets"""
import argparse
import os
import re
import sys
from pathlib import Path

# La lógica común vive en los scripts de crear-entidad
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "crear-entidad" / "scripts"))
from build_context import region_chain  # noqa: E402
from vault_lib import (ARCHIVED_FOLDER, CONTAINMENT_PROPS, OPEN_QUESTIONS, OUTSIDE_TYPE, SECRET_TYPE,  # noqa: E402
                       blocked_links, date_keys, find_gaps, first, format_year, gap_kind, int_value, load_calendars,
                       load_index, load_modules, normalize, read_world, reference_calendar, split_note, strip_links)
from vault_lib import vault_path  # noqa: E402

MAX_PER_GROUP = 15
MAX_MENTIONS = 6
SUMMARY_CHARS = 110
# Lo que se lee de una mención: un trozo de la línea alrededor del nombre
MENTION_CHARS, MENTION_BEFORE = 200, 70
# Dónde está algo que no es un lugar con región: su residencia o su ubicación actual
WHERE_PROPS = CONTAINMENT_PROPS + ("residencia", "ubicacion_actual")


def md_link(vault, relative, text):
    """Enlace Markdown a un archivo de la bóveda, relativo al directorio de trabajo (se abre con un clic)."""
    target = Path(os.path.relpath(vault / relative, Path.cwd())).as_posix()
    return f"[{text}]({target.replace(' ', '%20')})"


def around(line, link):
    """El trozo legible de una línea alrededor de un enlace (sin marcas ni enlaces)."""
    pattern = re.compile(r"\[\[" + re.escape(link) + r"(?:[#^][^\]|]*)?(?:\\?\|([^\]]*))?\]\]", re.IGNORECASE)
    match = pattern.search(line)
    shown = (match.group(1) if match and match.group(1) else link.replace("_", " ")).strip()
    clean = re.sub(r"\*\*|__", "", strip_links(line.strip())).strip("-|> ").replace(" | ", " — ")
    start = max(clean.find(shown) - MENTION_BEFORE, 0)
    piece = clean[start:start + MENTION_CHARS].strip()
    return ("…" if start else "") + piece + ("…" if start + MENTION_CHARS < len(clean) else "")


def short(text, limit=SUMMARY_CHARS):
    text = strip_links(text or "").strip()
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + "…"


class World:
    """Lo que hace falta para responder: el índice, los enlaces pendientes, lo archivado y el calendario."""

    def __init__(self, vault, secrets):
        self.vault = vault
        self.modules = load_modules()
        self.index = [e for e in load_index(vault) if secrets or e["tipo"] != SECRET_TYPE]
        self.by_name = {e["name"].lower(): e for e in self.index}
        self.gaps = {g["link"].lower(): g for g in find_gaps(vault)[0]}
        folder = vault / ARCHIVED_FOLDER
        self.archived = {p.stem.lower() for p in folder.rglob("*.md")} if folder.is_dir() else set()
        self.calendar = reference_calendar(load_calendars(vault))
        self.world = read_world(vault)
        self.blocked = blocked_links(vault)

    def find(self, name):
        """La entidad por su nombre de archivo, su título o un alias; None si no hay ninguna."""
        key = name.strip().strip("[]").lower()
        if key in self.by_name:
            return self.by_name[key]
        wanted = normalize(name)
        return next((e for e in self.index if wanted in [normalize(e["titulo"])] + [normalize(a) for a in e["aliases"]]),
                    None)

    def link(self, entry):
        return md_link(self.vault, entry["path"], entry["titulo"] or entry["name"])

    def year(self, value):
        if value is None:
            return None
        return format_year(self.calendar, value) if self.calendar else f"año {value}"

    def describe(self, target):
        """Un destino de una relación con su estado: la entidad (canon o borrador), un enlace pendiente, lo de
        fuera del mundo, algo archivado o un archivo."""
        entry = self.by_name.get(target.lower())
        if entry:
            return f"{self.link(entry)} ({entry['tipo']}, {entry['estado']})"
        gap = self.gaps.get(target.lower())
        shown = target.replace("_", " ")
        if gap and gap["expected_type"] == OUTSIDE_TYPE:
            return f"{shown} (fuera del mundo: solo se nombra)"
        if gap:
            return f"{shown} (pendiente: aún no tiene nota" + (f"; {gap_kind(gap)})" if gap["expected_type"] else ")")
        if target.lower() in self.archived:
            return f"{shown} (archivada)"
        return shown

    def relation_props(self, entry):
        return set(self.modules.get(entry["tipo"], {}).get("relaciones", {}))


def secrets_about(world, name):
    return [e for e in world.index if e["tipo"] == SECRET_TYPE and name.lower() in (t.lower() for t in e["enlaces"])]


def questions_about(world, name):
    path = world.vault / OPEN_QUESTIONS
    if not path.is_file():
        return []
    pattern = re.compile(r"\[\[" + re.escape(name) + r"(?=[\]|#^\\])", re.IGNORECASE)
    return [strip_links(line.strip()) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("- [ ]") and pattern.search(line)]


def sections(vault, entry):
    """[(nivel, título, línea de inicio, número de líneas)] de las secciones de una nota."""
    lines = (vault / entry["path"]).read_text(encoding="utf-8").splitlines()
    heads = [(i, len(m.group(1)), m.group(2).strip()) for i, line in enumerate(lines)
             for m in [re.match(r"^(#{2,3})\s+(.*)$", line)] if m]
    result = []
    for n, (i, level, title) in enumerate(heads):
        end = next((j for j, lv, _ in heads[n + 1:] if lv <= level), len(lines))
        result.append((level, title, i, end - i - 1))
    return result, lines


def about(world, name):
    entry = world.find(name)
    if not entry:
        gap = world.gaps.get(name.strip().strip("[]").lower())
        # Sin secretos, un enlace pendiente que solo nombra un secreto no existe para quien pregunta
        if gap and visible_notes(world, gap):
            return pending_card(world, gap)
        close = [e for e in world.index if normalize(name) in normalize(e["titulo"]) or normalize(name) in normalize(e["name"])]
        out = [f"«{name}» no es una entidad ni un enlace pendiente del mundo."]
        if close:
            out.append("Parecidos: " + ", ".join(world.link(e) for e in close[:MAX_MENTIONS]))
        else:
            out.append("Prueba con search_vault.py, que busca también en los resúmenes, el Glosario y las preguntas.")
        return out
    out = [f"{world.link(entry)} · {entry['tipo']} · {entry['estado']} · relevancia {entry['relevancia']}"]
    if entry["resumen"]:
        out.append(f"> {entry['resumen']}")
    if entry["aliases"]:
        out.append(f"- Otros nombres: {', '.join(entry['aliases'])}")
    chain = region_chain(entry, world.by_name, set())
    if chain:
        out.append("- Dónde está: " + " › ".join(f"{world.link(p)} ({p['tipo']})" for p in chain))
    else:
        # Lo que la contiene aún no tiene nota: se dice igual
        where = [t for key in WHERE_PROPS for t in entry["relaciones"].get(key, [])]
        if where:
            out.append("- Dónde está: " + ", ".join(world.describe(t) for t in where))
    module = world.modules.get(entry["tipo"], {})
    dates = [(key, int_value(first(entry["props"].get(key)))) for key in module.get("fechas", [])]
    dates = [(key, value) for key, value in dates if value is not None]
    if dates:
        out.append("- Fechas: " + " · ".join(f"{key.replace('_', ' ')} {world.year(value)}" for key, value in dates))
    props = world.relation_props(entry)
    own = [(key, values) for key, values in entry["relaciones"].items() if key in props]
    if own:
        out.append("- Sus relaciones:")
        out += [f"  - {key}: " + ", ".join(world.describe(t) for t in values) for key, values in own]
    incoming, mentioned = {}, []
    for other in world.index:
        if other is entry or other["tipo"] == SECRET_TYPE:
            continue
        keys = [key for key, values in other["relaciones"].items()
                if key in world.relation_props(other) and entry["name"].lower() in (v.lower() for v in values)]
        for key in keys:
            incoming.setdefault(key, []).append(other)
        if not keys and entry["name"].lower() in (t.lower() for t in other["enlaces"]):
            mentioned.append(other)
    if incoming:
        out.append("- La tienen en sus relaciones:")
        for key, others in sorted(incoming.items()):
            out.append(f"  - como `{key}`: " + ", ".join(f"{world.link(o)} ({o['tipo']}, {o['estado']})"
                                                       for o in others[:MAX_PER_GROUP])
                       + (f" … y {len(others) - MAX_PER_GROUP} más" if len(others) > MAX_PER_GROUP else ""))
    if mentioned:
        out.append("- La nombran en su texto: " + ", ".join(world.link(o) for o in mentioned[:MAX_PER_GROUP])
                   + (f" … y {len(mentioned) - MAX_PER_GROUP} más" if len(mentioned) > MAX_PER_GROUP else ""))
    secrets = secrets_about(world, entry["name"]) if entry["tipo"] != SECRET_TYPE else []
    for secret in secrets:
        out.append(f"- 🔒 Secreto (la verdad, solo para el autor): {world.link(secret)} ({secret['estado']}) — "
                   f"{short(secret['resumen'])}")
    for question in questions_about(world, entry["name"]):
        out.append(f"- Por decidir: {question[len('- [ ]'):].strip()}")
    heads, _ = sections(world.vault, entry)
    if heads:
        out.append("- Secciones: " + ", ".join(f"{title} ({count})" for level, title, _, count in heads if level == 2))
    return out


def visible_notes(world, gap):
    """Las notas de entidades que nombran un enlace pendiente y que se pueden mostrar (sin secretos, si se piden así)."""
    paths = {e["path"] for e in world.index}
    return sorted({o["note"] for o in gap["occurrences"]} & paths)


def pending_card(world, gap):
    """Un enlace pendiente: su tipo y lo que dicen de él las notas que lo nombran."""
    shown = gap["link"].replace("_", " ")
    if gap["expected_type"] == OUTSIDE_TYPE:
        head = f"{shown}: fuera del mundo; se nombra como referencia y no tiene nota."
    else:
        head = (f"{shown}: aún no tiene nota (enlace pendiente" + (f" de tipo {gap_kind(gap)}" if gap["expected_type"] else "")
                + ("; lo que lo afirma espera tu confirmación en Preguntas Abiertas" if gap["link"].lower() in world.blocked
                   else "") + ").")
    out = [head, "Lo que dicen las notas que lo nombran:"]
    pattern = re.compile(r"\[\[" + re.escape(gap["link"]) + r"(?=[\]|#^\\])", re.IGNORECASE)
    notes = visible_notes(world, gap)
    for note in notes[:MAX_MENTIONS]:
        entry = next((e for e in world.index if e["path"] == note), None)
        if not entry:
            continue
        _, body = split_note((world.vault / note).read_text(encoding="utf-8"))
        line = next((l for l in body if pattern.search(l)), None)
        props = [o["property"] for o in gap["occurrences"] if o["note"] == note and o["property"]]
        secret = entry["tipo"] == SECRET_TYPE
        out.append(f"- {'🔒 ' if secret else ''}{world.link(entry)} ({entry['estado']}"
                   + ("; secreto: la verdad, solo para el autor" if secret else "") + ")"
                   + (f", en `{props[0]}`" if props else "")
                   + (f": {around(line, gap['link'])}" if line else ""))
    if len(notes) > MAX_MENTIONS:
        out.append(f"- … y {len(notes) - MAX_MENTIONS} nota(s) más")
    return out


def inside(world, name):
    place = world.find(name)
    if not place:
        return [f"«{name}» no es una entidad del mundo."]
    members = {place["name"].lower()}
    changed = True
    while changed:
        changed = False
        for entry in world.index:
            if entry["name"].lower() in members:
                continue
            ups = [t.lower() for key in CONTAINMENT_PROPS for t in entry["relaciones"].get(key, [])]
            if any(u in members for u in ups):
                members.add(entry["name"].lower())
                changed = True
    groups = {}
    for entry in world.index:
        if entry is place:
            continue
        hits = [(key, t) for key, values in entry["relaciones"].items() if key in world.relation_props(entry)
                for t in values if t.lower() in members]
        if hits:
            groups.setdefault(entry["tipo"], []).append((entry, hits))
    out = [f"Dentro de {world.link(place)} ({place['tipo']}, {place['estado']}):"]
    if not groups:
        out.append("- Nada con nota todavía.")
    for kind in sorted(groups, key=lambda k: (-len(groups[k]), k)):
        items = sorted(groups[kind], key=lambda item: -(item[0]["relevancia"] or 0))
        out.append(f"- {kind} ({len(items)}):")
        for entry, hits in items[:MAX_PER_GROUP]:
            how = "; ".join(f"{key}: {world.by_name[t.lower()]['titulo'] if t.lower() in world.by_name else t.replace('_', ' ')}"
                            for key, t in hits[:3])
            out.append(f"  - {world.link(entry)} ({entry['estado']}) · {how} — {short(entry['resumen'], 80)}")
        if len(items) > MAX_PER_GROUP:
            out.append(f"  - … y {len(items) - MAX_PER_GROUP} más")
    named = []
    for member in members:
        entry = world.by_name.get(member)
        for key, values in (entry["relaciones"].items() if entry else []):
            if key in world.relation_props(entry):
                named += [(key, t) for t in values if t.lower() in world.gaps
                          and world.gaps[t.lower()]["expected_type"] != OUTSIDE_TYPE]
    if named:
        out.append("- Se nombra dentro y aún no tiene nota: "
                   + ", ".join(sorted({f"{t.replace('_', ' ')} ({key})" for key, t in named})))
    return out


def timeline(world, start, end, kind):
    rows = []
    for entry in world.index:
        if kind and entry["tipo"] != kind:
            continue
        first_key, last_key = date_keys(world.modules.get(entry["tipo"], {}))
        begin = int_value(first(entry["props"].get(first_key))) if first_key else None
        finish = int_value(first(entry["props"].get(last_key))) if last_key else None
        if begin is None:
            continue
        if (end is not None and begin > end) or (start is not None and (finish if finish is not None else begin) < start):
            continue
        rows.append((begin, finish, first_key, last_key, entry))
    rows.sort(key=lambda row: (row[0], row[4]["name"].lower()))
    now = world.world["ano_actual"]
    out = [f"Cronología ({len(rows)})" + (f" · hoy: {world.year(now)}" if now is not None else "") + ":"]
    placed = now is None
    for begin, finish, first_key, last_key, entry in rows:
        if not placed and begin > now:
            out.append(f"- ── hoy, {world.year(now)} ──")
            placed = True
        span = f"{first_key} {world.year(begin)}" + (f" · {last_key} {world.year(finish)}" if finish is not None else "")
        out.append(f"- {world.year(begin)} · {world.link(entry)} ({entry['tipo']}, {entry['estado']}) — {span} · "
                   f"{short(entry['resumen'], 90)}")
    if not placed:
        out.append(f"- ── hoy, {world.year(now)} ──")
    if not rows:
        out.append("- Nada con fecha" + (" en ese tramo." if start is not None or end is not None or kind else "."))
    return out


def outline(world, name):
    entry = world.find(name)
    if not entry:
        return [f"«{name}» no es una entidad del mundo."]
    heads, _ = sections(world.vault, entry)
    return [f"{world.link(entry)} ({entry['tipo']}, {entry['estado']}) — secciones:"] + \
        [f"{'  ' if level == 3 else ''}- {title} ({count} líneas)" for level, title, _, count in heads]


def read_sections(world, name, wanted):
    entry = world.find(name)
    if not entry:
        return [f"«{name}» no es una entidad del mundo."]
    heads, lines = sections(world.vault, entry)
    out = [f"{world.link(entry)} ({entry['tipo']}, {entry['estado']})"]
    for title in wanted:
        match = next((h for h in heads if normalize(h[1]).startswith(normalize(title))), None)
        if not match:
            out.append(f"(no tiene la sección «{title}»: " + ", ".join(h[1] for h in heads if h[0] == 2) + ")")
            continue
        level, heading, start, count = match
        out += ["", *lines[start:start + count + 1]]
    return out


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--about", metavar="NOTA", help="Qué es una entidad, o qué se dice de un enlace pendiente")
    parser.add_argument("--in", dest="inside", metavar="LUGAR", help="Lo que hay dentro de un lugar")
    parser.add_argument("--timeline", action="store_true", help="Lo que tiene fecha, en orden")
    parser.add_argument("--from", dest="start", type=int, help="Desde este año del eje (con --timeline)")
    parser.add_argument("--to", dest="end", type=int, help="Hasta este año del eje (con --timeline)")
    parser.add_argument("--type", help="Solo un tipo (con --timeline)")
    parser.add_argument("--outline", metavar="NOTA", help="Las secciones de una nota")
    parser.add_argument("--section", nargs="+", metavar="NOTA SECCIÓN", help="Una nota y las secciones que leer")
    parser.add_argument("--no-secrets", action="store_true", help="Sin secretos: ni los muestra ni dice que existen")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    world = World(vault, secrets=not args.no_secrets)
    if args.about:
        out = about(world, args.about)
    elif args.inside:
        out = inside(world, args.inside)
    elif args.timeline:
        out = timeline(world, args.start, args.end, args.type)
    elif args.outline:
        out = outline(world, args.outline)
    elif args.section and len(args.section) >= 2:
        out = read_sections(world, args.section[0], args.section[1:])
    else:
        sys.exit("Error: indica una consulta: --about, --in, --timeline, --outline o --section NOTA SECCIÓN.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
