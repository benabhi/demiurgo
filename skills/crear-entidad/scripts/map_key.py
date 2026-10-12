#!/usr/bin/env python3
"""Muestra y mantiene la leyenda del mapa de un lugar (su sección Mapa) sin leer la nota entera.

El mapa de un lugar es su leyenda numerada; la imagen es una edición de esa leyenda. Los números
son estables: solo se añaden al final, nunca se renumeran ni se reutilizan.

Sin opciones, muestra la leyenda y su estado: si al lugar le toca mapa (por su categoría y su
relevancia), la edición, las zonas sin cartografiar y si toca dibujar la primera edición o una nueva.

  --add NOMBRE --position ORIENTACIÓN [--level N] --desc TEXTO [--connects 2,5]
      Añade una zona al final de la leyenda. NOMBRE es texto («la plaza de las cenizas») o un enlace
      («[[Torre_Hendida|La torre hendida]]»). Las conexiones se anotan en las dos zonas. Si el lugar
      ya tiene mapa, la zona queda «sin cartografiar» hasta la edición siguiente. Si el enlace ya está
      en la leyenda, no hace nada; si su nivel ya tiene 12 zonas, no la añade y sale con código 3.
  --charted
      Tras dibujar una edición: suma una a `mapa_edicion`, pone `mapa_zonas` en el último número y
      quita las marcas «sin cartografiar».

Ejemplos:  map_key.py Puerto_Gris
           map_key.py Puerto_Gris --json
           map_key.py Puerto_Gris --add "[[Torre_Hendida|La torre hendida]]" --position noreste --desc "Vigía sobre el río." --connects 5
           map_key.py Cripta_Honda --add "las celdas" --position oeste --level 2 --desc "Cuatro celdas con rejas." --connects 9
           map_key.py Puerto_Gris --charted"""
import argparse
import json
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (CONNECTS_RE, KEY_LINE_RE, LINK_RE, MAP_ITEM_EMPTY_RE, MAP_SECTION, MAX_MARKERS,  # noqa: E402
                       ORIENTATION_SYNONYMS, ORIENTATIONS, UNCHARTED_MARK, first, format_connections,
                       int_value, load_modules, map_key_problems, map_status, normalize, parse_frontmatter,
                       parse_map_key, resolve_note, zones_per_level)

EXIT_FULL = 3


def frontmatter_end(lines):
    """Índice de la línea `---` que cierra el frontmatter, o None."""
    if not lines or lines[0].strip() != "---":
        return None
    return next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)


def set_property(lines, end, key, value):
    """Pone un valor escalar en una propiedad del frontmatter; si la nota no la tiene, la añade al
    final del frontmatter. Devuelve el nuevo índice del cierre del frontmatter."""
    for i in range(1, end):
        match = KEY_LINE_RE.match(lines[i])
        if match and match.group(1) == key:
            lines[i] = f"{key}: {value}"
            return end
    lines.insert(end, f"{key}: {value}")
    return end + 1


def section_start(lines, end):
    """Índice de la línea `## Mapa` en la nota, o None."""
    return next((i for i in range(end + 1, len(lines)) if lines[i].strip() == f"## {MAP_SECTION}"), None)


def add_connection(line, number):
    """La línea de una zona con `number` añadido a sus conexiones."""
    match = CONNECTS_RE.search(line)
    if match:
        current = [int(n) for n in re.findall(r"\d+", match.group(1))]
        return line[:match.start()] + format_connections(current + [number]) + line[match.end():]
    phrase = format_connections([number])
    if UNCHARTED_MARK in line:
        return line.replace(UNCHARTED_MARK, f"{phrase} {UNCHARTED_MARK}")
    return f"{line.rstrip()} {phrase}"


