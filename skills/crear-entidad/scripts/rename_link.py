#!/usr/bin/env python3
"""Cambia el destino de un enlace en toda la bóveda sin leer las notas: cuando un enlace pendiente
con nombre de rol (`Madre_de_Aldric_Voss`) se completa con una entidad que ya tiene nombre propio.

Reemplaza `[[Viejo]]`, `[[Viejo|texto]]`, `[[Viejo#Sección|texto]]` y `[[Viejo\\|texto]]` (en las
tablas) por el destino nuevo, en el frontmatter y en el cuerpo de todas las notas, sin distinguir
mayúsculas, y conserva el texto visible. En el cuerpo, un enlace que no llevaba texto recibe el
nombre legible del nuevo si su archivo lleva guiones bajos. Las plantillas, los archivados y el
registro de enlaces pendientes no se tocan (el registro se regenera con pending_links.py).

Ejemplos:  rename_link.py Madre_de_Aldric_Voss Elsa_Voss
           rename_link.py Madre_de_Aldric_Voss Elsa_Voss --dry-run"""
import argparse
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import DEFAULT_EXCLUDED, is_hidden  # noqa: E402
from vault_lib import vault_path  # noqa: E402

MAX_LISTED = 20


def renamer(new, in_table, in_frontmatter):
    readable = new.replace("_", " ")
    separator = "\\|" if in_table else "|"  # en las tablas, la barra del alias va escapada

    def replace(match):
        anchor, alias = match.group(1) or "", match.group(2)
        if in_frontmatter:
            return f"[[{new}{anchor}]]"
        if alias:
            return f"[[{new}{anchor}{alias}]]"
        if "_" in new:
            return f"[[{new}{anchor}{separator}{readable}]]"
        return f"[[{new}{anchor}]]"
    return replace


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("old", help="Destino viejo (el enlace pendiente con nombre de rol)")
    parser.add_argument("new", help="Destino nuevo (la nota con su nombre propio)")
    parser.add_argument("--dry-run", action="store_true", help="Solo muestra dónde cambiaría, sin escribir")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    old, new = args.old.strip().strip("[]"), args.new.strip().strip("[]")
    if not old or not new or old.lower() == new.lower():
        sys.exit("Error: indica un destino viejo y uno nuevo distintos.")
    pattern = re.compile(r"\[\[" + re.escape(old) + r"(#[^\]|\\]*)?((?:\\?\|)[^\]]*)?\]\]", re.IGNORECASE)

    changed = []
    for path in sorted(vault.rglob("*.md")):
        relative = path.relative_to(vault).as_posix()
        if is_hidden(relative) or relative.startswith(DEFAULT_EXCLUDED):
            continue
        text = path.read_text(encoding="utf-8")
        if old.lower() not in text.lower():
            continue
        lines = text.split("\n")
        in_frontmatter = bool(lines) and lines[0].strip() == "---"
        count = 0
        for i, line in enumerate(lines):
            if in_frontmatter and i > 0 and line.strip() == "---":
                in_frontmatter = False
                continue
            fixed, n = pattern.subn(renamer(new, line.lstrip().startswith("|"), in_frontmatter and i > 0), line)
            if n:
                lines[i], count = fixed, count + n
        if count:
            changed.append((relative, count))
            if not args.dry_run:
                path.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    total = sum(n for _, n in changed)
    verb = "cambiaría" if args.dry_run else "cambiados"
    print(f"[[{old}]] → [[{new}]]: {total} enlaces {verb} en {len(changed)} notas")
    for relative, n in changed[:MAX_LISTED]:
        print(f"  · {relative} ({n})")
    if len(changed) > MAX_LISTED:
        print(f"  … y {len(changed) - MAX_LISTED} notas más")
    if changed and not args.dry_run:
        print("Regenera el registro con pending_links.py.")


if __name__ == "__main__":
    main()
