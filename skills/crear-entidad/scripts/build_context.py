#!/usr/bin/env python3
"""Arma el paquete de contexto para crear o completar una entidad sin leer toda la bóveda.

Para un enlace pendiente (hueco): qué dicen de él las notas que lo nombran y qué tipo se espera.
Para una entidad: su resumen y sus relaciones. En ambos casos añade los datos del mundo (año
actual, calendario, foco y eras en orden), las entidades relacionadas con su resumen de una línea
(por relevancia), la cadena de regiones, los nombres ya usados cerca y las preguntas abiertas
relacionadas.

Ejemplos:  build_context.py --target Capital_de_Reino_de_Ejemplo
           build_context.py --target Aldric_Voss --max-words 1200
           build_context.py --index        (índice compacto de todas las entidades)"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (OPEN_QUESTIONS, calendar_summary, describe_expected, find_gaps, first,  # noqa: E402
                       format_year, index_vault, int_value, link_exists, load_calendars, load_index,
                       place_types, read_world, reference_calendar, split_note, strip_links)
from vault_lib import vault_path  # noqa: E402

REGION_PROPS = ("region", "region_padre", "ubicacion", "residencia", "ubicacion_actual", "lugar_nacimiento")
PLACE_TYPES = place_types()
MAX_NAMES = 120
MAX_ERAS = 12


def one_line(entry):
    relevance = entry["relevancia"] if entry["relevancia"] is not None else "?"
    summary = entry["resumen"] or "(sin resumen)"
    return f"- [[{entry['name']}]] · {entry['tipo']} · relevancia {relevance} — {summary}"


def region_chain(entry, by_name, seen=None):
    """Lugares que contienen a la entidad (regiones y asentamientos), subiendo por su región."""
    seen = seen if seen is not None else set()
    chain = []
    for prop in REGION_PROPS:
        for target in entry["relaciones"].get(prop, []):
            region = by_name.get(target.lower())
            if region and region["tipo"] in PLACE_TYPES and region["name"] not in seen:
                seen.add(region["name"])
                chain.append(region)
                chain += region_chain(region, by_name, seen)
    return chain


def mentions(vault, note_path, target):
    """Líneas del cuerpo de una nota que mencionan el enlace, legibles y recortadas."""
    _, body = split_note((vault / note_path).read_text(encoding="utf-8"))
    needle = f"[[{target.lower()}"
    lines = []
    for line in body:
        if needle in line.lower():
            raw = line.strip()
            clean = strip_links(raw)
            if raw.startswith("|"):
                # Fila de tabla: las celdas se unen con guiones en lugar de barras
                clean = " — ".join(cell.strip() for cell in clean.strip("|").split("|") if cell.strip())
            else:
                clean = clean.lstrip("-*> ").strip()
            lines.append(clean[:300] + ("…" if len(clean) > 300 else ""))
    return lines


def print_index(index):
    print(f"# Índice del mundo ({len(index)} entidades)\n")
    for entry in sorted(index, key=lambda e: (e["tipo"], -(e["relevancia"] or 0), e["name"])):
        print(one_line(entry))


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", help="Nombre de la entidad o del enlace pendiente")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--max-words", type=int, default=2000, help="Tope aproximado de palabras del paquete")
    parser.add_argument("--index", action="store_true", help="Imprime el índice compacto de todas las entidades (en un mundo grande es largo: para buscar, mejor search_vault.py)")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    index = load_index(vault)
    if args.index:
        print_index(index)
        return
    if not args.target:
        sys.exit("Error: indica --target o --index.")

    by_name = {e["name"].lower(): e for e in index}
    backlinks = defaultdict(list)
    for entry in index:
        for link in entry["enlaces"]:
            backlinks[link.lower()].append(entry)
    names, paths = index_vault(vault)
    world = read_world(vault)
    target = args.target.strip()
    key = target.lower()
    lines = [f"# Contexto para [[{target}]]", ""]

    # Objetivo: una entidad existente o un enlace pendiente
    entry = by_name.get(key)
    related = {}
    if entry:
        lines += ["## Entidad", one_line(entry)]
        for prop, targets in sorted(entry["relaciones"].items()):
            shown = ", ".join(f"[[{t}]]" + ("" if link_exists(t, names, paths) else " (pendiente)") for t in targets)
            lines.append(f"  - `{prop}`: {shown}")
        for link in entry["enlaces"]:
            if link.lower() in by_name:
                related[link.lower()] = by_name[link.lower()]
        for other in backlinks.get(key, []):
            related[other["name"].lower()] = other
    else:
        gaps, _ = find_gaps(vault)
        gap = next((g for g in gaps if g["link"].lower() == key), None)
        if not gap:
            sys.exit(f"Error: '{target}' no es una entidad ni un enlace pendiente de la bóveda.")
        lines += ["## Enlace pendiente", f"Tipo esperado: {describe_expected(gap)}", "", "Lo que dicen las notas que lo nombran:"]
        for occurrence in gap["occurrences"]:
            if occurrence["property"]:
                lines.append(f"- {occurrence['note']} — propiedad `{occurrence['property']}`")
        for note in sorted({o["note"] for o in gap["occurrences"]}):
            for mention in mentions(vault, note, target):
                lines.append(f"- {note}: «{mention}»")
        for other in backlinks.get(key, []):
            related[other["name"].lower()] = other
            for link in other["enlaces"]:
                if link.lower() in by_name and link.lower() != key:
                    related[link.lower()] = by_name[link.lower()]

    # Mundo
    lines += ["", "## Mundo",
              f"- Año actual: {world['ano_actual'] if world['ano_actual'] is not None else 'por definir'}",
              f"- Calendario: {world['calendario'] or 'por definir'}",
              f"- Foco: {world['foco'] or 'por definir'}"]
    # Calendario de referencia: las fechas del texto se escriben con sus nombres
    calendars = load_calendars(vault)
    reference = reference_calendar(calendars)
    if reference:
        lines.append(f"- Calendario de referencia: [[{reference['nombre']}]] (las fechas del texto, con sus nombres)")
        lines += [f"  {line}" for line in calendar_summary(reference, world["ano_actual"])]
    # Eras, en orden: dónde cae en la historia lo que se va a crear
    eras = [e for e in index if e["tipo"] == "era"]
    if eras:
        def year_text(value, missing):
            if value is None:
                return missing
            return format_year(reference, value) if reference else str(value)

        def era_line(era):
            start, end = (int_value(first(era["props"].get(k))) for k in ("inicio", "fin"))
            situation = first(era["props"].get("situacion"))
            tag = f", {situation}" if situation in ("legendaria", "profetizada") else ""
            return f"[[{era['name']}]] ({year_text(start, '?')} – {year_text(end, 'hoy' if situation == 'actual' else '?')}{tag})"

        ordered = sorted(eras, key=lambda e: (int_value(first(e["props"].get("inicio"))) is None,
                                              int_value(first(e["props"].get("inicio"))) or 0, e["name"]))
        lines.append("- Eras, de la más antigua a la más reciente: " + " · ".join(era_line(e) for e in ordered[:MAX_ERAS])
                     + (f" · … y {len(ordered) - MAX_ERAS} más" if len(ordered) > MAX_ERAS else ""))
    others = [c for c in calendars if c is not reference]
    if others:
        present = world["ano_actual"]
        lines.append("- Otros calendarios: " + " · ".join(
            f"[[{c['nombre']}]]" + (f" (año actual {format_year(c, present)})" if present is not None else "")
            for c in others))

    # Regiones que contienen al objetivo o a lo relacionado
    chain = []
    seen_regions = set()
    for item in ([entry] if entry else []) + list(related.values()):
        chain += region_chain(item, by_name, seen_regions)
    for region in chain:
        related.setdefault(region["name"].lower(), region)

    # Entidades relacionadas, por relevancia, hasta el tope de palabras
    related.pop(key, None)
    ranked = sorted(related.values(), key=lambda e: (-(e["relevancia"] or 2), e["name"]))
    lines += ["", "## Entidades relacionadas (por relevancia)"]
    budget = args.max_words - sum(len(l.split()) for l in lines)
    reserve = min(300, args.max_words // 4)  # sitio para los nombres usados y las preguntas abiertas
    shown_count = 0
    for item in ranked:
        line = one_line(item)
        if budget - len(line.split()) < reserve:
            break
        lines.append(line)
        budget -= len(line.split())
        shown_count += 1
    if shown_count < len(ranked):
        lines.append(f"- … y {len(ranked) - shown_count} más (pide su contexto si hace falta)")
    if not ranked:
        lines.append("- Ninguna todavía.")

    # Nombres ya usados: los relacionados primero, luego el resto por relevancia
    used = []
    for item in ranked + sorted(index, key=lambda e: -(e["relevancia"] or 2)):
        for name in [item["titulo"]] + item["aliases"]:
            if name and name not in used:
                used.append(name)
    lines += ["", "## Nombres ya usados (no los repitas)", ", ".join(used[:MAX_NAMES]) or "Ninguno todavía."]

    # Preguntas abiertas que tocan al objetivo o a lo relacionado
    questions_path = vault / OPEN_QUESTIONS
    keys = {key} | set(related)
    open_lines = []
    if questions_path.is_file():
        for line in questions_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("- [ ]") and any(f"[[{k}" in line.lower() for k in keys):
                open_lines.append(line.strip())
    lines += ["", "## Preguntas abiertas relacionadas"] + (open_lines or ["- Ninguna."])
    print("\n".join(lines))


if __name__ == "__main__":
    main()
