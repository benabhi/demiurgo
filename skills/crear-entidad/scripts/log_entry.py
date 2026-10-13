#!/usr/bin/env python3
"""Añade una entrada suelta a la Bitácora del mundo (00_Sistema/Bitacora.md) sin leerla.

La Bitácora cuenta, para el autor del mundo, qué se creó y qué cambió en cada tarea, de lo más reciente a
lo más antiguo. Al terminar un generador, la entrada la escribe `report.py --log` con los datos del
informe; este script es para lo demás: una imagen o un mapa generados aparte, un cambio que se pidió
fuera de las skills o una entrada del pasado.

La entrada va arriba, con su fecha (hoy, o la de --date) y su título: `## <fecha> · <título>`. Cada
--line es una línea de la entrada; si no empieza por «- » ni por un número de lista, se le pone «- ».
Las notas que existen van enlazadas (`[[Nota|Nombre]]`); los enlaces pendientes, como texto. Si la
Bitácora no existe, la crea y la enlaza desde MOC_Inicio.

Ejemplos:  log_entry.py --title "Imagen: Aldric Voss" --line "**Nueva imagen** de [[Aldric_Voss|Aldric Voss]] en óleo (versión 2)."
           log_entry.py --title "Se creó el mundo «Ejemplo»" --date 2026-01-31 --line "**Bóveda:** estructura, guías y Ficha del Mundo.\""""
import argparse
import datetime
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import CHRONICLE, add_chronicle_entry, readable_links  # noqa: E402
from vault_lib import vault_path  # noqa: E402


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--title", required=True, help="Qué se hizo, en pocas palabras («Mapa: Puerto Gris»)")
    parser.add_argument("--line", action="append", default=[], help="Una línea de la entrada (repetible)")
    parser.add_argument("--date", help="Fecha de la entrada, AAAA-MM-DD (por defecto, hoy)")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    if args.date:
        try:
            datetime.date.fromisoformat(args.date)
        except ValueError:
            sys.exit(f"Error: --date debe ser una fecha AAAA-MM-DD (encontrado: {args.date}).")
    if not args.line:
        sys.exit("Error: la entrada necesita al menos una --line.")
    lines = []
    for line in args.line:
        line = readable_links(line.strip())
        lines.append(line if line.startswith("- ") or re.match(r"^\d+\. ", line) else f"- {line}")
    for warning in add_chronicle_entry(vault, args.title.strip(), lines, args.date):
        print(f"AVISO: {warning}")
    print(f"Bitácora: añadida la entrada «{args.title.strip()}» en {CHRONICLE}.")


if __name__ == "__main__":
    main()
