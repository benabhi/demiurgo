#!/usr/bin/env python3
"""Muestra los calendarios del mundo y escribe o convierte fechas con sus nombres.

Sin opciones, resume el calendario de referencia (el eje de la Ficha) y lista los demás, con su
año actual. Las fechas exactas se escriben «<día> de <mes> de <año>», con los nombres del
calendario; los años de las propiedades (`nacimiento`, `inicio`…) son siempre los del eje.

Ejemplos:  world_calendar.py
           world_calendar.py --calendar Calendario_de_Ejemplo
           world_calendar.py --year 412                       (ese año del eje en cada calendario)
           world_calendar.py --date "15 de Siega de 412 UE"   (valida la fecha y la convierte)"""
import argparse
import json
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (calendar_summary, format_date, format_year, load_calendars, normalize,  # noqa: E402
                       parse_exact_date, read_world, reference_calendar)


def find_calendar(calendars, name):
    """El calendario cuyo archivo, título o nombre normalizado coincide con `name`, o None."""
    key = normalize(name.strip().strip("[]"))
    return next((c for c in calendars if key in (normalize(c["nombre"]), normalize(c["titulo"]))), None)


def other_years(calendars, chosen, axis_year):
    """El mismo año del eje en los demás calendarios."""
    return [f"[[{c['nombre']}]]: {format_year(c, axis_year)}" for c in calendars if c is not chosen]


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--calendar", help="Calendario que se usa (por defecto, el de referencia)")
    parser.add_argument("--year", type=int, help="Año del eje que se muestra en cada calendario")
    parser.add_argument("--date", help="Fecha que se valida y se convierte: «15 de Siega de 412 UE»")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    calendars = load_calendars(vault)
    world_year = read_world(vault)["ano_actual"]
    if not calendars:
        print("No hay calendarios en la bóveda. El de referencia se crea con `/crear-entidad calendario`.")
        return
    reference = reference_calendar(calendars)
    chosen = find_calendar(calendars, args.calendar) if args.calendar else reference
    if args.calendar and not chosen:
        names = ", ".join(c["nombre"] for c in calendars)
        sys.exit(f"Error: no encuentro el calendario «{args.calendar}» (hay: {names}).")
    if not chosen:
        sys.exit("Error: ningún calendario es el de referencia (`referencia: true`); indica uno con --calendar.")
    # Ordena: el elegido primero y después el de referencia
    calendars = [chosen] + [c for c in calendars if c is not chosen]

    if args.date:
        parsed, problem = parse_exact_date(args.date, chosen)
        if problem:
            sys.exit(f"Fecha no válida en [[{chosen['nombre']}]]: {problem}")
        axis_year, month, day = parsed
        result = {"fecha": format_date(chosen, axis_year, month, day), "ano_eje": axis_year, "mes": month,
                  "dia": day, "otros_calendarios": other_years(calendars, chosen, axis_year)}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        print(f"Fecha válida en [[{chosen['nombre']}]]: {result['fecha']} (año {axis_year} del eje, mes {month}, día {day})")
        for line in result["otros_calendarios"]:
            print(f"- Ese año en {line} (cada calendario empieza el año a su manera: solo se convierte el año)")
        return

    if args.year is not None:
        lines = [f"[[{c['nombre']}]]: {format_year(c, args.year)}" for c in calendars]
        if args.json:
            print(json.dumps({"ano_eje": args.year, "calendarios": lines}, ensure_ascii=False, indent=2))
            return
        print(f"El año {args.year} del eje:")
        for line in lines:
            print(f"- {line}")
        return

    if args.json:
        print(json.dumps({"ano_actual": world_year, "calendarios": calendars}, ensure_ascii=False, indent=2))
        return
    role = "calendario de referencia" if chosen["referencia"] else f"calendario (año 0 = año {chosen['ano_cero']} del eje)"
    print(f"# {chosen['titulo']} — {role}: [[{chosen['nombre']}]]")
    for line in calendar_summary(chosen, world_year):
        print(line)
    if chosen["errores"]:
        print(f"- Errores de estructura: {len(chosen['errores'])} (revísalos con check_note.py {chosen['nombre']})")
    others = calendars[1:]
    if others:
        print("\n## Otros calendarios")
        for calendar in others:
            present = f"año actual {format_year(calendar, world_year)}" if world_year is not None else "año actual por definir"
            kind = "referencia" if calendar["referencia"] else f"año 0 = año {calendar['ano_cero']} del eje"
            print(f"- [[{calendar['nombre']}]] — {calendar['titulo']} ({kind}; {present})")


if __name__ == "__main__":
    main()
