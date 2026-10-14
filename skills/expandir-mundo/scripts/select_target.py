#!/usr/bin/env python3
"""Elige qué desarrollar en el próximo ciclo de expandir-mundo, según el estado del mundo.

Arranque: si la Ficha nombra un foco que aún no existe como lugar (una región, por ejemplo),
lo primero es crearlo (acción crear_foco); lo demás se generará dentro. --skip-focus lo omite.

Enlaces pendientes: las entidades que alguna nota ya nombra con un enlace y que todavía no tienen
nota propia. Se pueden crear los que tienen tipo (por su propiedad de relación o por el registro
Enlaces_Pendientes) y un módulo que los cree. Quedan fuera los que esperan una confirmación
("- [ ] Confirmar: …") en Preguntas Abiertas, los que se pasan con --skip (porque ningún módulo
encaja de verdad con ellos) y los que coinciden con el nombre o un alias de una entidad que ya
existe (son enlaces que hay que corregir).
  - Canon de base (acción crear_canon): los que nombra la Ficha o enlazan al menos tres notas,
    como el conflicto central, la especie o el gran hecho. Van antes que todo lo demás;
    --skip-canon lo omite.
  - Completar (acción completar_hueco): los demás. Puntúan más los que nombran más notas, los
    que nombran notas más relevantes y los que están dentro del foco de la Ficha.
  - Crear algo nuevo: un paquete de Paquetes.md cuyos tipos tienen todos módulo (acción paquete)
    o una entidad suelta (acción nueva_entidad).

Profundizar (acción profundizar): la relevancia decide cuánto desarrollo lleva una nota. Una nota en
borrador se puede profundizar si la nombran tantas notas que su relevancia se quedó corta (3 notas
piden relevancia 3; 6, relevancia 4; 10, relevancia 5) o si su relevancia ya pide secciones que no
tiene (porque el usuario la subió). Con --deepen-chance, el ciclo profundiza en vez de completar o
crear; las notas en canon no se tocan.

Cartografiar (acción cartografiar): un lugar con leyenda al que le toca dibujar su mapa, la primera
edición (una región que ya tiene las zonas mínimas) o una nueva (3 zonas sin cartografiar o más, o un
cuarto de las cartografiadas). Con --map-chance, el ciclo cartografía en vez de completar o crear;
--no-maps lo omite (en una tanda sin imágenes).

Conectar (acción conectar): lo que debería estar unido por una ruta y no lo está (dos asentamientos
vecinos sin camino, un asentamiento importante sin camino a la capital de su región, dos regiones vecinas
que ninguna ruta une, un lugar importante al que no llega nada; routes.py --unconnected). Con
--connect-chance, el ciclo crea la ruta que los une en vez de completar o crear otra cosa; como crear
algo nuevo, se hace menos cuando hay muchos enlaces pendientes por entidad. Con 1, siempre que haya algo
que unir.

Equilibrio: la densidad es la cantidad de enlaces pendientes que se pueden crear por entidad (los
secretos no cuentan como entidades).
Con poca densidad se crea algo nuevo con la probabilidad de --new-chance y cada nota puede abrir
bastantes enlaces pendientes nuevos (presupuesto amplio); con mucha, casi siempre se completa lo
pendiente y cada nota abre los mínimos (presupuesto justo). Así el mundo no se llena de enlaces
vacíos ni se queda sin hilos de los que tirar. El presupuesto se traduce en un rango de enlaces
pendientes nuevos por nota para cada tipo (enlaces_nuevos), dentro de su huecos_propios.

El objetivo se sortea entre los mejores, con peso según la puntuación y los empates decididos al
azar, para que el mundo no crezca siempre por el mismo sitio. Si hay demasiados borradores
procedurales sin revisar, se detiene (código 2).

Ejemplos:  select_target.py     select_target.py --json --seed 7     select_target.py --skip Aldea_de_X"""
import argparse
import json
import random
import re
import sys
from pathlib import Path

