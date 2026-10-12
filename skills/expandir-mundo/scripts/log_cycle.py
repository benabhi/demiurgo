#!/usr/bin/env python3
"""Añade la entrada de un ciclo al Registro de Generación sin leerlo entero: va arriba, debajo del
comentario, con su número (el último ciclo registrado más uno) y la fecha de hoy.

El cuerpo de la entrada (las líneas «- **Acción:** …», «- **Por qué:** …», etc.; ver el Paso 6 de
SKILL.md) llega por la entrada estándar o con --file, sin el título «## Ciclo», que pone el script.
Imprime el número del ciclo, que va también en el mensaje del commit.

Ejemplos:  log_cycle.py --file entrada.md
           log_cycle.py < entrada.md"""
import argparse
import datetime
import re
import sys
from pathlib import Path

LOG = "00_Sistema/06_Generacion/Registro_de_Generacion.md"
MARKER = "<!-- Las entradas nuevas se añaden debajo de esta línea -->"
CYCLE_RE = re.compile(r"^## Ciclo (\d+)\b")


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", help="Archivo con el cuerpo de la entrada (si no, la entrada estándar)")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    args = parser.parse_args()

    path = Path(args.vault) / LOG
    if not path.is_file():
        sys.exit(f"Error: no existe {LOG}: ejecuta antes setup_generation.py.")
    body = (Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read()).strip("\n")
    body_lines = [l for l in body.splitlines() if not CYCLE_RE.match(l)]
    if not any(l.strip() for l in body_lines):
        sys.exit("Error: la entrada está vacía.")

    lines = path.read_text(encoding="utf-8").splitlines()
    numbers = [int(m.group(1)) for m in (CYCLE_RE.match(l) for l in lines) if m]
    number = max(numbers, default=0) + 1
    entry = [f"## Ciclo {number} — {datetime.date.today().isoformat()}"] + body_lines
    at = next((i + 1 for i, l in enumerate(lines) if l.strip() == MARKER), None)
    if at is None:
        # Sin el comentario (lo borró alguien), la entrada va tras el título
        at = next((i + 1 for i, l in enumerate(lines) if l.startswith("# ")), len(lines))
    rest = lines[at:]
    while rest and not rest[0].strip():
        rest.pop(0)
    lines[at:] = [""] + entry + ([""] + rest if rest else [])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Ciclo {number} registrado en {LOG}")


if __name__ == "__main__":
    main()
