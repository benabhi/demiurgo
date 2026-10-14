#!/usr/bin/env python3
"""El cierre del mundo: lo que falta para cerrarlo, los cambios de estado y lo que se cierra por el camino.

  status        La lista del cierre (sin orden, esto): qué falta de cada criterio y lo siguiente que toca. El mundo
                se cierra con todo en verde:
                  - pilares: ninguno «Por definir» (decididos, o sin definir a propósito: un misterio);
                  - preguntas: ninguna abierta (confirmada, rechazada, respondida o misterio);
                  - enlaces pendientes: ninguno (lo de fuera de un mundo que es una ciudad o una región no cuenta);
                  - borradores: ninguno (todo pasó por revisar-mundo);
                  - notas impecables: todas pasan check_note sin errores ni avisos, y ninguna (ni el Glosario) tiene
                    anotaciones de trabajo («por definir», «por confirmar», «sin cartografiar», restos de plantilla);
                  - el auditor, sin errores ni avisos;
                  - imágenes: toda entidad tiene la suya (los secretos no llevan);
                  - mapas: dibujados y al día, sin un solo cambio por dibujar, y lo más alto del mapa con el suyo;
                  - ni imágenes sueltas en 02_Activos (las que ninguna nota usa) ni notas en la Bandeja de Entrada.
  start         Abre el cierre: el mundo pasa a «en cierre» (ya no crece, y ninguna nota abre enlaces pendientes
                nuevos).
  close         Cierra el mundo si la lista está toda en verde: «cerrado» (no se crea nada; se puede consultar,
                narrar e ilustrar).
  reopen        Lo reabre («abierto»), con --reason.
  resolve TEXTO ESTADO [--note NOTA]
                Cierra la pregunta abierta que contiene TEXTO: confirmado, rechazado, respondida o misterio. Un pilar
                por definir que queda como misterio pasa a «Sin definir, a propósito» en la Ficha.
  tidy          Aparta a 02_Activos/Anteriores, con `_suelta`, las imágenes que ninguna nota usa.

Cada cambio de estado deja su línea en el Registro de Canon y su entrada en la Bitácora, y rehace las Estadísticas.

Ejemplos:  close_world.py
           close_world.py start
           close_world.py resolve "por qué la niebla se detiene" misterio --note "nadie lo sabe, y así queda"
           close_world.py close"""
import argparse
import datetime
import re
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]
# La lógica común vive en los scripts de crear-entidad
sys.path.insert(0, str(SKILLS / "crear-entidad" / "scripts"))
from health import (Health, drafts, inbox, loose_images, map_states, missing_images,  # noqa: E402
                    open_questions, pending, tidy_images, undefined_pillars, work_notes)
from map_key import frontmatter_end, set_property  # noqa: E402
from vault_lib import (CANON_LOG, OPEN_QUESTIONS, SECRET_TYPE, STATS_NOTE, WORLD_CLOSED, WORLD_CLOSING,  # noqa: E402
                       WORLD_OPEN, WORLD_SHEET, add_canon_log, add_chronicle_entry, load_index, normalize,
                       strip_links, world_state)
from vault_lib import vault_path  # noqa: E402
from world_stats import write_stats  # noqa: E402

UNDEFINED = "Por definir."
MYSTERY_PILLAR = "Sin definir, a propósito."
RESOLUTIONS = ("confirmado", "rechazado", "respondida", "misterio")
STATE_TEXT = {WORLD_OPEN: "abierto", WORLD_CLOSING: "en cierre", WORLD_CLOSED: "cerrado"}
MAX_SHOWN = 8


def listed(items, limit=MAX_SHOWN):
    return ", ".join(items[:limit]) + (f" y {len(items) - limit} más" if len(items) > limit else "")


