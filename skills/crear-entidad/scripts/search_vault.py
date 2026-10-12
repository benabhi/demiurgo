#!/usr/bin/env python3
"""Busca en la bóveda sin leerla entera: las entidades, los enlaces pendientes, el Glosario y las
preguntas abiertas que coinciden con un texto, con un tope de resultados por grupo.

Sirve para comprobar si algo ya existe antes de crearlo (también con nombres parecidos, que pueden
ser la misma cosa escrita de otra forma), para reutilizar un enlace pendiente en lugar de inventar
otro y para encontrar lo que el mundo dice de un tema. No distingue mayúsculas ni tildes, y cada
palabra del texto tiene que aparecer en lo que coincide, en cualquier orden. En las entidades busca
en el nombre, el título y los alias y, después, en el resumen.

Ejemplos:  search_vault.py "puerto viejo"
           search_vault.py gremio --in entidades pendientes
           search_vault.py --type faccion
           search_vault.py --type sistema sangre --limit 5"""
import argparse
import difflib
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (OPEN_QUESTIONS, blocked_links, describe_expected, find_gaps,  # noqa: E402
                       glossary_table, load_index, load_modules, normalize, strip_links)

GROUPS = ("entidades", "pendientes", "glosario", "preguntas")
MAX_SUMMARY = 140
SIMILAR_CUTOFF = 0.85
MAX_NAMERS = 3


def words(text):
    """Palabras comparables de un texto (sin tildes ni mayúsculas, sin signos)."""
    return [w for w in "".join(c if c.isalnum() else " " for c in normalize(text)).split() if w]


def matches(query, text):
    """Si todas las palabras de la búsqueda aparecen en el texto, en cualquier orden."""
    haystack = set(words(text))
    return all(any(h.startswith(w) for h in haystack) for w in query)


