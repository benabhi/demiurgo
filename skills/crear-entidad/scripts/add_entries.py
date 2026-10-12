#!/usr/bin/env python3
"""Añade entradas a las notas internas que crecen con el mundo, sin que haga falta leerlas enteras:
filas del Glosario y preguntas o confirmaciones en Preguntas Abiertas.

- Glosario (`--glossary TÉRMINO TIPO NOTA DEFINICIÓN`, repetible): una fila al final de la tabla
  (la fila vacía de la plantilla se sustituye). Si el término ya está con el mismo Tipo, no se
  repite; si está con otro Tipo, avisa y no lo añade. NOTA es el enlace a la nota (`[[Nota]]`) o
  vacía (""); las barras verticales de las celdas se escapan solas.
- Preguntas Abiertas: `--question TEXTO` añade `- [ ] TEXTO` y `--confirm TEXTO` añade
  `- [ ] Confirmar: TEXTO` al final de la sección «Otras preguntas». Una línea igual no se repite.
  En una confirmación, el sujeto del hecho va enlazado primero (ver SKILL.md).

Ejemplos:  add_entries.py --glossary "Puerto Viejo" asentamiento "[[Puerto_Viejo]]" "Villa de pescadores"
           add_entries.py --confirm "existe el gremio [[Gremio_del_Puerto]] (propuesto al crear [[Puerto_Viejo]])"
           add_entries.py --question "¿Quién gobierna [[Puerto_Viejo]]?" """
import argparse
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (CELL_SPLIT_RE, GLOSSARY, OPEN_QUESTIONS, glossary_table, normalize,  # noqa: E402
                       split_terms)

EMPTY_ROW_RE = re.compile(r"^\|(\s*\|)+\s*$")
OTHER_QUESTIONS = "## Otras preguntas"


def cell(text):
    """Una celda de tabla: sin saltos de línea y con las barras verticales escapadas."""
    return CELL_SPLIT_RE.sub(r"\\|", " ".join((text or "").split()))


def add_glossary(vault, entries):
    """Añade las filas que no estaban. Devuelve los mensajes del resultado."""
    path = vault / GLOSSARY
    if not path.is_file():
        return [f"ERROR: no existe el Glosario ({GLOSSARY})"]
    lines = path.read_text(encoding="utf-8").splitlines()
    header = next((i for i, l in enumerate(lines) if l.strip().startswith("|")
                   and normalize(l.strip().strip("|").split("|")[0]) == "termino"), None)
    if header is None:
        return ["ERROR: el Glosario no tiene la tabla «| Término | Tipo | Nota | Definición breve |»"]
    end = header + 1
    while end < len(lines) and lines[end].strip().startswith("|"):
        end += 1
    known = {}
    for row in glossary_table(vault):
        for name in row["nombres"]:
            known.setdefault(normalize(name), row["tipo"])
    rows, messages = [], []
    for term, kind, note, definition in entries:
        existing = next((known[normalize(n)] for n in split_terms(term) if normalize(n) in known), None)
        if existing is not None:
            if normalize(existing) == normalize(kind):
                messages.append(f"ya estaba: «{term}» ({kind})")
            else:
                messages.append(f"AVISO: «{term}» ya está en el Glosario como «{existing}»; no lo añado. Si es "
                                f"otra cosa, usa otro nombre; si el Tipo estaba mal, corrige esa fila")
            continue
        rows.append(f"| {cell(term)} | {cell(kind)} | {cell(note)} | {cell(definition)} |")
        for name in split_terms(term):
            known[normalize(name)] = kind
        messages.append(f"añadido: «{term}» ({kind})")
    if rows:
        # La fila vacía de la plantilla («| | | | |») se sustituye por la primera fila real
        body = [l for l in lines[header + 2:end] if not EMPTY_ROW_RE.match(l.strip())]
        lines[header + 2:end] = body + rows
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return messages


def add_questions(vault, items):
    """Añade las líneas que no estaban al final de «Otras preguntas». Devuelve los mensajes."""
    path = vault / OPEN_QUESTIONS
    if not path.is_file():
        return [f"ERROR: no existe Preguntas Abiertas ({OPEN_QUESTIONS})"]
    lines = path.read_text(encoding="utf-8").splitlines()
    present = {normalize(l.strip()) for l in lines}
    start = next((i for i, l in enumerate(lines) if l.strip() == OTHER_QUESTIONS), None)
    if start is None:
        lines += ["", OTHER_QUESTIONS]
        start = len(lines) - 1
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1  # las nuevas van pegadas a la última de la sección, no tras las líneas en blanco
    new, messages = [], []
    for item in items:
        line = f"- [ ] {item.strip()}"
        if normalize(line) in present:
            messages.append(f"ya estaba: {line}")
            continue
        new.append(line)
        present.add(normalize(line))
        messages.append(f"añadida: {line}")
    if new:
        lines[end:end] = new
        path.write_text("\n".join(lines).rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    return messages


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--glossary", nargs=4, action="append", default=[],
                        metavar=("TÉRMINO", "TIPO", "NOTA", "DEFINICIÓN"), help="Una fila del Glosario (repetible)")
    parser.add_argument("--question", action="append", default=[], metavar="TEXTO",
                        help="Una pregunta abierta (repetible)")
    parser.add_argument("--confirm", action="append", default=[], metavar="TEXTO",
                        help="Un hecho por confirmar, con su sujeto enlazado primero (repetible)")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    if not (args.glossary or args.question or args.confirm):
        sys.exit("Error: indica qué añadir (--glossary, --question o --confirm).")
    messages = []
    if args.glossary:
        messages += [f"Glosario — {m}" for m in add_glossary(vault, args.glossary)]
    items = list(args.question) + [f"Confirmar: {text.strip()}" for text in args.confirm]
    if items:
        messages += [f"Preguntas Abiertas — {m}" for m in add_questions(vault, items)]
    print("\n".join(messages))
    sys.exit(1 if any("ERROR" in m for m in messages) else 0)


if __name__ == "__main__":
    main()
