#!/usr/bin/env python3
"""Registro de enlaces pendientes: las entidades que alguna nota ya nombra (enlazadas) y que todavía
no tienen nota propia.

Regenera 00_Sistema/Enlaces_Pendientes.md a partir de la bóveda, agrupado por tipo: cada enlace a
una nota que no existe, con su tipo, las notas que lo nombran y su primera mención. El tipo sale de
la propiedad de relación donde aparece; si solo está en el cuerpo, del que se le asignó en el propio
registro (`--set` o la columna Tipo). Los tipos asignados se conservan al regenerar. La primera vez,
enlaza el registro desde MOC_Inicio.

Ejemplos:  pending_links.py                                     (regenera el registro)
           pending_links.py --set Madre_de_Aldric_Voss=personaje --set Puerto_Viejo=lugar
           pending_links.py --list                              (resumen, sin escribir)"""
import argparse
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (PENDING_NOTE, blocked_links, find_gaps, known_types, load_index,  # noqa: E402
                       load_modules, load_pending_types, split_note, strip_links)

# La mención se recorta a esta longitud, empezando un poco antes del enlace
MENTION_LENGTH, MENTION_BEFORE = 140, 50
EMPHASIS_RE = re.compile(r"\*\*|__|\*")
HOME_MOC = "00_Sistema/MOC_Inicio.md"
HOME_LINE = "- [[Enlaces_Pendientes]] — entidades que el mundo ya nombra y que todavía no tienen nota."

HEADER = """---
tipo: meta
---

# Enlaces pendientes

Entidades que alguna nota ya nombra (con un enlace) y que todavía no tienen nota propia. Se crean con `/crear-entidad <tipo> hueco=<Enlace>`, y el motor (`/expandir-mundo`) las va completando.
- **En Obsidian, no hagas clic en un enlace pendiente** (se ve atenuado): crearía una nota vacía con su nombre y dejaría de contar como pendiente.
- **Lo regenera `pending_links.py`** cada vez que se crean entidades: no lo edites a mano, salvo la columna Tipo. El tipo es el del módulo que creará la entidad (`asentamiento`, `lugar` o `region`, no solo «lugar»); también se asigna con `pending_links.py --set <Enlace>=<tipo>`. Si su propiedad de relación ya le da un tipo, manda la propiedad, salvo para concretar el módulo dentro de su familia.
"""


def density_text(ready, entities):
    if not entities:
        return "todavía no hay entidades"
    return f"{ready / entities:.1f} enlaces pendientes que se pueden crear por cada entidad"


def kind_of(gap):
    """El tipo con que se agrupa y se muestra un enlace pendiente: el módulo que lo creará si solo
    hay uno (un asentamiento, no «lugar»), o su tipo."""
    modules = gap["expected_modules"]
    return modules[0] if len(modules) == 1 else (gap["expected_type"] or "")


def first_mention(vault, notes, gap):
    """La primera mención del enlace, legible, sin marcas de formato y recortada alrededor de él."""
    pattern = re.compile(r"\[\[" + re.escape(gap["link"]) + r"(?:[#^][^\]|]*)?(?:\\?\|([^\]]*))?\]\]",
                         re.IGNORECASE)
    for note in notes:
        _, body = split_note((vault / note).read_text(encoding="utf-8"))
        for line in body:
            match = pattern.search(line)
            if not match:
                continue
            shown = (match.group(1) or gap["link"].replace("_", " ")).strip()
            clean = EMPHASIS_RE.sub("", strip_links(line.strip()))
            if clean.startswith("|"):
                clean = " — ".join(cell.strip() for cell in clean.strip("|").split("|") if cell.strip())
            clean = clean.lstrip("-> ").strip()
            start = max(clean.find(shown) - MENTION_BEFORE, 0)
            text = clean[start:start + MENTION_LENGTH].strip()
            return ("…" if start else "") + text + ("…" if start + MENTION_LENGTH < len(clean) else "")
    properties = sorted({o["property"] for o in gap["occurrences"] if o["property"]})
    return f"(solo en la propiedad `{properties[0]}`)" if properties else ""


