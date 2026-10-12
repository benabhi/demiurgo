#!/usr/bin/env python3
"""Tira en las tablas de generación (azar real) y devuelve los ingredientes como clave=valor.

Las tablas son Markdown editable: 00_Sistema/06_Generacion/Tablas/<Archivo>.md en la bóveda o,
si no existe, assets/Tablas/ de esta skill. Cada tabla es una sección `## Nombre` con filas
`| Peso | Resultado |`: a más peso, más frecuente.

Con --derive <Nota> añade ingredientes derivados del canon: por cada propiedad de relación de
esa nota (pueblos, especies, creencias, control…) elige uno de sus enlaces. Así lo que se crea
en una región sale de lo que ya existe allí.

Siempre imprime la semilla usada, para poder repetir la tirada y anotarla en el registro.

Ejemplos:  roll_tables.py --file Oraculos
           roll_tables.py --file Personaje --file Oraculos --derive Reino_de_Ejemplo
           roll_tables.py --file Personaje --table Edad --seed 12
           roll_tables.py --list"""
import argparse
import random
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py, en los scripts de crear-entidad
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "crear-entidad" / "scripts"))
from vault_lib import load_index, load_modules, normalize  # noqa: E402

ASSET_TABLES = Path(__file__).resolve().parent.parent / "assets" / "Tablas"
VAULT_TABLES = "00_Sistema/06_Generacion/Tablas"
ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$")


def find_file(vault, name):
    wanted = normalize(name)
    for folder in (vault / VAULT_TABLES, ASSET_TABLES):
        if folder.is_dir():
            for path in sorted(folder.glob("*.md")):
                if normalize(path.stem) == wanted:
                    return path
    return None


def parse_tables(path):
    """{nombre de tabla: [(peso, resultado)]}."""
    tables, current = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            current = heading.group(1).strip()
            tables[current] = []
            continue
        row = ROW_RE.match(line)
        if current and row and int(row.group(1)) > 0:
            tables[current].append((int(row.group(1)), row.group(2)))
    return {name: rows for name, rows in tables.items() if rows}


def key_of(name):
    return re.sub(r"[^a-z0-9]+", "_", normalize(name)).strip("_")


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", action="append", default=[], help="Archivo de tablas (repetible)")
    parser.add_argument("--table", action="append", default=[], help="Solo estas tablas (repetible)")
    parser.add_argument("--derive", help="Nota de la que derivar ingredientes de sus relaciones")
    parser.add_argument("--seed", type=int, help="Semilla para repetir la tirada")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--list", action="store_true", help="Lista los archivos y tablas disponibles")
    args = parser.parse_args()

    vault = Path(args.vault)
    if args.list:
        seen = set()
        for folder, origin in ((vault / VAULT_TABLES, "bóveda"), (ASSET_TABLES, "skill")):
            for path in sorted(folder.glob("*.md")) if folder.is_dir() else []:
                if normalize(path.stem) in seen:
                    continue
                seen.add(normalize(path.stem))
                print(f"- {path.stem} ({origin}): {', '.join(parse_tables(path))}")
        return
    if not args.file and not args.derive:
        sys.exit("Error: indica al menos un --file o un --derive (o usa --list).")

    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(10 ** 9)
    rng = random.Random(seed)
    wanted = {normalize(t) for t in args.table}
    for name in args.file:
        path = find_file(vault, name)
        if not path:
            sys.exit(f"Error: no existe el archivo de tablas '{name}'. Usa --list para ver los disponibles.")
        for table, rows in parse_tables(path).items():
            if wanted and normalize(table) not in wanted:
                continue
            total = sum(weight for weight, _ in rows)
            weight, result = rng.choices(rows, weights=[w for w, _ in rows])[0]
            print(f"{key_of(table)}={result}    # {path.stem} · peso {weight} de {total}")

    if args.derive:
        entry = next((e for e in load_index(vault) if e["name"].lower() == args.derive.strip().lower()), None)
        if not entry:
            sys.exit(f"Error: no existe la nota '{args.derive}' para derivar ingredientes.")
        relation_keys = load_modules().get(entry["tipo"], {}).get("relaciones", {})
        for prop, targets in sorted(entry["relaciones"].items()):
            if prop not in relation_keys:
                continue  # solo propiedades de relación del módulo (no la imagen, por ejemplo)
            choice = rng.choice(targets)
            print(f"deriv_{prop}=[[{choice}]]    # {len(targets)} opciones en {entry['name']}")
    print(f"semilla={seed}")


if __name__ == "__main__":
    main()