def diagnose(vault):
    """Cada criterio del cierre: (nombre, cumplido, detalle), con las comprobaciones comunes (health.py) en su
    nivel estricto."""
    health = Health(vault)
    rows = []

    pillars = undefined_pillars(vault)
    rows.append(("Pilares por definir", not pillars, listed(pillars) or "ninguno"))

    questions = open_questions(vault)
    confirmations = [q for q in questions if q[1]]
    shown = [strip_links(q[0][6:])[:70] for q in questions]
    rows.append(("Preguntas abiertas", not questions,
                 f"{len(questions)} ({len(confirmations)} confirmaciones)" + (f": {listed(shown, 3)}" if shown else "")
                 if questions else "ninguna"))

    links = pending(health)
    gaps, minor = links["all"], [g["link"] for g in links["minor"]]
    detail = (f"{len(gaps)}: {len(links['ready'])} se pueden crear, {len(links['waiting'])} esperan una confirmación, "
              f"{len(links['untyped'])} sin tipo, {len(links['no_module'])} sin módulo"
              + (f"; menores, para proponer disolverlos ({len(minor)}): {listed([m.replace('_', ' ') for m in minor])}"
                 if minor else "")) if gaps else "ninguno"
    rows.append(("Enlaces pendientes", not gaps, detail))

    unrevised = drafts(health)
    rows.append(("Borradores", not unrevised,
                 f"{len(unrevised)} ({sum(1 for e in unrevised if e['origen'] == 'procedural')} del motor)"
                 if unrevised else "ninguno"))

    flawed = [f"{entry['name']} ({len(errors)} errores, {len(warnings)} avisos)"
              for entry, errors, warnings in health.note_checks() if errors or warnings]
    annotated = [f"{name} ({', '.join(labels)})" for name, labels in work_notes(health)]
    rows.append(("Notas impecables", not flawed and not annotated,
                 "; ".join(part for part in (f"check_note: {listed(flawed, 4)}" if flawed else "",
                                             f"anotaciones de trabajo: {listed(annotated, 4)}" if annotated else "")
                           if part) or "todas"))

    audit = health.audit()
    rows.append(("Auditor", not audit["errores"] and not audit["avisos"],
                 f"{len(audit['errores'])} errores, {len(audit['avisos'])} avisos"))

    missing = missing_images(health)
    rows.append(("Imágenes", not missing, f"faltan {len(missing)}: {listed(missing)}" if missing else "todas"))

    stale, tops = map_states(health, complete=True)
    rows.append(("Mapas al día", not stale,
                 f"{len(stale)}: {listed([f'{name} ({why})' for name, why in stale], 4)}" if stale else "todos"))
    unmapped = [f"{name} ({'sin dibujar' if rule else 'no le toca mapa por su categoría o su relevancia'})"
                for name, edition, rule in tops if not edition]
    rows.append(("Lo más alto del mapa", bool(tops) and not unmapped,
                 (listed(unmapped) if unmapped else listed([f"{n} (edición {e})" for n, e, _ in tops]))
                 if tops else "ningún lugar todavía"))

    orphans = loose_images(vault)
    rows.append(("Imágenes sueltas", not orphans,
                 f"{len(orphans)}: {listed([p.name for p in orphans], 5)} (tidy las aparta)" if orphans else "ninguna"))
    box = inbox(vault)
    rows.append(("Bandeja de Entrada", not box, f"{len(box)}: {listed(box, 5)}" if box else "vacía"))
    return rows, health.world


NEXT = [("Pilares por definir", "decidir los pilares por definir con el usuario, o dejarlos como misterio"),
        ("Preguntas abiertas", "resolver las confirmaciones y las preguntas: confirmar, rechazar, responder o misterio"),
        ("Enlaces pendientes", "cerrar los enlaces pendientes: disolver los menores que el usuario apruebe, crear el "
                               "resto (el motor, en cierre, solo completa), dar tipo a los que no tienen y fusionar los "
                               "que son otro nombre"),
        ("Borradores", "revisar los borradores con /revisar-mundo"),
        ("Notas impecables", "corregir las notas que no pasan check_note o tienen anotaciones de trabajo"),
        ("Auditor", "resolver lo que señala el auditor (audit_world.py)"),
        ("Imágenes", "generar las imágenes que faltan (/generar-imagen)"),
        ("Mapas al día", "dibujar los mapas que faltan o están atrasados (/generar-imagen <Nota> mapa)"),
        ("Lo más alto del mapa", "dibujar el mapa de lo más alto del mapa"),
        ("Imágenes sueltas", "apartar las imágenes sueltas (close_world.py tidy)"),
        ("Bandeja de Entrada", "procesar la Bandeja de Entrada: lo que sirve, a su nota; lo demás, al archivo")]


