#!/usr/bin/env python3
"""Las rutas del mundo como un grafo de distancias, para que lo nuevo respete lo que ya se sabe.

Cada ruta (nota de tipo ruta) da sus tramos en la tabla «Recorrido», con los días de cada uno por su medio
habitual. Solo cuentan las rutas ciertas que se pueden recorrer hoy (en uso o en declive), y cada una se
recorre en los dos sentidos. Un lugar sin rutas propias se alcanza por el sitio que lo contiene (la
taberna, por su ciudad).

  routes.py <Lugar>          las rutas que pasan por él y lo más cercano, con los días
  routes.py <A> <B>          el camino más rápido conocido entre dos lugares, o que no hay ninguno
  routes.py --unconnected    lo que debería estar unido y no lo está (vecinos sin camino, lo importante de
                             una región sin camino a su capital, regiones vecinas sin ruta, lugares a los
                             que no llega nada): lo que el motor une con la acción `conectar`
Con --all cuentan también las rutas que hoy no se recorren (cortadas, abandonadas, perdidas o dudosas).

Ejemplos:  routes.py Ciudad_de_Ejemplo   routes.py Aldea_A "Puerto Viejo"   routes.py --unconnected --top 10"""
import argparse
import json
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (connection_candidates, days_value, first, format_days, load_index,  # noqa: E402
                       nearest_places, normalize, place_node, route_components, route_graph, route_usable,
                       shortest_route)
from vault_lib import vault_path  # noqa: E402

MAX_NEAREST = 6


def find_place(text, by_name, by_label, graph):
    """Clave del lugar (nombre de su nota en minúsculas, o el de un enlace pendiente que es extremo de una
    ruta) a partir de su nombre de archivo, su título o un alias. None si no aparece."""
    raw = text.strip().strip("[]").split("|")[0].strip()
    for key in (raw.lower(), raw.replace(" ", "_").lower()):
        if key in by_name or key in graph:
            return key
    entry = by_label.get(normalize(raw))
    return entry["name"].lower() if entry else None


def shown(key, by_name, points):
    """Un nodo para mostrar: enlace legible si es una nota o un enlace pendiente; si no, su texto."""
    entry = by_name.get(key)
    if entry:
        return f"[[{entry['name']}|{entry['titulo']}]]" if "_" in entry["name"] else f"[[{entry['name']}]]"
    point = points.get(key, {})
    target = point.get("enlace")
    if target:
        text = point.get("texto") or target.replace("_", " ")
        return f"[[{target}|{text}]]" if "_" in target else f"[[{target}]]"
    return point.get("texto") or key.split("#", 1)[-1]


def route_label(name, by_name):
    """La ruta enlazada, con su categoría, su medio y sus días de punta a punta."""
    entry = by_name.get(name.lower())
    if not entry:
        return f"[[{name}]]"
    props = entry["props"]
    total = days_value(first(props.get("dias")))
    details = [first(props.get("categoria")), first(props.get("medio")),
               format_days(total) if total not in (None, False) else ""]
    extra = ", ".join(d for d in details if d)
    link = f"[[{entry['name']}|{entry['titulo']}]]" if "_" in entry["name"] else f"[[{entry['name']}]]"
    return link + (f" ({extra})" if extra else "")


def group_path(path):
    """Agrupa los tramos seguidos de una misma ruta: [(desde, hasta, días, ruta, tramos)]."""
    groups = []
    for start, end, days, route in path:
        if groups and groups[-1][3] == route:
            first_start, _, total, _, count = groups[-1]
            groups[-1] = (first_start, end, total + days, route, count + 1)
        else:
            groups.append((start, end, days, route, 1))
    return groups


def place_report(key, graph, points, by_name, index, vault):
    lines = []
    node, via = place_node(key, graph, by_name)
    label = shown(key, by_name, points)
    if node is None:
        lines.append(f"Ninguna ruta que se recorra hoy pasa por {label}, ni por el sitio donde está.")
    else:
        if node != key:
            lines.append(f"Ninguna ruta pasa por {label}: se llega por {shown(node, by_name, points)} (donde está).")
        by_route = {}
        for other, days, route in graph.get(node, []):
            by_route.setdefault(route, []).append((other, days))
        lines.append(f"Rutas de {shown(node, by_name, points)}: {len(by_route)}")
        for route, neighbours in sorted(by_route.items()):
            near = " · ".join(f"{shown(o, by_name, points)} {format_days(d)}" for o, d in neighbours)
            lines.append(f"- {route_label(route, by_name)}: al lado, {near}")
        nearest = nearest_places(graph, node, MAX_NEAREST)
        if nearest:
            lines.append("Lo más cercano por las rutas: " + " · ".join(
                f"{shown(o, by_name, points)} {format_days(d)}" for o, d in nearest))
    # Las rutas que lo tocan pero hoy no se recorren (cortadas, abandonadas, perdidas, dudosas)
    full, _ = route_graph(vault, index, usable_only=False)
    idle = sorted({route for _, _, route in full.get(key, [])
                   if not route_usable(by_name.get(route.lower(), {}).get("props", {}))})
    if idle:
        lines.append("Rutas que hoy no se recorren: " + " · ".join(
            f"{route_label(r, by_name)} — {first(by_name[r.lower()]['props'].get('situacion'))}"
            + (", dudosa" if first(by_name[r.lower()]["props"].get("certeza")) == "dudosa" else "")
            for r in idle if r.lower() in by_name))
    return lines