def show(path, status, zones, problems, as_json):
    if as_json:
        print(json.dumps({"nota": path.stem, **status, "leyenda": zones or [], "problemas": problems},
                         ensure_ascii=False, indent=2))
        return
    print(f"Mapa de {path.stem}")
    if not status["aplica"]:
        print("  No le toca mapa por su categoría y su relevancia.")
    else:
        print(f"  Clase: {status['clase']} · edición: {status['edicion'] or 'ninguna'} · zonas: {status['zonas']}"
              + (f" ({status['sin_cartografiar']} sin cartografiar)" if status["edicion"] else ""))
        if status["toca"] == "primera":
            print(f"  TOCA DIBUJAR la primera edición (niveles: {', '.join(map(str, status['niveles']))}).")
        elif status["toca"] == "nueva":
            print(f"  TOCA DIBUJAR una edición nueva: {status['razon']} (niveles: "
                  f"{', '.join(map(str, status['niveles']))}).")
        elif status["razon"]:
            print(f"  Aún no toca dibujar: {status['razon']}.")
    if zones is None:
        print("  La nota no tiene sección Mapa.")
        return
    levels = len(zones_per_level(zones)) > 1
    for zone in zones:
        where = (f"nivel {zone['nivel']}, " if levels else "") + zone["orientacion"]
        extra = " · sin cartografiar" if zone["sin_cartografiar"] else ""
        link = f" → [[{zone['enlace']}]]" if zone["enlace"] else ""
        connects = f" · conecta con {', '.join(map(str, zone['conecta']))}" if zone["conecta"] else ""
        print(f"  {zone['numero']:>2}. {zone['nombre']}{link} · {where}{connects}{extra}")
    for problem in problems:
        print(f"  ERROR: {problem}")


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("note", help="Nombre o ruta de la nota del lugar")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    parser.add_argument("--add", metavar="NOMBRE", help="Añade una zona al final de la leyenda")
    parser.add_argument("--position", help="Orientación de la zona nueva: " + ", ".join(ORIENTATIONS))
    parser.add_argument("--level", type=int, default=1, help="Nivel de la zona nueva, en una mazmorra (1)")
    parser.add_argument("--desc", default="", help="Una línea que la defina")
    parser.add_argument("--connects", default="", help="Zonas con las que conecta: 2,5")
    parser.add_argument("--charted", action="store_true", help="Marca la leyenda como cartografiada tras una edición")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    path = resolve_note(args.note, vault)
    if not path:
        sys.exit(f"Error: no encuentro la nota '{args.note}' (o hay varias con ese nombre).")
    lines = path.read_text(encoding="utf-8").splitlines()
    end = frontmatter_end(lines)
    if end is None:
        sys.exit(f"Error: {path.name} no tiene frontmatter.")
    props = parse_frontmatter(lines[1:end], [])
    module = load_modules().get(first(props.get("tipo")))
    if not module or not module.get("mapa"):
        sys.exit(f"Error: el tipo «{first(props.get('tipo')) or 'vacío'}» de {path.name} no lleva mapa.")
    body = lines[end + 1:]
    zones, problems = parse_map_key(body)
    relevance = int_value(first(props.get("relevancia")))

    if not args.add and not args.charted:
        show(path, map_status(module, props, zones, relevance), zones, problems, args.json)
        return
    if zones is None:
        sys.exit(f"Error: {path.name} no tiene sección Mapa. Si ya le toca mapa, profundízala para añadírsela.")
    if problems or map_key_problems(zones)[0]:
        sys.exit(f"Error: la leyenda de {path.name} tiene errores; corrígelos antes (check_note.py {path.stem}).")
    start = section_start(lines, end)
    offset = start + 1

    if args.charted:
        if not zones:
            sys.exit(f"Error: la leyenda de {path.name} está vacía.")
        for zone in zones:
            row = offset + zone["linea"]
            lines[row] = lines[row].replace(f" {UNCHARTED_MARK}", "").replace(UNCHARTED_MARK, "").rstrip()
        edition = (int_value(first(props.get("mapa_edicion"))) or 0) + 1
        last = max(zone["numero"] for zone in zones)
        end = set_property(lines, end, "mapa_edicion", edition)
        set_property(lines, end, "mapa_zonas", last)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"{path.name} — edición {edition} del mapa: {last} zonas cartografiadas.")
        return

    # --add
    name = args.add.strip()
    link = LINK_RE.search(name)
    if link:
        target = link.group(1).strip().lower()
        same = next((z for z in zones if z["enlace"] and z["enlace"].lower() == target), None)
        if same:
            print(f"{path.name} — [[{link.group(1).strip()}]] ya está en la leyenda como la zona {same['numero']}.")
            return
    orientation = ORIENTATION_SYNONYMS.get(normalize(args.position or ""), normalize(args.position or ""))
    if orientation not in ORIENTATIONS:
        sys.exit(f"Error: --position debe ser una de: {', '.join(ORIENTATIONS)}.")
    if args.level < 1:
        sys.exit("Error: --level empieza en 1.")
    if zones_per_level(zones).get(args.level, 0) >= MAX_MARKERS:
        where = f"el nivel {args.level}" if args.level > 1 else "la leyenda"
        print(f"{path.name} — {where} ya tiene {MAX_MARKERS} zonas, el máximo de un mapa: no la añado. Sitúa el "
              f"lugar en una zona más concreta con mapa propio (un barrio, una subregión) o anota la pregunta "
              f"en Preguntas Abiertas.")
        sys.exit(EXIT_FULL)
    numbers = {zone["numero"] for zone in zones}
    connects = sorted({int(n) for n in re.findall(r"\d+", args.connects)})
    unknown = [n for n in connects if n not in numbers]
    if unknown:
        sys.exit(f"Error: --connects nombra zonas que no existen: {', '.join(map(str, unknown))}.")
    number = max(numbers, default=0) + 1
    description = args.desc.strip()
    if description and description[-1] not in ".!?…":
        description += "."
    position = (f"nivel {args.level}, " if args.level > 1 else "") + orientation
    parts = [f"- **{number}.** **{name}** · {position} — {description or 'Sin describir.'}"]
    if connects:
        parts.append(format_connections(connects))
    if int_value(first(props.get("mapa_edicion"))):
        parts.append(UNCHARTED_MARK)
    new_line = " ".join(parts)

    for zone in zones:
        if zone["numero"] in connects:
            row = offset + zone["linea"]
            lines[row] = add_connection(lines[row], number)
    # Va tras la última zona de su nivel (con varios niveles, cada uno lleva su mapa y debajo sus zonas); en un
    # nivel nuevo, al final y con su título; en una leyenda vacía, en lugar del «1.» de la plantilla
    same_level = [zone for zone in zones if zone["nivel"] == args.level]
    if same_level:
        lines.insert(offset + max(zone["linea"] for zone in same_level) + 1, new_line)
    elif zones:
        at = offset + max(zone["linea"] for zone in zones) + 1
        lines[at:at] = ["", f"**Nivel {args.level}**", "", new_line]
    else:
        stop = next((i for i in range(offset, len(lines)) if lines[i].startswith("## ")), len(lines))
        placeholder = next((i for i in range(offset, stop) if MAP_ITEM_EMPTY_RE.match(lines[i].strip())), None)
        if placeholder is not None:
            lines[placeholder] = new_line
        else:
            at = stop
            while at > offset and not lines[at - 1].strip():
                at -= 1
            lines.insert(at, new_line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"{path.name} — zona {number} añadida a la leyenda: {new_line}")


if __name__ == "__main__":
    main()