def status(vault, quiet=False):
    rows, world = diagnose(vault)
    state = world_state(vault)
    if not quiet:
        print(f"Mundo: {world['props'].get('mundo') or '(sin nombre)'} · estado: {STATE_TEXT[state]}")
        print("Para cerrar el mundo:")
        for name, ok, detail in rows:
            print(f"  {'✓' if ok else '✗'} {name}: {detail}")
        pending = [name for name, ok, _ in rows if not ok]
        if state == WORLD_OPEN:
            print("Lo siguiente: empezar el cierre (close_world.py start).")
        elif state == WORLD_CLOSED:
            print("El mundo está cerrado.")
        elif pending:
            print("Lo siguiente: " + next(text for name, text in NEXT if name == pending[0]) + ".")
        else:
            print("Todo en verde: se puede cerrar (close_world.py close).")
    return rows, world, state


def closing_summary(vault):
    """Lo que hizo el cierre, desde que empezó: lo decidido en el Registro de Canon (pasó a canon, se archivó, se
    quitó, se disolvió) y las preguntas cerradas (confirmadas, rechazadas, respondidas, misterios)."""
    rows = [line for line in (vault / CANON_LOG).read_text(encoding="utf-8").splitlines() if line.startswith("| 2")] \
        if (vault / CANON_LOG).is_file() else []
    start = next((i for i, row in enumerate(rows) if "El mundo entra en cierre" in row), None)
    if start is None:
        return []
    since = rows[start].split("|")[1].strip()
    changes = [row.split("|")[3].strip() for row in rows[:start]]
    counts = [(("pasó a canon", "pasaron a canon"), sum(1 for c in changes if c.startswith("Pasa a canon"))),
              (("se archivó para rehacerla", "se archivaron para rehacerlas"),
               sum(1 for c in changes if c.startswith("Archivada"))),
              (("se quitó del mundo", "se quitaron del mundo"), sum(1 for c in changes if c.startswith("Quitada"))),
              (("enlace pendiente se disolvió", "enlaces pendientes se disolvieron"),
               sum(1 for c in changes if c.startswith("Disuelto")))]
    questions = (vault / OPEN_QUESTIONS).read_text(encoding="utf-8") if (vault / OPEN_QUESTIONS).is_file() else ""
    closed = re.findall(r"^\s*-\s*\[x\].*? — (confirmado|rechazado|respondida|misterio) \((\d{4}-\d{2}-\d{2})\)",
                        questions, re.MULTILINE)
    outcomes = [o for o, day in closed if day >= since]
    lines = [f"- **El cierre** (desde el {since}): "
             + (", ".join(f"{n} {what[0] if n == 1 else what[1]}" for what, n in counts if n) or "nada") + "."]
    if outcomes:
        lines.append("- **Preguntas cerradas:** " + ", ".join(
            f"{outcomes.count(o)} {one if outcomes.count(o) == 1 else many}"
            for o, one, many in (("confirmado", "confirmada", "confirmadas"), ("rechazado", "rechazada", "rechazadas"),
                                 ("respondida", "respondida", "respondidas"), ("misterio", "misterio", "misterios"))
            if outcomes.count(o)) + ".")
    return lines


def world_summary(vault):
    """El resumen del mundo de sus Estadísticas: su sección Resumen y la tabla por tipo."""
    path = vault / STATS_NOTE
    if not path.is_file():
        return []
    lines, keep = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            keep = line[3:].strip() in ("Resumen", "Por tipo")
            continue
        if keep and line.strip():
            lines.append(line)
    return lines


def set_state(vault, value):
    path = vault / WORLD_SHEET
    lines = path.read_text(encoding="utf-8").splitlines()
    end = frontmatter_end(lines)
    set_property(lines, end, "estado_mundo", value)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def record(vault, today, change, why, title, lines):
    add_canon_log(vault, [f"| {today} | [[Ficha_del_Mundo]] | {change} | {why} |"])
    add_chronicle_entry(vault, title, lines, today)
    write_stats(vault, today)