def build(vault, gaps, modules, index):
    blocked = blocked_links(vault)
    by_kind, untyped = {}, []
    for gap in gaps:
        (by_kind.setdefault(kind_of(gap), []) if gap["expected_type"] else untyped).append(gap)
    ready = [g for g in gaps if g["expected_modules"] and g["link"].lower() not in blocked]
    waiting = {k: len(items) for k, items in by_kind.items() if not items[0]["expected_modules"]}
    confirming = sum(1 for g in gaps if g["link"].lower() in blocked)
    waiting_total = sum(waiting.values())
    lines = [HEADER, "## Resumen",
             f"- **{len(gaps)} {'enlace pendiente' if len(gaps) == 1 else 'enlaces pendientes'}:** {len(ready)} "
             f"{'se puede' if len(ready) == 1 else 'se pueden'} crear ya"
             + (f", {confirming} {'espera' if confirming == 1 else 'esperan'} una confirmación tuya"
                if confirming else "")
             + (f", {waiting_total} {'espera' if waiting_total == 1 else 'esperan'} su módulo ("
                + ", ".join(f"{k}: {n}" for k, n in sorted(waiting.items())) + ")" if waiting else "")
             + (f", **{len(untyped)} sin tipo**" if untyped else "") + ".",
             f"- **{len(index)} {'entidad' if len(index) == 1 else 'entidades'} en el mundo:** "
             f"{density_text(len(ready), len(index))}.", ""]

    def table(items):
        rows = ["| Enlace | Tipo | Lo nombran | Primera mención |", "|---|---|---|---|"]
        for gap in sorted(items, key=lambda g: (-len(g["notes"]), g["link"].lower())):
            notes = gap["notes"] or sorted({o["note"] for o in gap["occurrences"]})
            named = ", ".join(f"[[{Path(n).stem}]]" for n in notes[:4]) + (" …" if len(notes) > 4 else "")
            kind = kind_of(gap) or "?"
            if len(gap["expected_modules"]) > 1:
                kind += f" ({', '.join(gap['expected_modules'])})"
            if gap["link"].lower() in blocked:
                kind += " (espera confirmación)"
            elif gap["expected_type"] and not gap["expected_modules"]:
                kind += " (sin módulo todavía)"
            mention = first_mention(vault, notes, gap).replace("|", "/")
            rows.append(f"| `{gap['link']}` | {kind} | {named} | {mention} |")
        return rows

    if untyped:
        lines += [f"## Sin tipo ({len(untyped)})",
                  "Asígnales el tipo del módulo que las creará (`--set` o la columna Tipo).", ""]
        lines += table(untyped) + [""]
    for kind in sorted(by_kind, key=lambda k: (not by_kind[k][0]["expected_modules"], k)):
        lines += [f"## {kind} ({len(by_kind[kind])})", ""] + table(by_kind[kind]) + [""]
    if not gaps:
        lines.append("No hay enlaces pendientes.")
    return "\n".join(lines).rstrip() + "\n"


def link_from_home(vault):
    """Enlaza el registro desde MOC_Inicio, debajo de Preguntas_Abiertas, si falta."""
    home = vault / HOME_MOC
    if not home.is_file():
        return None
    lines = home.read_text(encoding="utf-8").splitlines()
    if any("[[Enlaces_Pendientes]]" in line for line in lines):
        return None
    anchor = next((i for i, line in enumerate(lines) if "[[Preguntas_Abiertas]]" in line), None)
    if anchor is None:
        return f"AVISO: no encuentro dónde enlazar el registro en MOC_Inicio; añádelo a mano: {HOME_LINE}"
    lines.insert(anchor + 1, HOME_LINE)
    home.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return f"Enlazado desde {HOME_MOC}."


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--set", action="append", default=[], metavar="ENLACE=TIPO",
                        help="Asigna el tipo de un enlace pendiente (repetible)")
    parser.add_argument("--list", action="store_true", help="Muestra el resumen sin escribir el registro")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    modules = load_modules()
    valid = known_types(modules)
    types = load_pending_types(vault)
    for item in args.set:
        link, _, kind = item.partition("=")
        link, kind = link.strip().strip("[]"), kind.strip().lower()
        if not link or kind not in valid:
            sys.exit(f"Error: «{item}» debe ser <Enlace>=<tipo>, con un tipo de: {', '.join(sorted(valid))}.")
        types[link.lower()] = kind

    gaps, _ = find_gaps(vault, pending_types=types)
    index = load_index(vault)
    text = build(vault, gaps, modules, index)
    untyped = [g["link"] for g in gaps if not g["expected_type"]]
    if args.list:
        print(text.split("## Resumen", 1)[1].split("\n## ", 1)[0].strip())
    else:
        (vault / PENDING_NOTE).write_text(text, encoding="utf-8", newline="\n")
        print(f"Registro actualizado: {PENDING_NOTE} ({len(gaps)} enlaces pendientes, {len(untyped)} sin tipo).")
        linked = link_from_home(vault)
        if linked:
            print(linked)
    if untyped:
        print("Sin tipo: " + ", ".join(untyped[:15]) + (" …" if len(untyped) > 15 else ""))


if __name__ == "__main__":
    main()
