#!/usr/bin/env python3
"""Las estadísticas del mundo en una nota de la bóveda (`00_Sistema/Estadisticas.md`), para ver de un vistazo
cuánto hay y qué falta:
  - las entidades, por tipo, por estado y por relevancia, y los secretos y las notas archivadas;
  - los enlaces pendientes: los que se pueden crear ya, los que esperan una confirmación y los que no tienen
    tipo, y los más nombrados;
  - las imágenes, los mapas (su edición, lo que falta por cartografiar y si toca redibujarlos), el Glosario,
    las preguntas abiertas, las entidades huérfanas y las más enlazadas.

La nota se rehace entera cada vez y no se edita a mano: la reescriben `report.py --log` y `log_entry.py` al
terminar cada tarea, junto con la Bitácora. Las cifras principales van también en su frontmatter, para que un
tablero (Bases, Dataview o el que venga) las lea sin abrirla. La IA no necesita leerla: para saber cuánto hay,
`world_stats.py --print`.

Ejemplos:  world_stats.py   world_stats.py --print"""
import argparse
import datetime
import sys
from collections import Counter, defaultdict
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (ARCHIVED_FOLDER, HOME_MOC, NARRATIVE_FOLDER, OPEN_QUESTIONS, OUTSIDE_TYPE, PENDING_NOTE,  # noqa: E402
                       SECRET_TYPE, world_state,
                       SECRETS_FOLDER, STATS_HOME_LINE, STATS_NOTE, blocked_links, find_gaps, gap_kind,
                       glossary_table, is_confirmation, load_index, load_modules, map_applies, map_status,
                       parse_map_key, parse_map_routes, split_note)
from vault_lib import vault_path  # noqa: E402

TOP = 10
STATE_LABELS = {"abierto": "abierto", "en_cierre": "en cierre (`/finalizar-mundo`): solo se cierran cabos",
                "cerrado": "cerrado: no se crea nada"}


def plural(count, singular, plural_form=None):
    return f"{count} {singular if count == 1 else plural_form or singular + 's'}"


def decimal(value):
    """Un decimal a la española: 2,5."""
    return f"{value:.1f}".replace(".", ",")


def wiki(entry, in_table=False):
    """Enlace de Obsidian a la entidad, con su nombre legible (en una tabla, la barra va escapada)."""
    title = entry["titulo"] or entry["name"].replace("_", " ")
    bar = "\\|" if in_table else "|"
    return f"[[{entry['name']}{bar}{title}]]" if title != entry["name"] else f"[[{entry['name']}]]"


def collect(vault):
    """Las cifras del mundo, en un diccionario."""
    modules = load_modules()
    index = load_index(vault)
    secrets = [e for e in index if e["tipo"] == SECRET_TYPE]
    entities = [e for e in index if e["tipo"] != SECRET_TYPE]
    archive = vault / ARCHIVED_FOLDER
    archived = [p for p in archive.rglob("*.md") if p.name != "README.md"] if archive.is_dir() else []
    stories = vault / NARRATIVE_FOLDER
    narratives = [p for p in stories.rglob("*.md") if p.name != "README.md" and not p.name.startswith("MOC_")] \
        if stories.is_dir() else []
    gaps, _ = find_gaps(vault)
    blocked = blocked_links(vault)
    ready = sorted((g for g in gaps if g["expected_modules"] and g["link"].lower() not in blocked),
                   key=lambda g: (-len(g["notes"]), g["link"].lower()))
    waiting = [g for g in gaps if g["link"].lower() in blocked]
    untyped = [g for g in gaps if not g["expected_type"]]
    outside = [g for g in gaps if g["expected_type"] == OUTSIDE_TYPE]
    # Quién enlaza a quién, sin contar los secretos (solo enlazan hacia fuera)
    linkers = defaultdict(set)
    for entry in entities:
        for target in entry["enlaces"]:
            if target.lower() != entry["name"].lower():
                linkers[target.lower()].add(entry["name"])
    maps = []
    for entry in entities:
        module = modules.get(entry["tipo"])
        if not module or not module.get("mapa") or not map_applies(module, entry["props"], entry["relevancia"]):
            continue
        _, body = split_note((vault / entry["path"]).read_text(encoding="utf-8"))
        zones, _ = parse_map_key(body)
        routes, _ = parse_map_routes(body)
        maps.append((entry, map_status(module, entry["props"], zones or [], entry["relevancia"], routes)))
    questions_path = vault / OPEN_QUESTIONS
    questions = [line.strip() for line in questions_path.read_text(encoding="utf-8").splitlines()
                 if line.strip().startswith("- [ ]")] if questions_path.is_file() else []
    return {"modules": modules, "entities": entities, "secrets": secrets, "archived": archived,
            "narratives": narratives, "gaps": gaps, "state": world_state(vault),
            "ready": ready, "waiting": waiting, "untyped": untyped, "outside": outside, "linkers": linkers,
            "maps": maps,
            "glossary": glossary_table(vault), "questions": questions, "registry": (vault / PENDING_NOTE).is_file(),
            "confirmations": [q for q in questions if is_confirmation(q)]}