def resolve(vault, text, outcome, note, today):
    path = vault / OPEN_QUESTIONS
    lines = path.read_text(encoding="utf-8").splitlines()
    wanted = normalize(text)
    matches = [i for i, line in enumerate(lines) if re.match(r"^\s*-\s*\[ \]", line) and wanted in normalize(line)]
    if len(matches) != 1:
        sys.exit(f"Error: «{text}» coincide con {len(matches)} preguntas abiertas; precisa más el texto.")
    i = matches[0]
    question = lines[i]
    lines[i] = question.replace("[ ]", "[x]", 1).rstrip() + f" — {outcome} ({today})" + (f": {note}" if note else "")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Cerrada ({outcome}): {question.strip()[6:]}")
    pillar = question.strip()[6:].strip()
    if outcome == "misterio" and pillar in undefined_pillars(vault):
        sheet = vault / WORLD_SHEET
        content = sheet.read_text(encoding="utf-8").replace(f"- **{pillar}:** {UNDEFINED}",
                                                            f"- **{pillar}:** {MYSTERY_PILLAR}", 1)
        sheet.write_text(content, encoding="utf-8", newline="\n")
        print(f"La Ficha: «{pillar}» queda sin definir, a propósito.")


def tidy(vault):
    print("\n".join(tidy_images(vault)))


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status", help="La lista del cierre")
    sub.add_parser("start", help="Abre el cierre")
    sub.add_parser("close", help="Cierra el mundo, si todo está en verde")
    reopen = sub.add_parser("reopen", help="Reabre el mundo")
    reopen.add_argument("--reason", default="", help="Por qué se reabre")
    res = sub.add_parser("resolve", help="Cierra una pregunta abierta")
    res.add_argument("text", help="Un trozo del texto de la pregunta")
    res.add_argument("outcome", choices=RESOLUTIONS, help="Cómo se cierra")
    res.add_argument("--note", default="", help="Una línea: lo que se decidió, o por qué queda como misterio")
    sub.add_parser("tidy", help="Aparta las imágenes sueltas")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    today = datetime.date.today().isoformat()
    command = args.command or "status"
    state = world_state(vault)
    if command == "status":
        status(vault)
    elif command == "start":
        if state != WORLD_OPEN:
            sys.exit(f"El mundo ya está {STATE_TEXT[state]}.")
        rows, world, _ = status(vault, quiet=True)
        set_state(vault, WORLD_CLOSING)
        missing = [f"{name.lower()}: {detail}" for name, ok, detail in rows if not ok]
        record(vault, today, "El mundo entra en cierre", "finalizar-mundo", "El mundo entra en cierre",
               ["- **Desde hoy** el mundo ya no crece: solo se cierran cabos, y ninguna nota abre enlaces pendientes "
                "nuevos.", f"- **Lo que falta:** {'; '.join(missing[:4]) or 'nada'}."])
        print("El mundo está en cierre. Lo que falta:")
        status(vault)
    elif command == "close":
        if state == WORLD_CLOSED:
            sys.exit("El mundo ya está cerrado.")
        rows, world, _ = status(vault)
        if any(not ok for _, ok, _ in rows):
            sys.exit("No se cierra: hay criterios en rojo.")
        set_state(vault, WORLD_CLOSED)
        index = load_index(vault)
        name = world["props"].get("mundo") or "el mundo"
        done = closing_summary(vault)
        record(vault, today, "El mundo se cierra", "finalizar-mundo: todo en verde", f"Se cerró «{name}»",
               [f"- **El mundo, terminado:** {len([e for e in index if e['tipo'] != SECRET_TYPE])} entidades y "
                f"{sum(1 for e in index if e['tipo'] == SECRET_TYPE)} secretos, todo en canon; sin enlaces pendientes, "
                f"sin preguntas abiertas, con sus imágenes y sus mapas.", *done,
                "- **Desde hoy** no se crea nada: se puede consultar, narrar e ilustrar."])
        print(f"«{name}» está cerrado.")
        print("\nEl mundo terminado (de sus Estadísticas):")
        print("\n".join(world_summary(vault)))
        if done:
            print("\nLo que hizo el cierre:")
            print("\n".join(done))
    elif command == "reopen":
        if state == WORLD_OPEN:
            sys.exit("El mundo ya está abierto.")
        set_state(vault, WORLD_OPEN)
        why = args.reason.strip() or "a pedido del usuario"
        record(vault, today, "Se reabre el mundo", why, "Se reabrió el mundo", [f"- **Por qué:** {why}."])
        print("El mundo está abierto otra vez.")
    elif command == "resolve":
        resolve(vault, args.text, args.outcome, args.note.strip(), today)
    else:
        tidy(vault)


if __name__ == "__main__":
    main()
