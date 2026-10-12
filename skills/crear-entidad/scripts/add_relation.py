#!/usr/bin/env python3
"""Añade enlaces a una propiedad de relación de una nota sin leerla entera: el vínculo inverso que
pide la reciprocidad (el sistema nuevo en los `sistemas` de un personaje, por ejemplo).

- En una propiedad de lista añade cada enlace que falte. En una de un solo valor lo pone si está
  vacía; si ya tiene otro, avisa y no lo cambia.
- Si la nota no tiene la propiedad (es anterior a un cambio de su plantilla), la añade en el sitio
  que le da la plantilla.
- Solo acepta las propiedades de relación del módulo de la nota.

Ejemplos:  add_relation.py Mira_Odan sistemas Arte_del_Hilo
           add_relation.py Puerto_Viejo lugares_notables Faro_Viejo Lonja_Vieja"""
import argparse
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (ITEM_LINE_RE, KEY_LINE_RE, SKILL_DIR, first, link_value, load_modules,  # noqa: E402
                       parse_frontmatter, resolve_note, split_note)


def template_keys(tipo):
    """(propiedades de la plantilla en orden, las que son listas)."""
    frontmatter, _ = split_note((SKILL_DIR / "tipos" / tipo / "plantilla.md").read_text(encoding="utf-8"))
    keys, lists = [], set()
    for line in frontmatter or []:
        match = KEY_LINE_RE.match(line)
        if match:
            keys.append(match.group(1))
            if match.group(2).strip() in ("[]", ""):
                lists.add(match.group(1))
    return keys, lists


def block_end(lines, start, end):
    """Índice siguiente a la propiedad de la línea `start` y a sus elementos de lista."""
    i = start + 1
    while i < end and ITEM_LINE_RE.match(lines[i]):
        i += 1
    return i


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("note", help="Nombre o ruta de la nota que recibe el vínculo")
    parser.add_argument("property", help="Propiedad de relación (facciones, sistemas, region…)")
    parser.add_argument("links", nargs="+", help="Destinos que añadir (Nota o [[Nota]])")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    path = resolve_note(args.note, vault)
    if not path:
        sys.exit(f"Error: no encuentro la nota '{args.note}' (o hay varias con ese nombre).")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---" or "---" not in [l.strip() for l in lines[1:]]:
        sys.exit(f"Error: {path.name} no tiene frontmatter.")
    end = [l.strip() for l in lines[1:]].index("---") + 1
    tipo = first(parse_frontmatter(lines[1:end], []).get("tipo"))
    module = load_modules().get(tipo)
    if not module:
        sys.exit(f"Error: el tipo «{tipo or 'vacío'}» de {path.name} no tiene módulo.")
    key = args.property
    if key not in module["relaciones"]:
        sys.exit(f"Error: `{key}` no es una propiedad de relación de {tipo} "
                 f"({', '.join(module['relaciones'])}).")
    order, lists = template_keys(tipo)
    is_list = key in lists
    targets = [t.strip().strip("[]").split("|")[0].strip() for t in args.links]
    if not is_list and len(targets) > 1:
        sys.exit(f"Error: `{key}` admite un solo enlace.")

    row = next((i for i in range(1, end) if KEY_LINE_RE.match(lines[i])
                and KEY_LINE_RE.match(lines[i]).group(1) == key), None)
    if row is None:
        # La nota es anterior a esta propiedad: va tras la propiedad anterior de la plantilla que tenga
        previous = [k for k in order[:order.index(key)]] if key in order else []
        rows = {KEY_LINE_RE.match(lines[i]).group(1): i for i in range(1, end) if KEY_LINE_RE.match(lines[i])}
        anchor = next((rows[k] for k in reversed(previous) if k in rows), None)
        at = block_end(lines, anchor, end) if anchor is not None else end
        lines[at:at] = [f"{key}: []" if is_list else f'{key}: ""']
        end += 1
        row = at
        print(f"{path.name} — no tenía `{key}`: la añado")

    stop = block_end(lines, row, end)
    raw = KEY_LINE_RE.match(lines[row]).group(2).strip()
    current = [v for v in (link_value(i) for i in ([raw] if raw not in ("", "[]") else [])
                           + [ITEM_LINE_RE.match(l).group(1) for l in lines[row + 1:stop]]) if v]
    if raw.startswith("[") and raw not in ("[]",):
        current = [v for v in (link_value(x) for x in raw.strip("[]").split(",")) if v]
    known = {c.lower() for c in current}
    new = [t for t in targets if t.lower() not in known]
    for t in targets:
        if t.lower() in known:
            print(f"{path.name} — `{key}`: ya estaba [[{t}]]")
    if not new:
        return
    if is_list:
        added = [f'  - "[[{t}]]"' for t in new]
        if raw.startswith("[") and raw != "[]":
            # Lista en línea («[a, b]»): pasa a una por línea, con las que ya tenía
            lines[row:stop] = [f"{key}:"] + [f'  - "[[{c}]]"' for c in current] + added
        else:
            # Las líneas que ya tenía se quedan tal cual; las nuevas van al final de la lista
            lines[row:stop] = [f"{key}:"] + lines[row + 1:stop] + added
    else:
        if current:
            sys.exit(f"{path.name} — `{key}` ya vale [[{current[0]}]]: no lo cambio por [[{new[0]}]]. "
                     f"Si de verdad cambia, edítalo a mano.")
        lines[row:stop] = [f'{key}: "[[{new[0]}]]"']
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    for t in new:
        print(f"{path.name} — `{key}`: añadido [[{t}]]")


if __name__ == "__main__":
    main()