def build_note(data, today):
    """El texto de la nota de estadísticas."""
    entities, maps = data["entities"], data["maps"]
    drafts = sum(1 for e in entities if e["estado"] == "borrador")
    canon = sum(1 for e in entities if e["estado"] == "canon")
    with_image = [e for e in entities if e["relaciones"].get("imagen")]
    orphans = [e for e in entities if not data["linkers"].get(e["name"].lower())]
    to_draw = [(e, s) for e, s in maps if s["toca"]]
    relevances = [e["relevancia"] for e in entities if e["relevancia"] is not None]
    by_type = defaultdict(list)
    for entry in entities:
        by_type[entry["tipo"]].append(entry)

    numbers = {"estado_mundo": data["state"], "entidades": len(entities), "borradores": drafts, "canon": canon,
               "secretos": len(data["secrets"]),
               "archivadas": len(data["archived"]), "narraciones": len(data["narratives"]),
               "enlaces_pendientes": len(data["gaps"]),
               "pendientes_listos": len(data["ready"]), "pendientes_por_confirmar": len(data["waiting"]),
               "con_imagen": len(with_image), "mapas": len(maps), "mapas_por_dibujar": len(to_draw),
               "terminos_glosario": len(data["glossary"]), "preguntas_abiertas": len(data["questions"]),
               "huerfanas": len(orphans)}
    lines = ["---", "tipo: meta", f"actualizado: {today}"] + [f"{k}: {v}" for k, v in numbers.items()] + ["---", ""]
    lines += ["# Estadísticas del mundo", "",
              "> Cuánto hay en el mundo y qué falta. Las skills la rehacen al terminar cada tarea (`world_stats.py`): "
              "no la edites a mano.", "", f"*Actualizada el {today}.*", "", "## Resumen"]
    lines.append(f"- **Estado del mundo:** {STATE_LABELS.get(data['state'], data['state'])}")
    lines.append(f"- **Entidades:** {len(entities)}"
                 + (f", de {plural(len(by_type), 'tipo')} · {drafts} en borrador y {canon} en canon"
                    + (f" · relevancia media {decimal(sum(relevances) / len(relevances))}" if relevances else "")
                    if entities else ""))
    lines.append(f"- **Secretos:** {len(data['secrets'])} (en `{SECRETS_FOLDER}`) · "
                 f"**archivadas:** {len(data['archived'])} (en `{ARCHIVED_FOLDER}`)"
                 + (f" · **narraciones:** {len(data['narratives'])} (en `{NARRATIVE_FOLDER}`)"
                    if data["narratives"] else ""))
    density = len(data["ready"]) / max(len(entities), 1)
    lines.append(f"- **Enlaces pendientes:** {len(data['gaps'])} · {len(data['ready'])} se pueden crear ya "
                 f"({decimal(density)} por entidad), {len(data['waiting'])} "
                 f"{'espera' if len(data['waiting']) == 1 else 'esperan'} una confirmación tuya y "
                 f"{len(data['untyped'])} {'no tiene' if len(data['untyped']) == 1 else 'no tienen'} tipo"
                 + (f" · {len(data['outside'])} de fuera del mundo (referencias que no se crean)"
                    if data["outside"] else "")
                 + (f" · todos en [[{Path(PENDING_NOTE).stem}|Enlaces pendientes]]" if data["registry"] else ""))
    lines.append(f"- **Imágenes:** {len(with_image)} de {plural(len(entities), 'entidad', 'entidades')}")
    lines.append(f"- **Mapas:** {plural(len(maps), 'lugar', 'lugares')} con mapa · "
                 + (f"{len(to_draw)} por dibujar o redibujar" if to_draw else "ninguno por dibujar"))
    lines.append(f"- **Glosario:** {plural(len(data['glossary']), 'término')} · **Preguntas abiertas:** "
                 f"{len(data['questions'])} ({plural(len(data['confirmations']), 'confirmación', 'confirmaciones')})")
    lines.append(f"- **Huérfanas** (ninguna entidad las enlaza): {len(orphans)}"
                 + (": " + ", ".join(wiki(e) for e in orphans[:TOP])
                    + (f" y {len(orphans) - TOP} más" if len(orphans) > TOP else "") if orphans else ""))

    lines += ["", "## Por tipo"]
    if by_type:
        lines += ["| Tipo | Entidades | Borradores | Canon | Relevancia media | Con imagen |", "|---|---|---|---|---|---|"]
        for tipo, group in sorted(by_type.items(), key=lambda item: (-len(item[1]), item[0])):
            emoji = data["modules"].get(tipo, {}).get("emoji", "")
            values = [e["relevancia"] for e in group if e["relevancia"] is not None]
            lines.append(f"| {emoji} {tipo} | {len(group)} | {sum(1 for e in group if e['estado'] == 'borrador')} | "
                         f"{sum(1 for e in group if e['estado'] == 'canon')} | "
                         f"{decimal(sum(values) / len(values)) if values else '—'} | "
                         f"{sum(1 for e in group if e['relaciones'].get('imagen'))} |")
        counts = Counter(relevances)
        lines += ["", "**Por relevancia:** " + " · ".join(f"{n}: {counts.get(n, 0)}" for n in range(5, 0, -1))]
    else:
        lines.append("- Ninguna entidad todavía.")

    lines += ["", "## Mapas"]
    if maps:
        lines += ["| Lugar | Mapa | Edición | Zonas | Sin cartografiar | ¿Dibujar? |", "|---|---|---|---|---|---|"]
        for entry, status in sorted(maps, key=lambda item: (not item[1]["toca"], item[0]["name"].lower())):
            missing = [part for part in (plural(status["sin_cartografiar"], "zona") if status["sin_cartografiar"] else "",
                                         plural(status["rutas_sin_cartografiar"], "ruta")
                                         if status["rutas_sin_cartografiar"] else "",
                                         f"{plural(status['por_quitar'], 'zona')} por quitar"
                                         if status.get("por_quitar") else "") if part]
            draw = {"primera": "sí, la primera", "nueva": "sí, una edición nueva"}.get(status["toca"], "no")
            lines.append(f"| {wiki(entry, in_table=True)} | {status['clase']} | {status['edicion'] or '—'} | "
                         f"{status['zonas']} | {', '.join(missing) or '—'} | {draw} |")
    else:
        lines.append("- Ningún lugar con mapa todavía.")

    lines += ["", "## Lo más nombrado que falta"]
    if data["ready"]:
        lines += ["| Enlace pendiente | Tipo | Notas que lo nombran |", "|---|---|---|"]
        lines += [f"| {g['link'].replace('_', ' ')} | {gap_kind(g)} | {len(g['notes'])} |" for g in data["ready"][:TOP]]
    else:
        lines.append("- Nada que se pueda crear ya.")

    lines += ["", "## Lo más enlazado"]
    linked = sorted((e for e in entities if data["linkers"].get(e["name"].lower())),
                    key=lambda e: (-len(data["linkers"][e["name"].lower()]), e["name"].lower()))
    if linked:
        lines += ["| Entidad | Tipo | Notas que la enlazan |", "|---|---|---|"]
        lines += [f"| {wiki(e, in_table=True)} | {e['tipo']} | {len(data['linkers'][e['name'].lower()])} |"
                  for e in linked[:TOP]]
    else:
        lines.append("- Ninguna todavía.")
    return "\n".join(lines) + "\n", numbers


