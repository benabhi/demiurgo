#!/usr/bin/env python3
"""Disuelve un enlace pendiente: la entidad que nombra no tendrá nota. En todas las notas, el enlace pasa a ser
texto (el que mostraba, o su nombre legible), sale de las propiedades de relación donde estaba y, en una leyenda
de mapa, su zona se queda con el nombre y sin el enlace. En el Glosario, su fila pierde la nota. Con --term, queda
además como término del Glosario.

Sirve para lo que no merece nota (un sitio o una persona que solo se nombra de pasada); lo usa finalizar-mundo
con lo menor. Para un enlace que es otro nombre de algo que ya existe, rename_link.py; para quitar del mundo algo
que ya tiene nota, revisar-mundo.

Ejemplos:  dissolve_link.py Taberna_del_Cruce
           dissolve_link.py Mena_Roja --term expresion 'Hierro en bruto de las vetas del norte'"""
import argparse
import datetime
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from add_entries import add_glossary  # noqa: E402
from pending_links import build  # noqa: E402
from vault_lib import (ARCHIVED_FOLDER, CHRONICLE, GLOSSARY, NARRATIVE_FOLDER, PENDING_NOTE, STATS_NOTE,  # noqa: E402
                       add_canon_log, find_gaps, is_hidden, load_index, load_modules)
from vault_lib import vault_path  # noqa: E402

# Lo que no se toca: la historia (la Bitácora y lo archivado) y lo que se rehace solo (el registro y las Estadísticas)
UNTOUCHED = (ARCHIVED_FOLDER, CHRONICLE, PENDING_NOTE, STATS_NOTE, NARRATIVE_FOLDER)


def link_pattern(link):
    return re.compile(r"!?\[\[" + re.escape(link) + r"(?:#[^\]|]*)?(?:\\?\|([^\]]*))?\]\]", re.IGNORECASE)


def dissolve_text(text, link, glossary=False):
    """El texto de una nota sin el enlace. Devuelve (texto, cuántos cambios)."""
    pattern = link_pattern(link)
    readable = link.replace("_", " ")
    lines, changes, out = text.splitlines(), 0, []
    in_frontmatter = bool(lines) and lines[0].strip() == "---"
    for i, line in enumerate(lines):
        if in_frontmatter and i > 0 and line.strip() == "---":
            in_frontmatter = False
            out.append(line)
            continue
        if not pattern.search(line):
            out.append(line)
            continue
        changes += 1
        if in_frontmatter:
            item = re.match(r"^\s*-\s*", line)
            if item:
                continue  # el elemento de una lista de relación se va entero
            key = re.match(r"^([\w-]+):", line)
            out.append(f"{key.group(1)}: \"\"" if key else pattern.sub(lambda m: m.group(1) or readable, line))
            continue
        if glossary and line.strip().startswith("|"):
            # En el Glosario, la columna Nota se vacía; en la definición, el enlace pasa a texto
            cells = re.split(r"(?<!\\)\|", line)
            if len(cells) > 4 and pattern.search(cells[3]):
                cells[3] = " "
            line = "|".join(cells)
        out.append(pattern.sub(lambda m: (m.group(1) or readable).strip(), line))
    # En el frontmatter, una lista que se quedó sin elementos pasa a ser `[]`
    end = next((i for i in range(1, len(out)) if out[i].strip() == "---"), 0) if out and out[0].strip() == "---" else 0
    for i in range(1, end):
        key = re.match(r"^([\w-]+):\s*$", out[i])
        if key and not re.match(r"^\s*-\s", out[i + 1]):
            out[i] = f"{key.group(1)}: []"
    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), changes


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("link", help="El enlace pendiente que se disuelve")
    parser.add_argument("--term", nargs=2, metavar=("TIPO", "DEFINICIÓN"),
                        help="Lo deja como término del Glosario, con su tipo de término y su definición")
    parser.add_argument("--reason", default="", help="Por qué no tiene nota (para el Registro de Canon)")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    link = args.link.strip().strip("[]")
    gaps, _ = find_gaps(vault)
    gap = next((g for g in gaps if g["link"].lower() == link.lower()), None)
    if not gap:
        sys.exit(f"Error: [[{link}]] no es un enlace pendiente (si tiene nota y quieres sacarla del mundo, usa "
                 f"/revisar-mundo; si es otro nombre de algo que existe, rename_link.py).")
    link = gap["link"]
    touched = []
    for path in sorted(vault.rglob("*.md")):
        relative = path.relative_to(vault).as_posix()
        if is_hidden(relative) or relative.startswith(UNTOUCHED):
            continue
        text = path.read_text(encoding="utf-8")
        new, changes = dissolve_text(text, link, glossary=relative == GLOSSARY)
        if changes:
            path.write_text(new, encoding="utf-8", newline="\n")
            touched.append((relative, changes))
    messages = []
    if args.term:
        messages = add_glossary(vault, [(link.replace("_", " "), args.term[0], "", args.term[1])])
    # La decisión queda en el Registro de Canon, como texto (la entidad no tendrá nota)
    add_canon_log(vault, [f"| {datetime.date.today().isoformat()} | {link.replace('_', ' ')} | Disuelto: queda como "
                          f"texto{', término del Glosario' if args.term else ''} | "
                          f"{args.reason.strip().rstrip('.') or 'no merece nota'} |"])
    gaps, _ = find_gaps(vault)
    (vault / PENDING_NOTE).write_text(build(vault, gaps, load_modules(), load_index(vault)), encoding="utf-8",
                                      newline="\n")
    print(f"Disuelto [[{link}]]: ya no es un enlace pendiente; queda como texto en {len(touched)} nota(s).")
    for relative, changes in touched:
        print(f"  {relative}: {changes} línea(s)")
    for message in messages:
        print(f"Glosario: {message}")
    if not args.term and touched:
        print(f"AVISO: «{link.replace('_', ' ')}» queda en el texto como nombre propio sin enlace, y check_note lo "
              f"señala: regístralo como término del Glosario (--term <clase> <definición>, con una clase que no sea "
              f"un tipo de entidad) o reescribe esas menciones sin nombre propio.")
    print(f"Registro de enlaces pendientes rehecho ({len(gaps)}).")


if __name__ == "__main__":
    main()