# La lógica común vive en los scripts de crear-entidad
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "crear-entidad" / "scripts"))
from build_context import region_chain  # noqa: E402
from vault_lib import place_types as containing_types  # noqa: E402
from vault_lib import (ROUTE_TYPE, SKILL_DIR, WORLD_SHEET, blocked_links, connection_candidates,  # noqa: E402
                       describe_expected, find_gaps,
                       load_index, load_modules, map_applies, map_key_problems, map_status, normalize,
                       omitted_sections, parse_map_key, parse_map_routes, read_world, split_note,
                       template_sections, without_secrets)
from vault_lib import vault_path  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"
VAULT_PACKAGES = "00_Sistema/06_Generacion/Paquetes.md"
TOP_DRAW = 8
# Topes de la salida: en un mundo grande, las listas completas gastarían tokens sin aportar nada
MAX_SKIPPED = 10
MAX_NAMERS = 5
# Canon de base: los enlaces pendientes que nombran al menos tantas notas de entidades
CANON_NOTES = 3
# Qué puede ser el foco según la escala de la Ficha: en un mundo que es una sola ciudad, la ciudad (o un sitio
# como una estación, un barco o una mazmorra); en uno que es una sola región, la región; en los demás, cualquier
# lugar que contenga a otros
FOCUS_TYPES = {"ciudad": ["asentamiento", "lugar"], "region": ["region"]}
# Densidad (enlaces pendientes que se pueden crear por entidad): por debajo de la baja, presupuesto
# amplio y la probabilidad entera de crear algo nuevo; desde la alta, presupuesto justo y solo una
# parte de esa probabilidad. Simulado, el mundo se estabiliza en torno a la alta
DENSITY_LOW, DENSITY_HIGH = 0.75, 1.5
NEW_FLOOR = 0.4
# De lo nuevo, la parte que va a paquetes (el resto, una entidad suelta)
PACKAGE_SHARE = 0.6
BUDGETS = ("justo", "medio", "amplio")
# Profundizar: cuántas notas que la nombran piden cada relevancia (de mayor a menor)
RELEVANCE_BY_LINKERS = ((10, 5), (6, 4), (3, 3))


def map_candidates(vault, index, modules):
    """Lugares con leyenda a los que les toca dibujar el mapa: la primera edición o una nueva."""
    options = []
    for entry in index:
        module = modules.get(entry["tipo"])
        relevance = entry.get("relevancia")
        if not module or not module.get("mapa") or entry["estado"] == "archivado" \
                or not map_applies(module, entry["props"], relevance):
            continue
        _, body = split_note((vault / entry["path"]).read_text(encoding="utf-8"))
        zones, problems = parse_map_key(body)
        if zones is None or problems or map_key_problems(zones)[0]:
            continue
        routes, _ = parse_map_routes(body)
        status = map_status(module, entry["props"], zones, relevance, routes)
        if not status["toca"]:
            continue
        first_edition = status["toca"] == "primera"
        options.append({"accion": "cartografiar", "nota": entry["name"], "tipo": entry["tipo"],
                        "clase": status["clase"], "edicion": "primera" if first_edition else "nueva",
                        "niveles": status["niveles"],
                        "puntos": relevance + status["sin_cartografiar"] + status["rutas_sin_cartografiar"]
                        + (3 if first_edition else 0),
                        "razones": [status["razon"], f"relevancia {relevance}"]})
    return options