def short(text, limit=MAX_SUMMARY):
    text = " ".join((text or "").split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def shown(items, limit, render):
    """Las primeras `limit` líneas y, si hay más, cuántas faltan."""
    lines = [render(item) for item in items[:limit]]
    if len(items) > limit:
        lines.append(f"  … y {len(items) - limit} más: afina la búsqueda o sube --limit")
    return lines


def family_of(tipo, modules):
    """Los tipos de una familia (lugar: región, asentamiento, lugar) o el propio tipo."""
    family = {t for t, m in modules.items() if m.get("familia") == tipo}
    return family or {tipo}


def entity_line(entry):
    relevance = entry["relevancia"] if entry["relevancia"] is not None else "?"
    summary = short(entry["resumen"]) or "(sin resumen)"
    return f"- [[{entry['name']}]] · {entry['tipo']} · relevancia {relevance} — {summary}  ({entry['path']})"


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", nargs="*", help="Texto que buscar (varias palabras: todas deben aparecer)")
    parser.add_argument("--type", help="Solo entidades de este tipo o de esta familia (lugar incluye región, "
                                       "asentamiento y lugar)")
    parser.add_argument("--in", dest="groups", nargs="+", choices=GROUPS,
                        help="Dónde buscar (por defecto, en todo): " + ", ".join(GROUPS))
    parser.add_argument("--limit", type=int, default=10, help="Resultados por grupo (por defecto 10)")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    query = words(" ".join(args.query))
    if not query and not args.type:
        sys.exit("Error: indica un texto que buscar o un tipo (--type).")
    groups = set(args.groups or (["entidades"] if args.type and not query else GROUPS))
    if args.type:
        groups = {"entidades"} | (groups if query else set())

    modules = load_modules()
    index = load_index(vault)
    out = [f"Búsqueda: «{' '.join(args.query)}»" + (f" · tipo {args.type}" if args.type else "")]
    found = 0

    # Entidades: primero las que coinciden por su nombre, su título o un alias; después, por su resumen
    if "entidades" in groups:
        pool = index
        if args.type:
            allowed = family_of(args.type, modules)
            pool = [e for e in index if e["tipo"] in allowed]
        by_name, by_summary = [], []
        for entry in pool:
            names = " ".join([entry["name"].replace("_", " "), entry["titulo"], *entry["aliases"]])
            if not query or matches(query, names):
                by_name.append(entry)
            elif matches(query, entry["resumen"]):
                by_summary.append(entry)
        rank = lambda e: (-(e["relevancia"] or 0), e["name"].lower())  # noqa: E731
        hits = sorted(by_name, key=rank) + sorted(by_summary, key=rank)
        found += len(hits)
        title = f"Entidades de tipo {args.type}" if args.type and not query else "Entidades"
        out += ["", f"{title} ({len(hits)}):"] + (shown(hits, args.limit, entity_line) if hits else ["- ninguna"])

        # Nombres parecidos: la misma cosa escrita de otra forma (posibles duplicados)
        if query:
            labels = {}
            for entry in pool:
                for label in {entry["titulo"], entry["name"].replace("_", " "), *entry["aliases"]}:
                    if label:
                        labels.setdefault(" ".join(words(label)), entry)
            exact = {e["name"] for e in hits}
            close = difflib.get_close_matches(" ".join(query), list(labels), n=5, cutoff=SIMILAR_CUTOFF)
            similar = [(label, labels[label]) for label in close if labels[label]["name"] not in exact]
            if similar:
                out += ["", f"Nombres parecidos ({len(similar)}), quizá la misma entidad:"]
                out += [f"- [[{e['name']}]] · {e['tipo']} — «{label}»" for label, e in similar[:args.limit]]

    # Enlaces pendientes: entidades que alguna nota ya nombra y que aún no tienen nota
    if "pendientes" in groups and query:
        gaps, _ = find_gaps(vault)
        blocked = blocked_links(vault)
        hits = [g for g in gaps if matches(query, g["link"].replace("_", " "))]
        if args.type:
            allowed = family_of(args.type, modules) | {args.type}
            hits = [g for g in hits if g["expected_type"] in allowed or set(g["expected_modules"]) & allowed]
        found += len(hits)

        def gap_line(gap):
            namers = gap["notes"] or sorted({o["note"] for o in gap["occurrences"]})
            named = ", ".join(f"[[{Path(n).stem}]]" for n in namers[:MAX_NAMERS])
            named += " …" if len(namers) > MAX_NAMERS else ""
            waiting = " · espera una confirmación" if gap["link"].lower() in blocked else ""
            return f"- [[{gap['link']}]] → {describe_expected(gap)}{waiting} · lo nombran {named}"
        out += ["", f"Enlaces pendientes ({len(hits)}):"] + (shown(hits, args.limit, gap_line) if hits else ["- ninguno"])

    # Glosario: por el término y, después, por la definición
    if "glosario" in groups and query:
        rows = glossary_table(vault)
        by_term = [r for r in rows if matches(query, r["termino"])]
        by_text = [r for r in rows if r not in by_term and matches(query, r["definicion"])]
        hits = by_term + by_text
        found += len(hits)
        out += ["", f"Glosario ({len(hits)}):"] + (shown(
            hits, args.limit, lambda r: f"- «{r['termino']}» ({r['tipo'] or 'sin tipo'}) {r['nota']} — "
                                        f"{short(r['definicion'])}".replace("  — ", " — ")) if hits else ["- nada"])

    # Preguntas abiertas: primero las que siguen sin resolver
    if "preguntas" in groups and query:
        path = vault / OPEN_QUESTIONS
        lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
        items = [l.strip() for l in lines if l.strip().startswith(("- [ ]", "- [x]", "- [X]"))]
        hits = [l for l in items if matches(query, strip_links(l))]
        hits.sort(key=lambda l: not l.startswith("- [ ]"))
        found += len(hits)
        out += ["", f"Preguntas abiertas ({len(hits)}):"] + (shown(hits, args.limit, short) if hits else ["- ninguna"])

    if not found and query:
        out.append("\nNada coincide. Si es nuevo, no hay duplicado que temer.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