def path_report(start, goal, graph, points, by_name):
    a, _ = place_node(start, graph, by_name)
    b, _ = place_node(goal, graph, by_name)
    label_a, label_b = shown(start, by_name, points), shown(goal, by_name, points)
    if a is None or b is None:
        missing = [label for label, node in ((label_a, a), (label_b, b)) if node is None]
        return [f"No hay camino conocido entre {label_a} y {label_b}: a {' ni a '.join(missing)} no llega "
                f"ninguna ruta que se recorra hoy."], None
    found = shortest_route(graph, a, b)
    if found is None:
        components = route_components(graph)
        if components.get(a) == components.get(b):
            return [f"{label_a} y {label_b} están unidos por rutas, pero en algún tramo no se sabe cuánto se "
                    f"tarda (días «?»)."], None
        return [f"No hay camino conocido entre {label_a} y {label_b}."], None
    days, path = found
    lines = [f"De {label_a} a {label_b}: {format_days(days)} por el camino más rápido conocido"]
    for first_start, end, total, route, count in group_path(path):
        stretch = f" ({count} tramos)" if count > 1 else ""
        lines.append(f"- {shown(first_start, by_name, points)} → {shown(end, by_name, points)}: {format_days(total)} "
                     f"por {route_label(route, by_name)}{stretch}")
    def text(key):
        return points.get(key, {}).get("texto", key)
    return lines, {"dias": days, "tramos": [{"desde": text(s), "hasta": text(e), "dias": d, "ruta": r}
                                            for s, e, d, r in path]}


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("places", nargs="*", metavar="LUGAR", help="Un lugar (sus rutas) o dos (el camino entre ellos)")
    parser.add_argument("--unconnected", action="store_true", help="Lo que debería estar unido y no lo está")
    parser.add_argument("--all", action="store_true",
                        help="Cuenta también las rutas que hoy no se recorren (cortadas, abandonadas, perdidas, dudosas)")
    parser.add_argument("--top", type=int, default=15, help="Cuántos resultados mostrar con --unconnected (15)")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    index = load_index(vault)
    by_name = {e["name"].lower(): e for e in index}
    by_label = {}
    for entry in index:
        for label in [entry["titulo"], entry["name"], *entry["aliases"]]:
            by_label.setdefault(normalize(label), entry)

    if args.unconnected:
        candidates = connection_candidates(vault, index)
        if args.json:
            print(json.dumps(candidates[:args.top], ensure_ascii=False, indent=2))
            return
        if not candidates:
            print("Todo lo importante está unido por alguna ruta.")
            return
        print(f"Lo que debería estar unido y no lo está ({len(candidates)}):")
        for c in candidates[:args.top]:
            ends = f"[[{c['partida']}]]" + (f" ↔ [[{c['destino']}]]" if c["destino"] else "")
            print(f"  {c['puntos']:>3} pts  {c['motivo']:<9} {ends}: {'; '.join(c['razones'])}")
        if len(candidates) > args.top:
            print(f"  … y {len(candidates) - args.top} más (--top)")
        return

    if not args.places or len(args.places) > 2:
        sys.exit("Error: indica un lugar (sus rutas), dos (el camino entre ellos) o --unconnected.")
    graph, points = route_graph(vault, index, usable_only=not args.all)
    keys = []
    for text in args.places:
        key = find_place(text, by_name, by_label, graph)
        if key is None:
            sys.exit(f"Error: «{text}» no es un lugar de la bóveda ni el extremo de ninguna ruta.")
        keys.append(key)
    if len(keys) == 1:
        lines = place_report(keys[0], graph, points, by_name, index, vault)
        if args.json:
            node, _ = place_node(keys[0], graph, by_name)
            print(json.dumps({"lugar": keys[0], "nodo": node,
                              "rutas": sorted({r for _, _, r in graph.get(node, [])}) if node else [],
                              "cercanos": [{"lugar": points.get(o, {}).get("texto", o), "dias": d}
                                           for o, d in (nearest_places(graph, node, MAX_NEAREST) if node else [])]},
                             ensure_ascii=False, indent=2))
            return
        print("\n".join(lines))
        return
    lines, data = path_report(keys[0], keys[1], graph, points, by_name)
    if args.json:
        print(json.dumps(data or {"dias": None, "tramos": [], "mensaje": lines[0]}, ensure_ascii=False, indent=2))
        return
    print("\n".join(lines))


if __name__ == "__main__":
    main()
