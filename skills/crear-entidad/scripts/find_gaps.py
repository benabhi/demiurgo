#!/usr/bin/env python3
"""Lista los enlaces pendientes (huecos) de la bóveda: enlaces a notas que todavía no existen,
es decir, entidades que el mundo ya nombra y que aún no tienen nota.

Para cada uno indica las notas que lo contienen, si aparece en una propiedad o en una sección,
el tipo de entidad esperado y de dónde sale (la propiedad de relación, según los modulo.json de
crear-entidad, o el registro Enlaces_Pendientes) y los módulos que pueden crearlo. Primero van
los que no tienen tipo, que hay que asignar con pending_links.py --set.

Ejemplos:  find_gaps.py     find_gaps.py --note Aldric_Voss     find_gaps.py --link Puerto_Viejo"""
import argparse
import json
import sys
from pathlib import Path

# La lógica vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import DEFAULT_EXCLUDED, describe_expected, find_gaps  # noqa: E402
from vault_lib import vault_path  # noqa: E402

TYPED_BY = {"propiedad": "por su propiedad", "registro": "por el registro"}


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--note", help="Solo los enlaces pendientes de las notas cuya ruta o nombre contenga este texto")
    parser.add_argument("--link", help="Solo el enlace pendiente con este nombre (contexto completo)")
    parser.add_argument("--include-all", action="store_true", help="Incluye plantillas y archivados")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")

    gaps, malformed = find_gaps(vault, () if args.include_all else DEFAULT_EXCLUDED)
    if args.link:
        gaps = [g for g in gaps if g["link"].lower() == args.link.strip().strip("[]").lower()]
    if args.note:
        needle = args.note.lower()
        for gap in gaps:
            gap["occurrences"] = [o for o in gap["occurrences"] if needle in o["note"].lower()]
        gaps = [g for g in gaps if g["occurrences"]]
        malformed = [m for m in malformed if needle in m["note"].lower()]

    if args.json:
        print(json.dumps({"gaps": gaps, "malformed_links": malformed}, ensure_ascii=False, indent=2))
        return
    untyped = [g for g in gaps if not g["expected_type"]]
    typed = sorted((g for g in gaps if g["expected_type"]), key=lambda g: (g["expected_type"], g["link"].lower()))
    print(f"Enlaces pendientes: {len(gaps)} | sin tipo: {len(untyped)}")
    for heading, group in (("SIN TIPO (asígnaselo con pending_links.py --set <Enlace>=<tipo>)", untyped),
                           ("CON TIPO", typed)):
        if group:
            print(f"\n== {heading} ==")
        for gap in group:
            origin = f", {TYPED_BY[gap['typed_by']]}" if gap.get("typed_by") in TYPED_BY else ""
            print(f"\n[[{gap['link']}]] → tipo esperado: {describe_expected(gap)}{origin}")
            for o in gap["occurrences"]:
                where = f"propiedad `{o['property']}`" if o["property"] else f"sección «{o['section']}»"
                print(f"   · {o['note']} — {where}")
    for item in malformed:
        print(f"\nAVISO: enlace mal formado en {item['note']}: {item['line']}")


if __name__ == "__main__":
    main()