def deepen_candidates(vault, index, modules):
    """Notas en borrador a las que les faltan secciones: por la relevancia que piden las notas que
    las nombran o por la que ya tienen. Cada una con su relevancia nueva y las secciones que faltan."""
    linkers = {}
    for entry in index:
        for target in entry["enlaces"]:
            if target.lower() != entry["name"].lower():
                linkers.setdefault(target.lower(), set()).add(entry["name"])
    templates, options = {}, []
    for entry in index:
        module = modules.get(entry["tipo"])
        current = entry.get("relevancia")
        if entry["estado"] != "borrador" or not module or not current:
            continue
        named_by = len(linkers.get(entry["name"].lower(), ()))
        target = max([current] + [r for n, r in RELEVANCE_BY_LINKERS if named_by >= n][:1])
        if entry["tipo"] not in templates:
            path = SKILL_DIR / "tipos" / entry["tipo"] / "plantilla.md"
            templates[entry["tipo"]] = split_note(path.read_text(encoding="utf-8"))[1]
        template = templates[entry["tipo"]]
        _, body = split_note((vault / entry["path"]).read_text(encoding="utf-8"))
        present = {line.strip() for line in body}
        skipped = set(omitted_sections(module, template, target, entry["props"]))
        missing = [title for level, title in template_sections(template)
                   if title not in skipped and f"{'#' * level} {title}" not in present]
        if not missing:
            continue
        reasons = [f"la nombran {named_by} nota(s)"] + (
            [f"eso pide relevancia {target} (tiene {current})"] if target > current else
            [f"su relevancia {current} ya pide secciones que no tiene"])
        options.append({"accion": "profundizar", "nota": entry["name"], "tipo": entry["tipo"],
                        "relevancia_actual": current, "relevancia_nueva": target, "secciones": missing,
                        "puntos": named_by + 2 * (target - current) + len(missing) // 3, "razones": reasons})
    return options


def find_focus(world, index, place_types):
    """Lugar foco de la Ficha: el lugar cuyo título o alias aparece en el texto del foco."""
    focus_text = normalize(world["foco"])
    if not focus_text:
        return None
    best = None
    for entry in index:
        if entry["tipo"] not in place_types:
            continue
        for name in [entry["titulo"]] + entry["aliases"]:
            key = normalize(name)
            if key and key in focus_text and (best is None or len(key) > best[0]):
                best = (len(key), entry)
    return best[1] if best else None


def in_focus(entry, focus, by_name):
    if not focus or not entry:
        return False
    if entry["name"] == focus["name"]:
        return True
    return any(region["name"] == focus["name"] for region in region_chain(entry, by_name, set()))


def shuffle_ties(options, rng):
    """Ordena de más a menos puntos; a igual puntuación, al azar (repetible con la semilla).
    Ordenar sin barajar dejaría los empates por orden alfabético, y siempre entrarían antes los
    mismos."""
    rng.shuffle(options)
    options.sort(key=lambda option: -option["puntos"])


def words(text):
    """Texto comparable palabra a palabra: normalizado, sin signos y con espacios en los extremos."""
    return f" {' '.join(re.sub(r'[^0-9a-z]+', ' ', normalize(text)).split())} "


def budget_for(density):
    if density < DENSITY_LOW:
        return "amplio"
    return "medio" if density < DENSITY_HIGH else "justo"


def new_links_range(module, budget):
    """(mínimo, máximo) de enlaces pendientes nuevos por nota con un presupuesto: el tercio bajo,
    el medio o el alto del rango huecos_propios del módulo."""
    low, high = module["huecos_propios"]["min"], module["huecos_propios"]["max"]
    cuts = [low, low + round((high - low) / 3), low + round(2 * (high - low) / 3), high]
    step = BUDGETS.index(budget)
    return cuts[step], cuts[step + 1]


def parse_packages(vault):
    path = vault / VAULT_PACKAGES
    path = path if path.is_file() else ASSETS / "Paquetes.md"
    packages, current = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            current = {"nombre": heading.group(1).strip(), "peso": 1, "composicion": []}
            packages.append(current)
            continue
        if not current:
            continue
        weight = re.match(r"^Peso:\s*(\d+)", line.strip())
        item = re.match(r"^-\s*([a-z_]+):\s*(\d+)\s*(?:\((.+)\))?", line.strip())
        if weight:
            current["peso"] = int(weight.group(1))
        elif item:
            current["composicion"].append({"tipo": item.group(1), "cantidad": int(item.group(2)),
                                           "papel": item.group(3) or ""})
    return [p for p in packages if p["composicion"]]


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--review-limit", type=int, default=20,
                        help="Borradores procedurales sin revisar a partir de los cuales se detiene (20)")
    parser.add_argument("--new-chance", type=float, default=0.4,
                        help="Probabilidad de crear algo nuevo (un paquete o una entidad suelta) en vez de completar "
                             "un enlace pendiente cuando hay pocos por entidad (0.4); con muchos baja hasta el 40 %% "
                             "de ese valor")
    parser.add_argument("--skip-focus", action="store_true",
                        help="No proponer crear el foco aunque falte (si ningún módulo encaja con él)")
    parser.add_argument("--skip", action="append", default=[], metavar="ENLACE",
                        help="Enlace pendiente que no se debe elegir (repetible), si ningún módulo encaja con él")
    parser.add_argument("--skip-canon", action="store_true",
                        help="No dar prioridad al canon de base pendiente")
    parser.add_argument("--deepen-chance", type=float, default=0.25,
                        help="Probabilidad de profundizar una nota que lo necesita en vez de completar o crear (0.25)")
    parser.add_argument("--map-chance", type=float, default=0.25,
                        help="Probabilidad de dibujar un mapa que toca en vez de completar o crear (0.25)")
    parser.add_argument("--no-maps", action="store_true", help="No proponer mapas (en una tanda sin imágenes)")
    parser.add_argument("--connect-chance", type=float, default=0.2,
                        help="Probabilidad de unir con una ruta lo que debería estar unido y no lo está, en vez de "
                             "completar o crear (0.2); con muchos enlaces pendientes baja como la de crear algo nuevo; con 1, "
                             "siempre que haya algo que unir")
    parser.add_argument("--seed", type=int, help="Semilla para repetir la elección")
    parser.add_argument("--top", type=int, default=5, help="Cuántos candidatos mostrar")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    seed = args.seed if args.seed is not None else random.SystemRandom().randrange(10 ** 9)
    rng = random.Random(seed)
    index = load_index(vault)
    by_name = {e["name"].lower(): e for e in index}
    by_path = {e["path"]: e for e in index}
    modules = load_modules()
    world = read_world(vault)
    # El foco es un lugar donde se genera lo demás (una región, una ciudad); una ruta o un ecosistema no
    # contienen nada (`contenedor: false`)
    place_types = sorted(containing_types(modules))
    focus = find_focus(world, index, place_types)
    # La escala de la Ficha: en un mundo que es una sola ciudad, el foco es esa ciudad (o un sitio, como una
    # estación o una mazmorra) y ninguna región cabe en él; en uno que es una sola región, el foco es la región
    scale = world["escala"]
    out_of_scale = {"region"} if scale == "ciudad" else set()
    focus_types = [t for t in FOCUS_TYPES.get(scale, place_types) if t in place_types] or place_types

    def finish(result, code=0, types=()):
        if "presupuesto" in result:
            ranges = {t: new_links_range(modules[t], result["presupuesto"]) for t in dict.fromkeys(types)
                      if t in modules}
            result["enlaces_nuevos"] = {t: f"{low}–{high}" for t, (low, high) in ranges.items()}
            if ranges:
                result["detalle"].append("enlaces pendientes nuevos por nota: "
                                         + ", ".join(f"{t} {v}" for t, v in result["enlaces_nuevos"].items()))
        result["semilla"] = seed
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result["resumen"])
            for line in result.get("detalle", []):
                print(f"  {line}")
            print(f"  (semilla {seed})")
        sys.exit(code)

    # Límite de revisión: no construir sobre demasiados borradores sin revisar
    pending = sum(1 for e in index if e["estado"] == "borrador" and e["origen"] == "procedural")
    if pending > args.review_limit:
        finish({"accion": "detener", "borradores_pendientes": pending,
                "resumen": f"DETENER: hay {pending} borradores procedurales sin revisar "
                           f"(límite {args.review_limit}). Revísalos antes de seguir generando."}, 2)

    blocked = blocked_links(vault)
    excluded = {name.strip().strip("[]").lower() for name in args.skip}
    gaps, _ = find_gaps(vault)
    sheet = vault / WORLD_SHEET
    sheet_words = words(sheet.read_text(encoding="utf-8")) if sheet.is_file() else ""

    # Un enlace pendiente que coincide con el nombre o un alias de una entidad que ya existe no se
    # crea: es un enlace que hay que corregir
    known = {}
    for entry in index:
        for label in [entry["titulo"], *entry["aliases"]]:
            if label:
                known.setdefault(normalize(label), entry["name"])

    # Enlaces pendientes que se pueden crear. El canon de base (lo que nombra la Ficha o enlazan
    # varias notas: el conflicto central, la especie, el gran hecho) va antes que los demás
    references, candidates, skipped = [], [], []
    for gap in gaps:
        link, key = gap["link"], gap["link"].lower()
        alias_of = known.get(normalize(link))
        if alias_of:
            skipped.append(f"[[{link}]]: es otro nombre de [[{alias_of}]]; corrige el enlace")
        elif key in excluded:
            skipped.append(f"[[{link}]]: descartado con --skip")
        elif not gap["expected_type"]:
            skipped.append(f"[[{link}]]: sin tipo (asígnaselo con pending_links.py --set {link}=<tipo>)")
        elif not gap["expected_modules"]:
            skipped.append(f"[[{link}]]: {describe_expected(gap)}")
        elif not set(gap["expected_modules"]) - out_of_scale:
            skipped.append(f"[[{link}]]: una región no cabe en un mundo que es una sola ciudad (si es de fuera, "
                           f"márcalo con pending_links.py --set {link}=fuera)")
        elif key in blocked:
            skipped.append(f"[[{link}]]: espera una confirmación en Preguntas Abiertas")
        else:
            linkers = sorted((by_path[n] for n in gap["notes"] if n in by_path),
                             key=lambda e: -(e.get("relevancia") or 2))
            notes = len(gap["notes"])
            option = {"tipo_esperado": gap["expected_type"],
                      "modulos": [m for m in gap["expected_modules"] if m not in out_of_scale],
                      "nombrado_por": [e["name"] for e in linkers[:MAX_NAMERS]]}
            in_sheet = bool(sheet_words) and words(link) in sheet_words
            if in_sheet or notes >= CANON_NOTES:
                reasons = [f"lo nombran {notes} nota(s)"] + (["lo nombra la Ficha"] if in_sheet else [])
                references.append({"accion": "crear_canon", "referencia": link, **option,
                                   "puntos": 3 * notes + 2 + (3 if in_sheet else 0),
                                   "razones": reasons + ["canon de base"]})
                continue
            relevance = (linkers[0].get("relevancia") or 2) if linkers else 2
            focused = any(in_focus(e, focus, by_name) for e in linkers)
            reasons = [f"lo nombran {notes} nota(s)", f"relevancia {relevance} de la más importante"]
            if focused:
                reasons.append("está en el foco")
            candidates.append({"accion": "completar_hueco", "hueco": link, **option,
                               "puntos": 2 * notes + relevance + (3 if focused else 0), "razones": reasons})
    shuffle_ties(references, rng)
    shuffle_ties(candidates, rng)

    # Equilibrio entre crear de la nada y completar lo pendiente, según la densidad
    entities = len(without_secrets(index))
    density = (len(references) + len(candidates)) / max(entities, 1)
    budget = budget_for(density)
    factor = min(max((DENSITY_HIGH - density) / (DENSITY_HIGH - DENSITY_LOW), 0.0), 1.0)
    new_chance = args.new_chance * (NEW_FLOOR + (1 - NEW_FLOOR) * factor)
    balance = [f"densidad: {density:.1f} enlaces pendientes que se pueden crear por entidad "
               f"({len(references) + len(candidates)} para {entities} entidades) · presupuesto {budget} · "
               f"probabilidad de crear algo nuevo {new_chance:.0%}"]
    if skipped:
        balance.append(f"descartados: {len(skipped)} (sin tipo, sin módulo, pendientes de confirmar, "
                       f"alias o con --skip)")
    common = {"densidad": round(density, 2), "presupuesto": budget, "borradores_pendientes": pending,
              "descartados": skipped[:MAX_SKIPPED], "descartados_total": len(skipped)}

    # Arranque: la Ficha nombra un foco que aún no existe; se crea antes que nada. Si la Ficha ya lo enlaza
    # (en «Lo que ya tiene nombre»), se crea completando ese enlace, con su tipo
    if world["foco"] and not focus and place_types and not args.skip_focus:
        sheet_gap = next((g for g in gaps if set(g["expected_modules"]) & set(focus_types)
                          and words(g["link"]) in words(world["foco"])
                          and any(o["note"] == WORLD_SHEET for o in g["occurrences"])), None)
        types = [t for t in sheet_gap["expected_modules"] if t in focus_types] if sheet_gap else focus_types
        finish({"accion": "crear_foco", "foco_texto": world["foco"], "modulos": types,
                **({"hueco": sheet_gap["link"]} if sheet_gap else {}), **common,
                "resumen": f"ELEGIDO: crear el foco de la Ficha, «{world['foco']}» "
                           + (f"completando su enlace [[{sheet_gap['link']}]] " if sheet_gap else "")
                           + f"(módulos: {', '.join(types)}); lo demás se generará dentro de él",
                "detalle": balance}, types=types)

    # Un paquete crea sus entidades de la nada: no vale si incluye un tipo sin módulo o con crear_desde_cero: false
    available = [p for p in parse_packages(vault)
                 if all(modules.get(i["tipo"], {}).get("crear_desde_cero", i["tipo"] in modules)
                        and i["tipo"] not in out_of_scale for i in p["composicion"])]
    create_new = not candidates or rng.random() < new_chance
    deepen = deepen_candidates(vault, index, modules)
    shuffle_ties(deepen, rng)
    if deepen:
        balance.append(f"notas que piden más profundidad: {len(deepen)} · probabilidad de profundizar "
                       f"{args.deepen_chance:.0%}")
    maps = [] if args.no_maps else map_candidates(vault, index, modules)
    shuffle_ties(maps, rng)
    if maps:
        balance.append(f"mapas por dibujar: {len(maps)} · probabilidad de cartografiar {args.map_chance:.0%}")
    # Lo que debería estar unido por una ruta y no lo está; lo del foco, antes
    connections = []
    if ROUTE_TYPE in modules and modules[ROUTE_TYPE].get("crear_desde_cero", True):
        connections = connection_candidates(vault, index)
        for option in connections:
            ends = [by_name.get(name.lower()) for name in (option["partida"], option["destino"]) if name]
            if any(in_focus(entry, focus, by_name) for entry in ends if entry):
                option["puntos"] += 3
                option["razones"].append("está en el foco")
        shuffle_ties(connections, rng)
    # Con 1 (o más), siempre que haya algo que unir; por debajo, baja con los enlaces pendientes, como lo nuevo
    connect_chance = 1.0 if args.connect_chance >= 1 else args.connect_chance * (NEW_FLOOR + (1 - NEW_FLOOR) * factor)
    if connections:
        balance.append(f"lugares por unir con una ruta: {len(connections)} · probabilidad de conectar "
                       f"{connect_chance:.0%}")
    if references and not args.skip_canon:
        pool = references[:TOP_DRAW]
        chosen = rng.choices(pool, weights=[r["puntos"] for r in pool])[0]
        finish({**chosen, **common,
                "resumen": f"ELEGIDO: crear [[{chosen['referencia']}]] → {chosen['tipo_esperado']} "
                           f"(módulos: {', '.join(chosen['modulos'])}): canon de base · {chosen['puntos']} puntos",
                "detalle": [f"razones: {'; '.join(chosen['razones'])}", "canon de base pendiente:"]
                           + [f"  {r['puntos']:>3} pts  [[{r['referencia']}]] → {r['tipo_esperado']}"
                              for r in references[:args.top]] + balance},
               types=chosen["modulos"])
    if maps and rng.random() < args.map_chance:
        pool = maps[:TOP_DRAW]
        chosen = rng.choices(pool, weights=[m["puntos"] for m in pool])[0]
        finish({**chosen, **common,
                "resumen": f"ELEGIDO: cartografiar [[{chosen['nota']}]] ({chosen['tipo']}, mapa {chosen['clase']}): "
                           f"{chosen['edicion']} edición · {chosen['puntos']} puntos",
                "detalle": [f"razones: {'; '.join(chosen['razones'])}",
                            f"niveles que dibujar: {', '.join(map(str, chosen['niveles']))}",
                            "mapas por dibujar:"]
                           + [f"  {m['puntos']:>3} pts  [[{m['nota']}]] ({m['edicion']} edición)"
                              for m in maps[:args.top]] + balance})
    if deepen and rng.random() < args.deepen_chance:
        pool = deepen[:TOP_DRAW]
        chosen = rng.choices(pool, weights=[d["puntos"] for d in pool])[0]
        finish({**chosen, **common,
                "resumen": f"ELEGIDO: profundizar [[{chosen['nota']}]] ({chosen['tipo']}), relevancia "
                           f"{chosen['relevancia_actual']} → {chosen['relevancia_nueva']} · {chosen['puntos']} puntos",
                "detalle": [f"razones: {'; '.join(chosen['razones'])}",
                            "secciones que añadir: " + ", ".join(f"«{t}»" for t in chosen["secciones"]),
                            "notas que piden más profundidad:"]
                           + [f"  {d['puntos']:>3} pts  [[{d['nota']}]] {d['relevancia_actual']} → "
                              f"{d['relevancia_nueva']}" for d in deepen[:args.top]] + balance},
               types=[chosen["tipo"]])
    if connections and rng.random() < connect_chance:
        pool = connections[:TOP_DRAW]
        chosen = rng.choices(pool, weights=[c["puntos"] for c in pool])[0]
        ends = f"[[{chosen['partida']}]]" + (f" y [[{chosen['destino']}]]" if chosen["destino"] else "")
        finish({"accion": "conectar", **chosen, **common,
                "resumen": f"ELEGIDO: conectar {ends} con una ruta ({chosen['motivo']}) · {chosen['puntos']} puntos",
                "detalle": [f"razones: {'; '.join(chosen['razones'])}", "lugares por unir:"]
                           + [f"  {c['puntos']:>3} pts  {c['motivo']:<9} [[{c['partida']}]]"
                              + (f" ↔ [[{c['destino']}]]" if c["destino"] else "") for c in connections[:args.top]]
                           + balance},
               types=[ROUTE_TYPE])
    if create_new and available and rng.random() < PACKAGE_SHARE:
        package = rng.choices(available, weights=[p["peso"] for p in available])[0]
        why = "no hay enlaces pendientes que se puedan crear" if not candidates else "toca crear algo nuevo"
        finish({"accion": "paquete", "paquete": package["nombre"], "composicion": package["composicion"],
                "foco": focus["name"] if focus else None, **common,
                "resumen": f"ELEGIDO: paquete «{package['nombre']}»"
                           + (f" en el foco [[{focus['name']}]]" if focus else "") + f" ({why})",
                "detalle": [f"- {i['tipo']} ×{i['cantidad']} ({i['papel']})" for i in package["composicion"]]
                           + balance},
               types=[i["tipo"] for i in package["composicion"]])
    if not create_new:
        pool = candidates[:TOP_DRAW]
        chosen = rng.choices(pool, weights=[c["puntos"] for c in pool])[0]
        finish({**chosen, **common,
                "resumen": f"ELEGIDO: completar [[{chosen['hueco']}]] → {chosen['tipo_esperado']} "
                           f"(módulos: {', '.join(chosen['modulos'])}) · {chosen['puntos']} puntos",
                "detalle": [f"razones: {'; '.join(chosen['razones'])}", "enlaces pendientes principales:"]
                           + [f"  {c['puntos']:>3} pts  [[{c['hueco']}]] → {c['tipo_esperado']}"
                              for c in candidates[:args.top]] + balance},
               types=chosen["modulos"])
    # Los secretos y los tipos con crear_desde_cero: false (las especies, por ejemplo) no se inventan
    types = sorted(t for t, module in modules.items()
                   if t != "secreto" and module.get("crear_desde_cero", True) and t not in out_of_scale)
    new_type = rng.choice(types)
    why = "no hay enlaces pendientes que se puedan crear" if not candidates else "toca crear algo nuevo"
    # Una ruta nueva nunca sale de la nada: une lo que más lo necesita, o parte de un lugar que ya existe
    anchor = {"conexion": {k: connections[0][k] for k in ("motivo", "partida", "destino")}} \
        if new_type == ROUTE_TYPE and connections else {}
    finish({"accion": "nueva_entidad", "tipo": new_type, "foco": focus["name"] if focus else None, **anchor, **common,
            "resumen": f"ELEGIDO: nueva entidad de tipo {new_type}"
                       + (f" en el foco [[{focus['name']}]]" if focus else "") + f" ({why})",
            "detalle": balance}, types=[new_type])


if __name__ == "__main__":
    main()