def link_from_home(vault):
    """Enlaza las Estadísticas desde MOC_Inicio, tras la Bitácora, si aún no lo están. Devuelve los avisos."""
    home = vault / HOME_MOC
    if not home.is_file():
        return []
    rows = home.read_text(encoding="utf-8").splitlines()
    if any("[[Estadisticas" in row for row in rows):
        return []
    anchor = next((i for i, row in enumerate(rows) if "[[Bitacora" in row), None)
    if anchor is None:
        anchor = next((i for i, row in enumerate(rows) if "[[Preguntas_Abiertas" in row), None)
    if anchor is None:
        return [f"no encuentro dónde enlazar las Estadísticas en MOC_Inicio; añádelo a mano: {STATS_HOME_LINE}"]
    rows.insert(anchor + 1, STATS_HOME_LINE)
    home.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    return []


def write_stats(vault, today=None):
    """Rehace la nota de estadísticas. Devuelve (cifras principales, avisos)."""
    text, numbers = build_note(collect(vault), today or datetime.date.today().isoformat())
    path = vault / STATS_NOTE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return numbers, link_from_home(vault)


def summary(numbers):
    """Una línea con lo esencial, para la salida de los scripts."""
    return (f"Estadísticas: {numbers['entidades']} entidades ({numbers['borradores']} en borrador), "
            f"{numbers['enlaces_pendientes']} enlaces pendientes, {numbers['con_imagen']} con imagen, "
            f"{numbers['mapas']} con mapa · en {STATS_NOTE}.")


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--print", action="store_true", help="Solo muestra las estadísticas, sin escribir la nota")
    args = parser.parse_args()
    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    if args.print:
        text, _ = build_note(collect(vault), datetime.date.today().isoformat())
        print(text.split("---", 2)[2].strip())
        return
    numbers, warnings = write_stats(vault)
    print(summary(numbers))
    for warning in warnings:
        print(f"AVISO: {warning}")


if __name__ == "__main__":
    main()
