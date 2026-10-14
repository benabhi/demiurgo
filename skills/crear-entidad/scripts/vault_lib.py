"""Biblioteca común de los scripts de crear-entidad y expandir-mundo.

Lee la bóveda como la entiende Obsidian: enlaces, frontmatter, módulos de tipos, la Ficha
del Mundo y un índice compacto con una entrada por entidad. No tiene línea de comandos."""
import datetime
import heapq
import itertools
import json
import math
import re
import unicodedata
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"!?\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
LINK_WITH_ALIAS_RE = re.compile(r"!?\[\[([^\]|#^]+?)\\?(?:[#^][^\]|]*)?(?:\\?\|([^\]]*))?\]\]")
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*)\s*:")
KEY_LINE_RE = re.compile(r"^([A-Za-z_][\w-]*):(.*)$")
ITEM_LINE_RE = re.compile(r"^\s+-\s+(.*)$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
COMMENT_RE = re.compile(r"<!--.*?-->")
QUOTED_LINK_RE = re.compile(r'^"\[\[[^\]]+\]\]"$')
INT_RE = re.compile(r"^-?\d+$")
CONFIRM_RE = re.compile(r"^-\s*\[ \]\s*confirmar\b", re.IGNORECASE)
ATTACHMENT_RE = re.compile(r"\.(png|jpe?g|webp|gif|svg|bmp|pdf|mp3|wav|ogg|mp4|webm|canvas|base)$", re.IGNORECASE)
PLAIN_FORBIDDEN_START = tuple("[]{}&*!|>'\"%@`")
HIDDEN_DIRS = {".obsidian", ".trash"}
# Notas internas, que no son entidades: los MOC, la Ficha, Preguntas Abiertas y los registros (`meta`)
SYSTEM_TYPES = {"moc", "meta", "ficha_mundo"}
# Las bóvedas creadas antes del módulo `sistema` daban ese tipo a sus notas internas de 00_Sistema
LEGACY_SYSTEM_TYPE = "sistema"
VARIATION_SELECTOR = chr(0xFE0F)
WORLD_SHEET = "00_Sistema/Ficha_del_Mundo.md"
OPEN_QUESTIONS = "00_Sistema/Preguntas_Abiertas.md"
GLOSSARY = "00_Sistema/04_Convenciones/Glosario.md"
# Registro de enlaces pendientes: lo genera pending_links.py y guarda el tipo de cada uno
PENDING_NOTE = "00_Sistema/Enlaces_Pendientes.md"
# Bitácora: lo que se creó y cambió en cada tarea, para el autor del mundo (la escriben report.py --log
# y log_entry.py, sin que la IA la lea)
CHRONICLE = "00_Sistema/Bitacora.md"
CHRONICLE_MARKER = "<!-- Las entradas nuevas se añaden debajo de esta línea -->"
CHRONICLE_HOME_LINE = "- [[Bitacora|Bitácora]] — cómo ha ido creciendo el mundo: qué se creó y cuándo."
HOME_MOC = "00_Sistema/MOC_Inicio.md"
# Los secretos: la verdad oculta, en su carpeta. Lo que cuentan no va nunca en una nota de lore
SECRET_TYPE = "secreto"
SECRETS_FOLDER = "80_Secretos"
SECRET_WARNING = "verdad oculta: la nota de lore no la cuenta; como mucho, señales o rumores que no la delaten"
# Lo de fuera del mundo: en un mundo que es una sola ciudad o una sola región (la Escala de la Ficha), lo que
# queda fuera (otra ciudad, el reino de al lado) se enlaza como referencia con este tipo en el registro de
# enlaces pendientes, y no se crea. Manda sobre el tipo que le dé una propiedad
OUTSIDE_TYPE = "fuera"
OUTSIDE_NOTE = "Lo de fuera del mundo (que es una sola ciudad o una sola región): se nombra como referencia o rumor y no se crea."
# Escalas de la Ficha en las que el mundo es su foco: todo se crea dentro de él (`local` es la de las Fichas
# anteriores, que no distinguían la ciudad de la región)
LOCAL_SCALES = ("ciudad", "region", "local")
# Estadísticas del mundo: las rehace world_stats.py al terminar cada tarea (con report.py --log y log_entry.py)
STATS_NOTE = "00_Sistema/Estadisticas.md"
STATS_HOME_LINE = ("- [[Estadisticas|Estadísticas]] — cuánto hay en el mundo y qué falta: entidades, enlaces "
                   "pendientes, imágenes y mapas.")
ARCHIVED_FOLDER = "00_Sistema/03_Archivados"
# Ni el registro de pendientes, ni la Bitácora, ni las Estadísticas cuentan como notas que nombran entidades:
# un enlace que solo quedara en ellas no debe seguir pendiente
DEFAULT_EXCLUDED = ("00_Sistema/01_Plantillas", ARCHIVED_FOLDER, PENDING_NOTE, CHRONICLE, STATS_NOTE)


# --- Bóveda ------------------------------------------------------------------

def vault_path(name):
    """La carpeta de la bóveda: la ruta dada si existe; si es relativa y no existe desde aquí, la misma
    carpeta en el directorio superior más cercano que la tenga. Así los scripts encuentran la bóveda
    aunque se ejecuten desde la carpeta de una skill. Si no aparece, la ruta tal cual (el script avisa)."""
    path = Path(name)
    if path.is_dir() or path.is_absolute():
        return path
    for parent in Path.cwd().resolve().parents:
        if (parent / path).is_dir():
            return parent / path
    return path


# --- Módulos -----------------------------------------------------------------

def load_modules():
    """{tipo: contenido de tipos/<tipo>/modulo.json} de todos los módulos."""
    modules = {}
    for path in sorted(SKILL_DIR.glob("tipos/*/modulo.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        modules[data["tipo"]] = data
    return modules


# Parte del rango de enlaces pendientes nuevos (`huecos_propios`) que abre una nota según su relevancia:
# un personaje corriente abre pocos; uno central, todos los del rango
GAPS_BY_RELEVANCE = {1: 0.25, 2: 0.5, 3: 0.75, 4: 1, 5: 1}


def own_gaps_range(module, relevance):
    """(mínimo, máximo) de enlaces pendientes nuevos de una nota del módulo con esa relevancia."""
    low, high = module["huecos_propios"]["min"], module["huecos_propios"]["max"]
    factor = GAPS_BY_RELEVANCE.get(relevance, 1)
    low = math.floor(low * factor)
    return low, max(low, math.ceil(high * factor))


def template_sections(template_body):
    """[(nivel, título)] de las secciones (## y ###) de una plantilla, en orden."""
    sections = []
    for line in template_body:
        match = re.match(r"^(#{2,3}) (.+?)\s*$", line)
        if match:
            sections.append((len(match.group(1)), match.group(2)))
    return sections


def omitted_sections(module, template_body, relevance, props=None):
    """Títulos de las secciones que una nota con esa relevancia no necesita: las que la `profundidad`
    del módulo reserva para una relevancia mayor, con sus subsecciones, y las opcionales (las que
    marca con 0: van solo si hay algo real que contar, a cualquier relevancia). El resto es el núcleo.
    La sección Mapa solo la necesita una nota a la que le toca mapa (por su categoría y su relevancia,
    según la regla `mapa` del módulo); sin las propiedades de la nota, cuenta como no necesaria."""
    depth = module.get("profundidad", {})
    needs_map = bool(map_applies(module, props, relevance)) if props is not None else False
    omitted, parent_omitted = [], False
    for level, title in template_sections(template_body):
        minimum = depth.get(title, 1)
        own = minimum == 0 or minimum > relevance
        if title == MAP_SECTION and module.get("mapa"):
            own = not needs_map
        if level == 2:
            parent_omitted = own
        if own or (level == 3 and parent_omitted):
            omitted.append(title)
    return omitted


# --- Mapas ---------------------------------------------------------------------
# El mapa de un lugar es la leyenda numerada de su sección Mapa; la imagen es una edición de esa
# leyenda. Los números son estables: solo se añaden al final, nunca se renumeran ni se reutilizan.

MAP_SECTION = "Mapa"
# Marcadores que un generador de imágenes dibuja bien en un mismo mapa
MAX_MARKERS = 12
MAP_CLASSES = ("interior", "urbano", "paraje", "territorio")
ORIENTATIONS = ("noroeste", "norte", "noreste", "oeste", "centro", "este", "suroeste", "sur", "sureste")
ORIENTATION_SYNONYMS = {"sudoeste": "suroeste", "sudeste": "sureste"}
UNCHARTED_MARK = "*Sin cartografiar.*"
# Edición nueva con tantas zonas sin cartografiar, o con un cuarto de las cartografiadas
NEW_EDITION_ZONES = 3
# Cada zona, una viñeta con su número en negrita: `- **9.** **Nombre** · orientación — descripción.` No es
# una lista numerada porque Obsidian la renumeraría al leerla (1, 2, 3, 9 se vería 1, 2, 3, 4). Se acepta
# también la forma anterior, `9. **Nombre** · …`
MAP_ITEM_RE = re.compile(r"^(?:-\s+\*\*(?P<numero>\d+)\.\*\*|(?P<numero_lista>\d+)\.)\s+\*\*(?P<nombre>.+?)\*\*"
                         r"\s+·\s+(?P<posicion>.+?)\s+[—–-]\s+(?P<resto>.*)$")
MAP_ITEM_START_RE = re.compile(r"^(?:-\s+\*\*\d+\.\*\*|\d+\.)")
MAP_ITEM_EMPTY_RE = re.compile(r"^(?:-\s+\*\*\d+\.\*\*|\d+\.)\s*$")
MAP_POSITION_RE = re.compile(r"^(?:nivel\s+(\d+)\s*,\s*)?([a-z]+)$")
CONNECTS_RE = re.compile(r"Conecta con ([\d ,y]+?)\.", re.IGNORECASE)
# Lo que la nota conoce de lo escondido: un paso oculto (una puerta disimulada, un pasadizo) hacia otras
# zonas, en los dos sentidos como las conexiones, y una trampa. Lo que nadie conoce es un secreto: no va aquí
HIDDEN_RE = re.compile(r"Pasos? ocultos? a ([\d ,y]+?)\.", re.IGNORECASE)
TRAP_RE = re.compile(r"Trampa:\s*(.+?)\.(?=\s|$)")


def map_rule(module, props):
    """La regla de `mapa` del módulo que corresponde a una nota por su categoría, o None."""
    category = first((props or {}).get("categoria"))
    for rule in module.get("mapa", []):
        if "categoria" not in rule or category in rule["categoria"]:
            return rule
    return None


def map_applies(module, props, relevance):
    """La regla de mapa si a la nota le toca leyenda por su categoría y su relevancia, o None."""
    rule = map_rule(module, props)
    return rule if rule and relevance is not None and relevance >= rule["desde"] else None


def map_section(body):
    """Líneas de la sección `## Mapa` (sin el título), o None si la nota no la tiene."""
    lines, inside = None, False
    for line in body:
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip() == MAP_SECTION
            if inside:
                lines = []
            continue
        if inside:
            lines.append(line)
    return lines


def join_numbers(numbers):
    """«2», «2 y 5», «1, 3 y 5»."""
    numbers = [str(n) for n in sorted(set(numbers))]
    return numbers[0] if len(numbers) == 1 else ", ".join(numbers[:-1]) + " y " + numbers[-1]


def format_connections(numbers):
    """«Conecta con 2.», «Conecta con 2 y 5.», «Conecta con 1, 3 y 5.»"""
    return f"Conecta con {join_numbers(numbers)}." if numbers else ""


def format_hidden(numbers):
    """«Paso oculto a 7.», «Pasos ocultos a 7 y 9.»"""
    if not numbers:
        return ""
    return f"{'Paso oculto' if len(set(numbers)) == 1 else 'Pasos ocultos'} a {join_numbers(numbers)}."


def parse_map_key(body):
    """(zonas, problemas) de la leyenda de la sección Mapa; zonas es None si la nota no la tiene.
    Cada zona: numero, linea (índice dentro de la sección), nombre (legible), enlace (destino o None),
    nivel, orientacion, conecta (números), sin_cartografiar y descripcion."""
    lines = map_section(body)
    if lines is None:
        return None, []
    zones, problems = [], []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not MAP_ITEM_START_RE.match(stripped) or MAP_ITEM_EMPTY_RE.match(stripped):
            continue
        match = MAP_ITEM_RE.match(stripped)
        if not match:
            problems.append(f"zona de la leyenda con formato no válido: «{stripped}» (debe ser "
                            f"`- **N.** **Nombre** · orientación — descripción.`)")
            continue
        number = match.group("numero") or match.group("numero_lista")
        name, position, rest = match.group("nombre"), match.group("posicion"), match.group("resto")
        place = MAP_POSITION_RE.match(normalize(position))
        orientation = ORIENTATION_SYNONYMS.get(place.group(2), place.group(2)) if place else ""
        if orientation not in ORIENTATIONS:
            problems.append(f"zona {number}: orientación no válida «{position}» (una de: {', '.join(ORIENTATIONS)}; "
                            f"en una mazmorra, con su nivel: «nivel 2, norte»)")
        link = LINK_RE.search(name)
        connects = CONNECTS_RE.search(rest)
        hidden = HIDDEN_RE.search(rest)
        trap = TRAP_RE.search(rest)
        zones.append({"numero": int(number), "linea": i, "nombre": strip_links(name).strip(),
                      "enlace": link.group(1).rstrip("\\").strip() if link else None,
                      "nivel": int(place.group(1)) if place and place.group(1) else 1,
                      "orientacion": orientation,
                      "conecta": [int(n) for n in re.findall(r"\d+", connects.group(1))] if connects else [],
                      "ocultos": [int(n) for n in re.findall(r"\d+", hidden.group(1))] if hidden else [],
                      "trampa": trap.group(1).strip() if trap else None,
                      "sin_cartografiar": "sin cartografiar" in normalize(rest),
                      "descripcion": rest.strip()})
    return zones, problems


def map_key_problems(zones):
    """(errores, avisos) de una leyenda: números del 1 al N sin repetir ni saltar, conexiones con
    zonas que existen (y en los dos sentidos) y como mucho MAX_MARKERS zonas por nivel."""
    errors, warnings = [], []
    numbers = [z["numero"] for z in zones]
    repeated = sorted({n for n in numbers if numbers.count(n) > 1})
    if repeated:
        errors.append(f"leyenda del mapa: números repetidos: {', '.join(map(str, repeated))}")
    if numbers:
        missing = sorted(set(range(1, max(numbers) + 1)) - set(numbers))
        if missing:
            errors.append(f"leyenda del mapa: faltan los números {', '.join(map(str, missing))} (van del 1 al "
                          f"último sin saltos; una zona que desaparece se marca, no se borra)")
    known = set(numbers)
    for zone in zones:
        for key, what in (("conecta", "conecta con"), ("ocultos", "tiene un paso oculto a")):
            for other in zone[key]:
                if other == zone["numero"] or other not in known:
                    errors.append(f"leyenda del mapa: la zona {zone['numero']} {what} {other}, que no existe")
                elif not any(z["numero"] == other and zone["numero"] in z[key] for z in zones):
                    warnings.append(f"leyenda del mapa: la zona {zone['numero']} {what} {other}, pero {other} no lo "
                                    f"anota hacia {zone['numero']} (los pasos, también los ocultos, van en los dos "
                                    f"sentidos)")
    for level, count in sorted(zones_per_level(zones).items()):
        if count > MAX_MARKERS:
            where = f"el nivel {level}" if len(zones_per_level(zones)) > 1 else "la leyenda"
            warnings.append(f"{where} tiene {count} zonas y un mapa admite {MAX_MARKERS}: divídela en niveles, o "
                            f"agrupa lugares en una zona con mapa propio (un barrio, una subregión)")
    return errors, warnings


def zones_per_level(zones):
    """{nivel: cuántas zonas tiene}."""
    counts = {}
    for zone in zones:
        counts[zone["nivel"]] = counts.get(zone["nivel"], 0) + 1
    return counts


def map_status(module, props, zones, relevance, routes=None):
    """Estado del mapa de una nota: si le toca leyenda, su clase, la edición, cuántas zonas hay y cuántas
    faltan por cartografiar, y si toca dibujar (`toca`: "primera", "nueva" o None, con su razón y
    los niveles que hay que dibujar). Las rutas nuevas o cambiadas del bloque «Rutas» (`routes`, de
    parse_map_routes) cuentan para la edición nueva como una zona sin cartografiar cada una."""
    rule = map_applies(module, props, relevance)
    zones = zones or []
    edition = int_value(first(props.get("mapa_edicion"))) or 0
    charted = int_value(first(props.get("mapa_zonas"))) or 0
    uncharted = [z for z in zones if z["numero"] > charted] if edition else list(zones)
    new_routes = [r for r in routes or [] if r["sin_cartografiar"]] if edition else []
    pending = len(uncharted) + len(new_routes) if edition else 0
    status = {"aplica": bool(rule), "clase": rule["clase"] if rule else None,
              "desde": rule["desde"] if rule else None, "edicion": edition, "zonas": len(zones),
              "cartografiadas": len(zones) - len(uncharted) if edition else 0,
              "sin_cartografiar": len(uncharted) if edition else 0, "rutas": len(routes or []),
              "rutas_sin_cartografiar": len(new_routes), "toca": None, "niveles": [], "razon": ""}
    if not rule:
        return status
    per_level = zones_per_level(zones)
    minimum = rule.get("zonas_minimas", 1)
    if any(count > MAX_MARKERS for count in per_level.values()):
        status["razon"] = f"un nivel pasa de {MAX_MARKERS} zonas: hay que dividir la leyenda antes de dibujarla"
    elif not edition:
        if len(zones) >= minimum:
            status.update(toca="primera", niveles=sorted(per_level), razon="aún no tiene mapa")
        else:
            status["razon"] = f"tiene {len(zones)} zona(s); el mapa se dibuja desde {minimum}"
    else:
        what = ", ".join(part for part in (f"{len(uncharted)} zona(s)" if uncharted else "",
                                           f"{len(new_routes)} ruta(s)" if new_routes else "") if part)
        if pending and (pending >= NEW_EDITION_ZONES or 4 * pending >= max(charted, 1)):
            # Los niveles que se redibujan: los de las zonas nuevas y los que cruzan las rutas nuevas
            levels = {z["nivel"] for z in uncharted}
            by_number = {z["numero"]: z["nivel"] for z in zones}
            levels |= {by_number[n] for r in new_routes for n in r["recorrido"] if n in by_number}
            status.update(toca="nueva", niveles=sorted(levels), razon=f"{what} sin cartografiar")
        elif pending:
            status["razon"] = (f"{what} sin cartografiar; la edición nueva toca con {NEW_EDITION_ZONES} "
                               f"o con un cuarto de las zonas cartografiadas")
    return status


# --- Las rutas en los mapas ----------------------------------------------------
# El mapa de un lugar dibuja también las rutas que lo cruzan. Van en un bloque al final de la sección Mapa,
# derivado de las notas de las rutas (lo escribe `map_key.py --sync-routes`): cada ruta, con su categoría
# (y su situación, si no está en uso) y las zonas por las que pasa, en orden. «sigue» marca que continúa
# fuera del mapa, y «se pierde», que acaba en nada dentro de él:
#   **Rutas:**
#   - **[[Camino_Real|Camino Real]]** (camino): sigue → 1 → 3 → 5.
#   - **[[Senda_Vieja|Senda Vieja]]** (sendero, abandonada): 3 → 4 → se pierde.

MAP_ROUTES_HEADING = "**Rutas:**"
ROUTE_CONTINUES = "sigue"
ROUTE_FADES = "se pierde"
MAP_ROUTE_RE = re.compile(r"^-\s+\*\*(?P<nombre>.+?)\*\*\s+\((?P<estilo>[^)]+)\):\s+(?P<recorrido>.+?)\.(?:\s+(?P<resto>.*))?$")
# Las rutas que se dibujan sobre el terreno: los portales y las rutas por el aire o el espacio, no
GROUND_ROUTE_CATEGORIES = ("camino", "sendero", "paso", "fluvial", "maritima", "subterranea", "otro")
# Las que no se sabe por dónde van no se dibujan
UNMAPPED_ROUTE_SITUATIONS = ("perdida",)
CONTAINMENT_PROPS = ("ubicacion", "ciudad", "region", "region_padre")


def parse_map_routes(body):
    """(rutas, problemas) del bloque «Rutas» de la sección Mapa. Cada ruta: linea (índice dentro de la
    sección), nombre, enlace, estilo, recorrido (números de zona, «sigue» y «se pierde») y sin_cartografiar."""
    lines = map_section(body)
    routes, problems, inside = [], [], False
    for i, line in enumerate(lines or []):
        stripped = line.strip()
        if stripped == MAP_ROUTES_HEADING:
            inside = True
            continue
        if not inside or not stripped:
            continue
        if not stripped.startswith("- "):
            break
        match = MAP_ROUTE_RE.match(stripped)
        if not match:
            problems.append(f"ruta del mapa con formato no válido: «{stripped}» (debe ser "
                            f"`- **[[Ruta|Nombre]]** (categoría): 1 → 3 → {ROUTE_CONTINUES}.`)")
            continue
        steps = []
        for token in (t.strip() for t in match.group("recorrido").split("→")):
            if token.isdigit():
                steps.append(int(token))
            elif normalize(token) in (ROUTE_CONTINUES, ROUTE_FADES):
                steps.append(normalize(token))
            else:
                problems.append(f"ruta del mapa «{strip_links(match.group('nombre'))}»: «{token}» no es una zona "
                                f"(un número), «{ROUTE_CONTINUES}» ni «{ROUTE_FADES}»")
        link = LINK_RE.search(match.group("nombre"))
        routes.append({"linea": i, "nombre": strip_links(match.group("nombre")).strip(),
                       "enlace": link.group(1).rstrip("\\").strip() if link else None,
                       "estilo": match.group("estilo").strip(), "recorrido": steps,
                       "sin_cartografiar": "sin cartografiar" in normalize(match.group("resto") or "")})
    return routes, problems


def format_map_route(name, style, steps, uncharted=False):
    """`- **[[Ruta|Nombre]]** (estilo): 1 → 3 → sigue.`, con la marca de sin cartografiar si hace falta."""
    path = " → ".join(str(step) for step in steps)
    return f"- **{name}** ({style}): {path}." + (f" {UNCHARTED_MARK}" if uncharted else "")


def map_routes_problems(routes, zones):
    """(errores, avisos) del bloque «Rutas»: sus zonas existen y la leyenda las conecta como la ruta."""
    errors, warnings = [], []
    known = {z["numero"]: z for z in zones or []}
    for route in routes:
        numbers = [n for n in route["recorrido"] if isinstance(n, int)]
        missing = [n for n in numbers if n not in known]
        if missing:
            errors.append(f"la ruta «{route['nombre']}» del mapa pasa por zonas que no existen: "
                          f"{', '.join(map(str, missing))}")
            continue
        for a, b in zip(numbers, numbers[1:]):
            if a != b and b not in known[a]["conecta"]:
                warnings.append(f"la ruta «{route['nombre']}» del mapa va de {a} a {b}, pero la leyenda no los "
                                f"conecta (`map_key.py <Nota> --sync-routes` lo arregla)")
    return errors, warnings


def route_points(vault, entry):
    """Los puntos de una ruta en orden, (texto, enlace o None): los de su Recorrido encadenado o, sin él, su
    partida, sus paradas y su destino."""
    _, body = split_note((vault / entry["path"]).read_text(encoding="utf-8"))
    points = []
    for segment in route_segments(body) or []:
        for label, link in ((segment["desde"], segment["desde_enlace"]), (segment["hasta"], segment["hasta_enlace"])):
            if label and (not points or (points[-1][1] or points[-1][0]).lower() != (link or label).lower()):
                points.append((label, link))
    if points:
        return points
    props = entry["props"]
    links = [link_value(first(props.get("partida")) or "")] + [link_value(v) for v in props.get("paradas", [])] \
        + [link_value(first(props.get("destino")) or "")]
    return [(link.replace("_", " "), link) for link in links if link]


def compute_map_routes(vault, index, note_name, zones):
    """Las rutas que cruzan las zonas de una leyenda: [{enlace, nombre, estilo, recorrido}], con el recorrido
    por sus zonas en orden. Un punto que no es una zona cuenta por la zona que lo contiene (la posada, por su
    ciudad); «sigue» si la ruta viene de fuera del mapa o sale de él, y «se pierde» si acaba en nada dentro de
    él. Solo las rutas con trazado sobre el terreno que se sabe por dónde van (ni portales, ni rutas por el
    aire o el espacio, ni perdidas o dudosas); la propia nota, si es una ruta, no."""
    by_name = {e["name"].lower(): e for e in index}
    note_key = note_name.lower()
    zone_by_link = {z["enlace"].lower(): z["numero"] for z in zones or [] if z["enlace"]}

    def locate(link):
        """(zona o None, si está dentro del mapa: True, False o None si no se sabe: un punto sin nota o un
        enlace pendiente)."""
        if not link:
            return None, None
        if link.lower() not in zone_by_link and link.lower() not in by_name:
            return None, None
        stack, seen = [link.lower()], set()
        while stack:
            key = stack.pop()
            if key in seen:
                continue
            seen.add(key)
            if key in zone_by_link:
                return zone_by_link[key], True
            if key == note_key:
                return None, True
            entry = by_name.get(key)
            for prop in CONTAINMENT_PROPS:
                stack += [t.lower() for t in (entry["relaciones"].get(prop, []) if entry else [])]
        return None, False

    found = []
    for entry in index:
        props = entry["props"]
        if entry["tipo"] != ROUTE_TYPE or entry["name"].lower() == note_key or entry["estado"] == "archivado" \
                or first(props.get("categoria")) not in GROUND_ROUTE_CATEGORIES \
                or first(props.get("situacion")) in UNMAPPED_ROUTE_SITUATIONS \
                or first(props.get("certeza")) == "dudosa" or first(props.get("trazado")) == "red":
            continue
        points = route_points(vault, entry)
        located = [locate(link) for _, link in points]
        steps = []
        for zone, _ in located:
            if zone is not None and (not steps or steps[-1] != zone):
                steps.append(zone)
        if not steps:
            continue
        first_zone, first_inside = located[0]
        last_zone, last_inside = located[-1]
        if first_zone is None and first_inside is False:
            steps.insert(0, ROUTE_CONTINUES)
        if last_zone is None:
            if last_inside is False:
                steps.append(ROUTE_CONTINUES)
            elif first(props.get("trazado")) == "sin_salida":
                steps.append(ROUTE_FADES)
        situation = first(props.get("situacion"))
        style = first(props.get("categoria")) + (f", {situation}" if situation and situation != "en_uso" else "")
        name = f"[[{entry['name']}|{entry['titulo']}]]" if "_" in entry["name"] else f"[[{entry['name']}]]"
        found.append({"enlace": entry["name"], "nombre": name, "estilo": style, "recorrido": steps})
    return sorted(found, key=lambda r: r["enlace"].lower())


def date_keys(module):
    """(propiedad de inicio, propiedad de fin) de un tipo: las dos primeras de sus `fechas`
    (`nacimiento` y `muerte`, `inicio` y `fin`, `fundacion` y `abandono`…), con None si faltan."""
    keys = list(module.get("fechas", [])) + [None, None]
    return keys[0], keys[1]


def place_types(modules=None):
    """Tipos de la familia `lugar` que pueden contener a otros (región, asentamiento, lugar): no los que el
    módulo marca con `contenedor: false`, como la ruta o el ecosistema, que no son el foco ni la región de
    nadie."""
    modules = modules if modules is not None else load_modules()
    return {tipo for tipo, module in modules.items()
            if module.get("familia") == "lugar" and module.get("contenedor", True)}


def candidate_modules(expected, modules, properties=None):
    """Módulos que pueden completar un hueco: el propio tipo, o los de su familia (p. ej. lugar).
    Un módulo de familia con la lista `completa` solo cuenta si **todas** las propiedades donde
    aparece el hueco están en esa lista: una región completa la `region` de un personaje, pero
    no un hueco que además es la `residencia` de alguien (eso es un asentamiento o un lugar)."""
    if not expected:
        return []
    # La familia manda aunque un módulo se llame como ella (el módulo `lugar` es de la familia `lugar`,
    # con la región y el asentamiento): si se mirara solo el nombre, quedarían fuera los demás
    family = [tipo for tipo, module in modules.items() if module.get("familia") == expected]
    if not family:
        return [expected] if expected in modules else []
    properties = set(properties or [])
    return sorted(tipo for tipo in family
                  if not modules[tipo].get("completa")
                  or (properties and properties <= set(modules[tipo]["completa"])))


# --- Enlaces -----------------------------------------------------------------

def is_hidden(relative):
    return bool(HIDDEN_DIRS & set(Path(relative).parts))


def index_vault(vault):
    """Nombres y rutas que resuelven un enlace, en minúsculas (Obsidian no distingue mayúsculas)."""
    names, paths = set(), set()
    for path in vault.rglob("*"):
        relative = path.relative_to(vault)
        if not path.is_file() or is_hidden(relative):
            continue
        posix = relative.as_posix().lower()
        names.add(path.name.lower())
        paths.add(posix)
        if path.suffix.lower() == ".md":
            names.add(path.stem.lower())
            paths.add(posix[:-3])
    return names, paths


def resolve_note(argument, vault):
    """Ruta de la nota a partir de una ruta o de su nombre; None si no existe o hay varias con ese nombre."""
    candidate = Path(argument)
    for path in (candidate, vault / candidate, vault / f"{argument}.md"):
        if path.is_file():
            return path
    stem = Path(argument).stem.lower()
    matches = [p for p in vault.rglob("*.md")
               if p.stem.lower() == stem and not HIDDEN_DIRS & set(p.relative_to(vault).parts)]
    return matches[0] if len(matches) == 1 else None


def link_exists(target, names, paths):
    target = target.strip().lower()
    if "/" in target:
        return any(p == target or p.endswith("/" + target) for p in paths)
    return target in names


def link_targets(line):
    """Destinos de los enlaces de una línea. En las tablas el alias se escribe `[[Nota\\|texto]]`:
    se quita la barra invertida que queda pegada al destino."""
    return [target.rstrip("\\").strip() for target in LINK_RE.findall(line)]


def malformed_lines(text):
    """Líneas del frontmatter con corchetes de enlace desparejados (p. ej. '"[[A]], del]]"')."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---" or "---" not in [l.strip() for l in lines[1:]]:
        return []
    end = [l.strip() for l in lines[1:]].index("---") + 1
    return [l.strip() for l in lines[1:end] if l.count("[[") != l.count("]]")]


def parse_note(text):
    """Devuelve (tipo de la nota, [(destino, propiedad o None, sección)])."""
    note_type, links = None, []
    lines = text.splitlines()
    in_frontmatter = bool(lines) and lines[0].strip() == "---"
    key, section, in_code, in_comment = None, "(inicio)", False, False
    for number, line in enumerate(lines):
        if in_frontmatter:
            if number == 0:
                continue
            if line.strip() == "---":
                in_frontmatter = False
                continue
            match = KEY_RE.match(line)
            if match:
                key = match.group(1)
                if key == "tipo":
                    note_type = line.split(":", 1)[1].strip().strip("\"'") or None
            links += [(target, key, None) for target in link_targets(line)]
            continue
        # Se ignoran los enlaces dentro de bloques de código, código en línea y comentarios
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if in_comment:
            if "-->" not in line:
                continue
            line, in_comment = line.split("-->", 1)[1], False
        line = COMMENT_RE.sub("", line)
        if "<!--" in line:
            line, in_comment = line.split("<!--", 1)[0], True
        if re.match(r"^#{1,6}\s", line):
            section = line.lstrip("#").strip()
        links += [(target, None, section) for target in link_targets(INLINE_CODE_RE.sub("", line))]
    return note_type, links


def is_confirmation(line):
    """Pregunta abierta sin resolver que pide confirmar un hecho: `- [ ] Confirmar: …`.
    Una pregunta que solo menciona la palabra ("a confirmar con el calendario") no lo es."""
    return bool(CONFIRM_RE.match(line.strip()))


def blocked_links(vault):
    """Enlaces que esperan la decisión del usuario: el sujeto de cada confirmación pendiente de
    Preguntas Abiertas, que es su primer enlace (`- [ ] Confirmar: existe [[Sujeto]] …`). Si es un
    enlace pendiente, no se crea todavía; los demás enlaces de la línea son contexto."""
    path = vault / OPEN_QUESTIONS
    blocked = set()
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            subject = re.search(r"\[\[([^\]|#^\\]+)", line) if is_confirmation(line) else None
            if subject:
                blocked.add(subject.group(1).strip().lower())
    return blocked


def is_secret_note(relative):
    """Si una nota (su ruta relativa a la bóveda) es un secreto: los secretos viven en su carpeta."""
    return relative.replace("\\", "/").lower().startswith(SECRETS_FOLDER.lower() + "/")


def strip_links(text):
    """Texto legible: `[[Nota|texto]]` → texto y `[[Nota_Larga]]` → Nota Larga."""
    def readable(match):
        target, alias = match.group(1), match.group(2)
        return alias if alias else target.replace("_", " ")
    return LINK_WITH_ALIAS_RE.sub(readable, text)


# --- Enlaces pendientes (huecos) ---------------------------------------------

def read_registry(vault):
    """{enlace en minúsculas: tipo, o None si no lo tiene} de las filas del registro de enlaces
    pendientes; None si el registro no existe."""
    path = vault / PENDING_NOTE
    if not path.is_file():
        return None
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) >= 2 and len(cells[0]) > 2 and cells[0].startswith("`") and cells[0].endswith("`"):
            tipo = cells[1].split(" ")[0].strip().lower()
            rows[cells[0].strip("`").strip().lower()] = tipo if tipo and tipo != "?" else None
    return rows


def load_pending_types(vault):
    """{enlace en minúsculas: tipo} del registro de enlaces pendientes (los que ya tienen tipo)."""
    return {link: tipo for link, tipo in (read_registry(vault) or {}).items() if tipo}


def entity_notes(gap):
    """Notas de entidades que nombran un enlace pendiente (sin las de sistema, como Preguntas
    Abiertas, cuyas menciones no cuentan como de una entidad)."""
    return sorted({o["note"] for o in gap["occurrences"] if not o["note"].startswith("00_Sistema/")})


def known_types(modules):
    """Tipos que puede tener un enlace pendiente: los módulos que existen y los que nombran sus
    relaciones (los previstos, como costumbre u obra), más las familias."""
    types = set(modules)
    for module in modules.values():
        types.add(module.get("familia", ""))
        types.update(v for v in module.get("relaciones", {}).values() if v != "cualquiera")
    return {t for t in types if t} | {OUTSIDE_TYPE}


def find_gaps(vault, excluded=DEFAULT_EXCLUDED, pending_types=None):
    """(enlaces pendientes, enlaces mal formados). Un enlace pendiente (o hueco) es un enlace a
    una nota que todavía no existe. Cada uno: enlace, tipo esperado y de dónde sale (`propiedad`,
    si aparece en una propiedad de relación con tipo; `registro`, si se le asignó en
    Enlaces_Pendientes), apariciones, notas de entidades que lo nombran y módulos que pueden
    crearlo. `pending_types` sustituye a los tipos del registro."""
    modules = load_modules()
    relations = {tipo: module["relaciones"] for tipo, module in modules.items()}
    registry = pending_types if pending_types is not None else load_pending_types(vault)
    names, paths = index_vault(vault)
    gaps, malformed = {}, []
    for path in sorted(vault.rglob("*.md")):
        relative = path.relative_to(vault).as_posix()
        if is_hidden(relative) or relative.startswith(excluded):
            continue
        text = path.read_text(encoding="utf-8")
        malformed += [{"note": relative, "line": line} for line in malformed_lines(text)]
        note_type, links = parse_note(text)
        for target, prop, section in links:
            target = target.strip()
            # Un archivo que falta (una imagen, un PDF) no es una entidad por crear
            if not target or link_exists(target, names, paths) or ATTACHMENT_RE.search(target):
                continue
            gap = gaps.setdefault(target.lower(), {"link": target, "expected_type": None, "occurrences": []})
            expected = relations.get(note_type, {}).get(prop) if prop else None
            if expected and expected != "cualquiera" and not gap["expected_type"]:
                gap["expected_type"] = expected
            occurrence = {"note": relative, "note_type": note_type, "property": prop, "section": section}
            if occurrence not in gap["occurrences"]:
                gap["occurrences"].append(occurrence)
    for gap in gaps.values():
        if registry.get(gap["link"].lower()) == OUTSIDE_TYPE:
            # Lo de fuera del mundo se nombra, pero no se crea: ningún módulo lo completa
            gap["typed_by"], gap["expected_type"], gap["expected_modules"] = "registro", OUTSIDE_TYPE, []
            gap["notes"] = entity_notes(gap)
            continue
        # Solo las propiedades que dan un tipo: una que admite cualquiera (el `afecta_a` de un secreto)
        # no dice qué módulo lo creará, y si contara dejaría el hueco sin ninguno
        properties = {o["property"] for o in gap["occurrences"] if o["property"]
                      and relations.get(o["note_type"], {}).get(o["property"]) not in (None, "cualquiera")}
        if gap["expected_type"]:
            gap["typed_by"] = "propiedad"
            gap["expected_modules"] = candidate_modules(gap["expected_type"], modules, properties)
            # La propiedad da una familia (lugar); el registro puede concretar el módulo (una región)
            chosen = registry.get(gap["link"].lower())
            if len(gap["expected_modules"]) > 1 and chosen in gap["expected_modules"]:
                gap["expected_modules"] = [chosen]
        elif gap["link"].lower() in registry:
            # El registro guarda el módulo concreto que lo creará (asentamiento, lugar, región…)
            gap["typed_by"] = "registro"
            gap["expected_type"] = registry[gap["link"].lower()]
            gap["expected_modules"] = [gap["expected_type"]] if gap["expected_type"] in modules else []
        else:
            gap["typed_by"] = None
            gap["expected_modules"] = []
        gap["notes"] = entity_notes(gap)
    return sorted(gaps.values(), key=lambda g: g["link"].lower()), malformed


def gap_kind(gap):
    """El tipo con que se muestra un enlace pendiente: el módulo que lo creará si solo hay uno (un
    asentamiento, no «lugar»), o su tipo."""
    modules = gap["expected_modules"]
    return modules[0] if len(modules) == 1 else (gap["expected_type"] or "")


def describe_expected(gap):
    """Texto del tipo esperado y de los módulos que pueden completarlo."""
    expected = gap["expected_type"]
    if not expected:
        return "desconocido"
    if expected == OUTSIDE_TYPE:
        return "fuera del mundo (una referencia: no se crea)"
    if not gap["expected_modules"]:
        return f"{expected} (sin módulo todavía)"
    if gap["expected_modules"] == [expected]:
        return expected
    return f"{expected} (módulos disponibles: {', '.join(gap['expected_modules'])})"


# --- Frontmatter -------------------------------------------------------------

def split_note(text):
    """(líneas del frontmatter o None, líneas del cuerpo)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i + 1:]
    return None, lines


def scalar_error(raw):
    """Motivo por el que un valor escalar no es YAML válido, o None."""
    if raw.startswith('"'):
        return None if len(raw) > 1 and raw.endswith('"') else "comillas sin cerrar"
    if raw.startswith("'"):
        return None if len(raw) > 1 and raw.endswith("'") else "comillas sin cerrar"
    if raw.startswith(PLAIN_FORBIDDEN_START):
        return f"empieza con '{raw[0]}' sin comillas"
    if ": " in raw or " #" in raw:
        return "contiene ': ' o ' #' sin comillas"
    return None


def parse_frontmatter(lines, errors):
    """{propiedad: [valores crudos]} para el subconjunto de YAML que usan las plantillas."""
    props, current = {}, None
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key_match = KEY_LINE_RE.match(line)
        if key_match:
            key, rest = key_match.group(1), key_match.group(2).strip()
            if key in props:
                errors.append(f"propiedad duplicada: `{key}`")
            current = None
            if rest in ("", "[]"):
                props[key] = []
                current = key if rest == "" else None
            elif rest.startswith("[") and rest.endswith("]"):
                props[key] = [v.strip() for v in re.findall(r'"[^"]*"|[^,\[\]]+', rest[1:-1]) if v.strip()]
            else:
                props[key] = [rest]
                problem = scalar_error(rest)
                if problem:
                    errors.append(f"`{key}`: valor no válido ({problem}): {rest}")
            continue
        item_match = ITEM_LINE_RE.match(line)
        if item_match and current:
            value = item_match.group(1).strip()
            props[current].append(value)
            problem = scalar_error(value)
            if problem:
                errors.append(f"`{current}`: elemento no válido ({problem}): {value}")
            continue
        errors.append(f"línea de frontmatter no válida: {line.strip()}")
    return props


def is_empty_value(values):
    return not values or values == ['""'] or values == ["''"]


def unquote(value):
    value = (value or "").strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def first(values):
    """Primer valor sin comillas de una propiedad, o cadena vacía."""
    return unquote(values[0]) if values else ""


def link_value(value):
    """Destino de un valor de propiedad con forma "[[Nota]]", o None."""
    match = LINK_RE.search(unquote(value))
    return match.group(1).rstrip("\\").strip() if match else None


def int_value(value):
    """Entero de un valor de propiedad ('312', '-40', '"7"'), o None."""
    value = unquote(str(value)) if value is not None else ""
    return int(value) if INT_RE.match(value) else None


# --- Bitácora ----------------------------------------------------------------

CHRONICLE_HEADER = f"""---
tipo: meta
---

# Bitácora

Cómo ha ido creciendo el mundo: qué se creó y qué cambió en cada tarea, de lo más reciente a lo más antiguo. La escriben las skills al terminar (`report.py --log`, `log_entry.py`); lo que se cambia a mano en Obsidian no queda aquí.
- Las notas creadas van enlazadas; los enlaces pendientes, como texto.
- El detalle técnico de cada ciclo del motor está en el Registro de Generación.

{CHRONICLE_MARKER}
"""


def add_chronicle_entry(vault, title, lines, date=None):
    """Añade una entrada arriba de la Bitácora, debajo de su marca: `## <fecha> · <título>` y sus líneas.
    Si la Bitácora no existe, la crea y la enlaza desde MOC_Inicio. Devuelve los avisos."""
    warnings = []
    path = vault / CHRONICLE
    text = path.read_text(encoding="utf-8") if path.is_file() else CHRONICLE_HEADER
    created = not path.is_file()
    entry = [f"## {date or datetime.date.today().isoformat()} · {title}", *lines, ""]
    rows = text.splitlines()
    at = next((i + 1 for i, line in enumerate(rows) if line.strip() == CHRONICLE_MARKER), None)
    if at is None:
        # Sin la marca (se borró a mano): tras el título y su presentación, antes de la primera entrada
        at = next((i for i, line in enumerate(rows) if line.startswith("## ")), len(rows))
        warnings.append(f"la Bitácora no tiene la marca de las entradas nuevas; añádela: {CHRONICLE_MARKER}")
    while at < len(rows) and not rows[at].strip():
        at += 1
    rows[at:at] = entry
    # Una línea en blanco entre la marca y la entrada más reciente
    marker = next((i for i, line in enumerate(rows) if line.strip() == CHRONICLE_MARKER), None)
    if marker is not None and marker + 1 < len(rows) and rows[marker + 1].strip():
        rows.insert(marker + 1, "")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(rows).rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    if created:
        home = vault / HOME_MOC
        if home.is_file():
            home_rows = home.read_text(encoding="utf-8").splitlines()
            if not any("[[Bitacora" in line for line in home_rows):
                anchor = next((i for i, line in enumerate(home_rows) if "[[Preguntas_Abiertas" in line), None)
                if anchor is None:
                    warnings.append(f"no encuentro dónde enlazar la Bitácora en MOC_Inicio; añádelo a mano: "
                                    f"{CHRONICLE_HOME_LINE}")
                else:
                    home_rows.insert(anchor + 1, CHRONICLE_HOME_LINE)
                    home.write_text("\n".join(home_rows) + "\n", encoding="utf-8", newline="\n")
    return warnings


def readable_links(text):
    """`[[Nota_Larga]]` → `[[Nota_Larga|Nota Larga]]`, para que Obsidian no muestre los guiones bajos."""
    def replace(match):
        target, alias = match.group(1), match.group(2)
        # Los embeds y los adjuntos se quedan como están: en un embed, el texto sería el tamaño
        if alias or "_" not in target or match.group(0).startswith("!") or ATTACHMENT_RE.search(target):
            return match.group(0)
        return f"[[{target.rstrip(chr(92))}|{target.rstrip(chr(92)).replace('_', ' ')}]]"
    return LINK_WITH_ALIAS_RE.sub(replace, text)


# --- Mundo -------------------------------------------------------------------

def normalize(text):
    """Forma comparable de un nombre: sin tildes, apóstrofes ni guiones bajos, en minúsculas."""
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"['’`´]", "", text).replace("_", " ").lower()
    return re.sub(r"\s+", " ", text).strip()


def display_title(heading):
    """Título de un H1 sin '# ' ni el emoji del tipo."""
    title = heading.lstrip("#").strip()
    parts = title.split(" ", 1)
    if len(parts) == 2 and not any(c.isalnum() for c in parts[0].replace(VARIATION_SELECTOR, "")):
        title = parts[1]
    return title.strip()


def read_world(vault):
    """Datos de la Ficha del Mundo: propiedades, año actual (entero o None), foco y calendario."""
    path = vault / WORLD_SHEET
    if not path.is_file():
        return {"props": {}, "ano_actual": None, "foco": "", "calendario": "", "escala": ""}
    frontmatter, body = split_note(path.read_text(encoding="utf-8"))
    props = {k: first(v) for k, v in parse_frontmatter(frontmatter or [], []).items()}

    def body_field(*labels):
        for line in body:
            for label in labels:
                prefix = f"- **{label}:**"
                if line.startswith(prefix):
                    return line[len(prefix):].strip()
        return ""

    return {"props": props, "ano_actual": int_value(props.get("ano_actual")),
            "foco": body_field("Foco inicial"), "calendario": body_field("Calendario", "Presente y calendario"),
            "escala": str(props.get("escala") or "").strip().strip('"').lower()}


def is_system_note(relative, note_type):
    """Si una nota es interna (no una entidad): por su tipo, o por el tipo `sistema` que llevaban las
    notas de 00_Sistema en las bóvedas anteriores al módulo `sistema`."""
    return note_type in SYSTEM_TYPES or (note_type == LEGACY_SYSTEM_TYPE and relative.startswith("00_Sistema/"))


def load_index(vault, excluded=DEFAULT_EXCLUDED):
    """Una entrada por entidad (no notas de sistema): nombre, ruta, tipo, título, resumen,
    relevancia, estado, origen, alias, propiedades (sin comillas), relaciones y enlaces."""
    entries = []
    for path in sorted(vault.rglob("*.md")):
        relative = path.relative_to(vault).as_posix()
        if is_hidden(relative) or relative.startswith(excluded):
            continue
        text = path.read_text(encoding="utf-8")
        frontmatter, body = split_note(text)
        if frontmatter is None:
            continue
        raw = parse_frontmatter(frontmatter, [])
        note_type = first(raw.get("tipo"))
        if not note_type or is_system_note(relative, note_type):
            continue
        headings = [line for line in body if line.startswith("# ")]
        title = display_title(headings[0]) if headings else path.stem.replace("_", " ")
        summary = ""
        if headings:
            after = body[body.index(headings[0]) + 1:]
            quote = next((l for l in after if l.strip().startswith("> ") and len(l.strip()) > 2), "")
            summary = strip_links(quote.strip()[2:].strip())
        _, links = parse_note(text)
        relations = {}
        for key, values in raw.items():
            targets = [t for t in (link_value(v) for v in values) if t]
            if targets:
                relations[key] = targets
        entries.append({
            "name": path.stem, "path": relative, "tipo": note_type, "titulo": title, "resumen": summary,
            "relevancia": int_value(first(raw.get("relevancia"))),
            "estado": first(raw.get("estado")), "origen": first(raw.get("origen")) or "manual",
            "aliases": [unquote(v) for v in raw.get("aliases", [])],
            "props": {k: [unquote(v) for v in vals] for k, vals in raw.items()},
            "relaciones": relations,
            "enlaces": sorted({t.strip() for t, _, _ in links if t.strip()}),
        })
    return entries


def without_secrets(index):
    """Las entidades del mundo, sin los secretos: los secretos se cuentan aparte y no entran ni en
    el total de entidades ni en la densidad de enlaces pendientes por entidad."""
    return [e for e in index if e["tipo"] != SECRET_TYPE]


# --- Calendarios -------------------------------------------------------------
# Un calendario es una nota de tipo calendario. Sus tablas «Meses», «Semana», «Estaciones» y
# «Festividades» las leen los scripts. El de referencia (`referencia: true`) es el eje de la
# Ficha; los demás dicen en `ano_cero` en qué año del eje empieza su cuenta.

EXACT_DATE_RE = re.compile(r"^(\d{1,3})\s+de\s+(.+)\s+de\s+(-?\d+)(?:\s+(\S.*))?$", re.IGNORECASE)
DAY_MONTH_RE = re.compile(r"^(\d{1,3})\s+de\s+(.+)$", re.IGNORECASE)
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
SEPARATOR_CELL_RE = re.compile(r"^:?-{3,}:?$")


def section_table(body, heading):
    """(cabecera normalizada, filas) de la primera tabla bajo `## <heading>`; ([], []) si no hay.
    Las celdas vienen sin espacios de más y con los enlaces como texto legible."""
    header, rows, inside = [], [], False
    for line in body:
        if line.startswith("## "):
            if inside:
                break
            inside = normalize(line[3:]) == normalize(heading)
            continue
        stripped = line.strip()
        if not inside:
            continue
        if not stripped.startswith("|"):
            if header:
                break  # la tabla terminó
            continue
        cells = [strip_links(cell.strip()) for cell in CELL_SPLIT_RE.split(stripped.strip("|"))]
        if not header:
            header = [normalize(cell) for cell in cells]
        elif not all(SEPARATOR_CELL_RE.match(cell) for cell in cells if cell):
            rows.append(cells)
    return header, rows


def table_cell(header, row, *names):
    """Celda de la fila en la primera columna cuyo encabezado coincide con alguno de los nombres."""
    for name in names:
        key = normalize(name)
        if key in header:
            i = header.index(key)
            return row[i] if i < len(row) else ""
    return ""


def parse_calendar(text, name=""):
    """Datos de una nota de calendario (año 0, sufijos, meses, semana, estaciones y festividades),
    con los errores de su estructura en `errores`."""
    frontmatter, body = split_note(text)
    props = parse_frontmatter(frontmatter or [], [])
    headings = [line for line in body if line.startswith("# ")]
    errors = []
    year_zero = int_value(first(props.get("ano_cero")))
    if year_zero is None:
        errors.append("`ano_cero` debe ser un número: el año del eje de la Ficha en que empieza su cuenta "
                      "(0 en el calendario de referencia)")
    calendar = {
        "nombre": name,
        "titulo": display_title(headings[0]) if headings else name.replace("_", " "),
        "referencia": first(props.get("referencia")).lower() == "true",
        "ano_cero": year_zero or 0,
        "sufijo": first(props.get("sufijo")),
        "sufijo_negativo": first(props.get("sufijo_negativo")),
        "meses": [], "semana": [], "estaciones": [], "festividades": [], "errores": errors,
    }
    if calendar["referencia"] and year_zero not in (None, 0):
        errors.append(f"el calendario de referencia es el eje de la Ficha: su `ano_cero` debe ser 0 "
                      f"(encontrado: {year_zero})")

    header, rows = section_table(body, "Meses")
    for row in rows:
        month = table_cell(header, row, "Nombre", "Mes")
        if not month:
            errors.append("tabla «Meses»: hay una fila sin nombre de mes")
            continue
        days = int_value(table_cell(header, row, "Días"))
        if days is None or days < 1:
            shown = table_cell(header, row, "Días") or "vacío"
            errors.append(f"tabla «Meses»: «{month}» necesita su número de días (encontrado: {shown})")
        if any(normalize(m["nombre"]) == normalize(month) for m in calendar["meses"]):
            errors.append(f"tabla «Meses»: el mes «{month}» está repetido")
        calendar["meses"].append({"nombre": month, "dias": max(days or 0, 0),
                                  "estacion": table_cell(header, row, "Estación")})
    if not calendar["meses"]:
        errors.append("la tabla «Meses» no tiene meses: una fila por mes, en orden, con su nombre y sus días")
    months = {normalize(m["nombre"]): i for i, m in enumerate(calendar["meses"], 1)}

    header, rows = section_table(body, "Semana")
    calendar["semana"] = [day for day in (table_cell(header, row, "Día", "Nombre") for row in rows) if day]

    header, rows = section_table(body, "Estaciones")
    for row in rows:
        season = table_cell(header, row, "Estación", "Nombre")
        start, end = table_cell(header, row, "Desde"), table_cell(header, row, "Hasta")
        for label, value in (("Desde", start), ("Hasta", end)):
            if value and normalize(value) not in months:
                errors.append(f"tabla «Estaciones»: «{value}» ({label}, {season}) no es un mes de la tabla «Meses»")
        calendar["estaciones"].append({"nombre": season, "desde": start, "hasta": end})
    seasons = {normalize(s["nombre"]) for s in calendar["estaciones"]}
    for month in calendar["meses"]:
        if seasons and month["estacion"] and normalize(month["estacion"]) not in seasons:
            errors.append(f"tabla «Meses»: la estación de «{month['nombre']}» («{month['estacion']}») "
                          f"no está en la tabla «Estaciones»")

    header, rows = section_table(body, "Festividades")
    for row in rows:
        date, festival = table_cell(header, row, "Fecha"), table_cell(header, row, "Nombre", "Festividad")
        entry = {"nombre": festival, "fecha": date, "mes": None, "dia": None}
        # «15 de <Mes>» se valida; una regla («la primera luna de <Mes>») es una fiesta movible
        match = DAY_MONTH_RE.match(date)
        if match:
            day, month_name = int(match.group(1)), match.group(2).strip()
            index = months.get(normalize(month_name))
            if index is None:
                errors.append(f"tabla «Festividades»: «{date}» ({festival}): «{month_name}» no es un mes "
                              f"de la tabla «Meses»")
            elif not 1 <= day <= calendar["meses"][index - 1]["dias"]:
                month = calendar["meses"][index - 1]
                errors.append(f"tabla «Festividades»: «{date}» ({festival}): {month['nombre']} tiene "
                              f"{month['dias']} días")
            else:
                entry["mes"], entry["dia"] = index, day
        calendar["festividades"].append(entry)
    calendar["dias_por_ano"] = sum(m["dias"] for m in calendar["meses"])
    return calendar


def load_calendars(vault):
    """Los calendarios de la bóveda (notas de tipo calendario), ya analizados."""
    return [parse_calendar((vault / entry["path"]).read_text(encoding="utf-8"), entry["name"])
            for entry in load_index(vault) if entry["tipo"] == "calendario"]


def reference_calendar(calendars):
    """El calendario de referencia (el eje de la Ficha), o None."""
    return next((c for c in calendars if c["referencia"]), None)


def format_year(calendar, axis_year):
    """Un año del eje escrito en un calendario: «412 UE», o «45 AUE» si es anterior a su año 0."""
    year = axis_year - calendar["ano_cero"]
    if year < 0 and calendar["sufijo_negativo"]:
        return f"{-year} {calendar['sufijo_negativo']}"
    return f"{year} {calendar['sufijo']}".strip()


def format_date(calendar, axis_year, month=None, day=None):
    """Una fecha del eje con los nombres del calendario: «15 de Siega de 412 UE», o solo el año."""
    year = format_year(calendar, axis_year)
    if month is None:
        return year
    return f"{day} de {calendar['meses'][month - 1]['nombre']} de {year}"


def sample_date(calendar, axis_year=None):
    """Una fecha de ejemplo escrita en el calendario, para mensajes y resúmenes."""
    axis_year = axis_year if axis_year is not None else calendar["ano_cero"] + 100
    if not calendar["meses"]:
        return f"15 de <mes> de {format_year(calendar, axis_year)}"
    return format_date(calendar, axis_year, 1, min(15, calendar["meses"][0]["dias"]) or 1)


def parse_exact_date(value, calendar):
    """((año del eje, nº de mes, día), None) de una fecha como «15 de Siega de 412 UE» escrita en
    ese calendario, o (None, motivo)."""
    match = EXACT_DATE_RE.match(unquote(value))
    if not match:
        return None, f"escríbela como «<día> de <mes> de <año>», por ejemplo «{sample_date(calendar)}»"
    day, month_name, year = int(match.group(1)), match.group(2).strip(), int(match.group(3))
    suffix = (match.group(4) or "").strip()
    month = {normalize(m["nombre"]): i for i, m in enumerate(calendar["meses"], 1)}.get(normalize(month_name))
    if month is None:
        names = ", ".join(m["nombre"] for m in calendar["meses"]) or "ninguno"
        return None, f"«{month_name}» no es un mes de [[{calendar['nombre']}]] (sus meses: {names})"
    if suffix:
        if calendar["sufijo_negativo"] and normalize(suffix) == normalize(calendar["sufijo_negativo"]):
            year = -year
        elif normalize(suffix) != normalize(calendar["sufijo"]):
            return None, (f"«{suffix}» no es como se escriben los años en [[{calendar['nombre']}]] "
                          f"(por ejemplo «{sample_date(calendar)}»)")
    days = calendar["meses"][month - 1]["dias"]
    if not 1 <= day <= days:
        return None, f"{calendar['meses'][month - 1]['nombre']} tiene {days} días"
    return (year + calendar["ano_cero"], month, day), None


def parse_moment(value, calendar):
    """(año del eje, nº de mes, día) de un texto escrito en el calendario: una fecha exacta
    («3 de Siega de 412 UE») o solo un año («340 UE», «12 AUE», «año 5»), con mes y día en None.
    None si no se entiende (un intervalo, una fecha aproximada…)."""
    text = re.sub(r"^a[nñ]o\s+", "", unquote(value), flags=re.IGNORECASE).strip()
    parsed, _ = parse_exact_date(text, calendar)
    if parsed:
        return parsed
    match = re.match(r"^(-?\d+)(?:\s+(\S.*))?$", text)
    if not match:
        return None
    year, suffix = int(match.group(1)), (match.group(2) or "").strip()
    if suffix:
        if calendar["sufijo_negativo"] and normalize(suffix) == normalize(calendar["sufijo_negativo"]):
            year = -year
        elif normalize(suffix) != normalize(calendar["sufijo"]):
            return None
    return year + calendar["ano_cero"], None, None


def parse_year(value, calendar):
    """Año del eje de un texto escrito en el calendario (ver parse_moment), o None."""
    moment = parse_moment(value, calendar)
    return moment[0] if moment else None


def calendar_summary(calendar, world_year=None):
    """Líneas de resumen de un calendario (años, meses, semana, estaciones y festividades), para
    build_context.py y world_calendar.py."""
    years = (f"año actual {format_year(calendar, world_year)}" if world_year is not None
             else f"se escriben «{format_year(calendar, calendar['ano_cero'] + 100)}»")
    if calendar["sufijo_negativo"]:
        years += f"; antes de su año 0, «{format_year(calendar, calendar['ano_cero'] - 45)}»"
    lines = [f"- Años: {years}. Fechas exactas: «{sample_date(calendar, world_year)}»."]
    months = " · ".join(f"{m['nombre']} ({m['dias']})" for m in calendar["meses"])
    # Los «meses» muy cortos (menos de un tercio de lo habitual) son días fuera de los meses
    lengths = sorted(m["dias"] for m in calendar["meses"])
    typical = lengths[len(lengths) // 2] if lengths else 0
    apart = [m for m in calendar["meses"] if m["dias"] * 3 < typical]
    shape = f"{len(calendar['meses']) - len(apart)} meses"
    if apart:
        names = ", ".join(m["nombre"] for m in apart)
        shape += f" y {sum(m['dias'] for m in apart)} días fuera de los meses ({names})"
    lines.append(f"- Año de {calendar['dias_por_ano']} días en {shape}: {months}")
    if calendar["semana"]:
        lines.append(f"- Semana de {len(calendar['semana'])} días: {', '.join(calendar['semana'])}")
    if calendar["estaciones"]:
        lines.append("- Estaciones: " + " · ".join(
            f"{s['nombre']} ({s['desde']}–{s['hasta']})" if s["desde"] else s["nombre"]
            for s in calendar["estaciones"]))
    if calendar["festividades"]:
        lines.append("- Festividades: " + " · ".join(
            f"{f['nombre']} ({f['fecha']})" for f in calendar["festividades"]))
    return lines


# --- Rutas -------------------------------------------------------------------
# Una ruta (tipo `ruta`) une lugares, o sale de uno y se pierde. Su tabla «Recorrido» (Desde, Hasta, Días,
# Cómo es) da sus tramos en orden, con los días de cada uno por su medio habitual (`medio`). Las rutas
# ciertas que se pueden recorrer hoy forman el grafo de distancias del mundo: los lugares son sus nodos y
# los tramos, sus aristas, en los dos sentidos. Un punto sin nota (un vado, el sitio donde se pierde) es un
# nodo de su propia ruta.

ROUTE_TYPE = "ruta"
ROUTE_SECTION = "Recorrido"
# Situaciones en que una ruta se puede recorrer hoy; una ruta con `certeza: dudosa` no cuenta nunca
ROUTE_USABLE = ("en_uso", "en_declive")
ROUTE_DAYS_RE = re.compile(r"^~?\s*(\d+(?:[.,]\d+)?)(?![\d.,])")
UNKNOWN_DAYS = ("?", "¿?")
# Lo que el motor quiere conectado: asentamientos y lugares, salvo los parajes naturales (se cruzan, no
# se va a ellos) y lo que nadie sabe dónde está
CONNECTABLE_TYPES = ("asentamiento", "lugar")
CROSSED_CATEGORIES = ("montana", "agua", "bosque", "isla", "desierto", "paraje")
UNREACHABLE_SITUATIONS = ("perdido",)
# Un lugar sin rutas propias se alcanza por el sitio que lo contiene (la taberna o el barrio, por su ciudad)
CONTAINER_PROPS = ("ubicacion", "ciudad")


def days_value(text):
    """Días de un tramo («3», «2,5», «~4 en verano») como número; None si no se saben («?»); False si no
    es un número."""
    text = strip_links(text or "").strip()
    if text in UNKNOWN_DAYS:
        return None
    match = ROUTE_DAYS_RE.match(text)
    return float(match.group(1).replace(",", ".")) if match else False


def format_days(days):
    """«3 días», «1 día», «2,5 días», «? días»."""
    if days is None:
        return "? días"
    shown = f"{days:g}".replace(".", ",")
    return f"{shown} día" if days == 1 else f"{shown} días"


def route_point(cell):
    """(nombre legible, destino del enlace o None) de un punto del Recorrido."""
    link = LINK_RE.search(cell or "")
    return strip_links(cell or "").strip(), (link.group(1).rstrip("\\").strip() if link else None)


def route_segments(body):
    """Tramos de la tabla «Recorrido» de una ruta, en orden: desde y hasta (nombre legible y destino del
    enlace, o None si el punto no es una entidad) y los días (número; None si no se saben; False si la
    celda no es válida). None si la nota no tiene esa tabla."""
    header, rows, inside = [], [], False
    for line in body:
        if line.startswith("## "):
            if inside:
                break
            inside = normalize(line[3:]) == normalize(ROUTE_SECTION)
            continue
        stripped = line.strip()
        if not inside:
            continue
        if not stripped.startswith("|"):
            if header:
                break  # la tabla terminó
            continue
        cells = [cell.strip() for cell in CELL_SPLIT_RE.split(stripped.strip("|"))]
        if not header:
            header = [normalize(cell) for cell in cells]
            continue
        if not any(cells) or all(SEPARATOR_CELL_RE.match(cell) for cell in cells if cell):
            continue
        start, start_link = route_point(table_cell(header, cells, "Desde"))
        end, end_link = route_point(table_cell(header, cells, "Hasta"))
        raw = table_cell(header, cells, "Días")
        rows.append({"desde": start, "desde_enlace": start_link, "hasta": end, "hasta_enlace": end_link,
                     "dias": days_value(raw), "dias_texto": strip_links(raw).strip()})
    return rows if header else None


def route_usable(props):
    """Si la ruta se puede recorrer hoy y se sabe por dónde va: solo esas cuentan para las distancias."""
    return first(props.get("situacion")) in ROUTE_USABLE and first(props.get("certeza")) != "dudosa"


def node_key(route, label, link):
    """Clave de un punto en el grafo: la nota del lugar, en minúsculas, o `<ruta>#<punto>` si no tiene nota."""
    return link.split("/")[-1].strip().lower() if link else f"{route.lower()}#{normalize(label)}"


def route_graph(vault, index, usable_only=True, skip=()):
    """(grafo, puntos) de las rutas: {nodo: [(otro nodo, días o None, ruta)]} y, de cada nodo, su texto
    legible y su enlace (`{"texto", "enlace"}`; el enlace es None en un punto sin nota). Por defecto, solo las rutas ciertas que se pueden recorrer hoy; `skip`, rutas que no cuentan
    (la que se está creando, para ver los caminos que ya había). Una ruta sin tabla de Recorrido cuenta
    como un tramo de su partida a su destino, con sus `dias`."""
    graph, points = {}, {}
    skipped = {name.lower() for name in skip}
    for entry in index:
        if entry["tipo"] != ROUTE_TYPE or entry["name"].lower() in skipped or entry["estado"] == "archivado" \
                or (usable_only and not route_usable(entry["props"])):
            continue
        _, body = split_note((vault / entry["path"]).read_text(encoding="utf-8"))
        segments = route_segments(body) or []
        if not segments:
            start, end = (link_value(first(entry["props"].get(k))) for k in ("partida", "destino"))
            if start and end:
                total = days_value(first(entry["props"].get("dias")))
                segments = [{"desde": start.replace("_", " "), "desde_enlace": start, "hasta": end.replace("_", " "),
                             "hasta_enlace": end, "dias": total}]
        for segment in segments:
            if not segment["desde"] or not segment["hasta"]:
                continue
            a = node_key(entry["name"], segment["desde"], segment["desde_enlace"])
            b = node_key(entry["name"], segment["hasta"], segment["hasta_enlace"])
            if a == b:
                continue
            days = None if segment["dias"] is False else segment["dias"]
            points.setdefault(a, {"texto": segment["desde"], "enlace": segment["desde_enlace"]})
            points.setdefault(b, {"texto": segment["hasta"], "enlace": segment["hasta_enlace"]})
            graph.setdefault(a, []).append((b, days, entry["name"]))
            graph.setdefault(b, []).append((a, days, entry["name"]))
    return graph, points


def shortest_route(graph, start, goal):
    """(días, tramos) del camino más rápido conocido entre dos nodos; cada tramo es (desde, hasta, días,
    ruta). None si no hay un camino con todos sus días conocidos."""
    if start == goal:
        return 0.0, []
    order = itertools.count()
    queue, best = [(0.0, next(order), start, [])], {start: 0.0}
    while queue:
        days, _, node, path = heapq.heappop(queue)
        if node == goal:
            return days, path
        if days > best.get(node, math.inf):
            continue
        for other, length, route in graph.get(node, []):
            if length is None:
                continue
            total = days + length
            if total < best.get(other, math.inf) - 1e-9:
                best[other] = total
                heapq.heappush(queue, (total, next(order), other, path + [(node, other, length, route)]))
    return None


def nearest_places(graph, start, limit=6):
    """[(nodo, días)] de los lugares más cercanos a un nodo por las rutas, del más cercano al más lejano
    (solo los nodos con nota, no los puntos sueltos de una ruta)."""
    best, queue, order = {start: 0.0}, [(0.0, 0, start)], itertools.count(1)
    while queue:
        days, _, node = heapq.heappop(queue)
        if days > best.get(node, math.inf):
            continue
        for other, length, _ in graph.get(node, []):
            if length is not None and days + length < best.get(other, math.inf) - 1e-9:
                best[other] = days + length
                heapq.heappush(queue, (days + length, next(order), other))
    found = sorted((days, node) for node, days in best.items() if node != start and "#" not in node)
    return [(node, days) for days, node in found[:limit]]


def route_components(graph):
    """{nodo: componente}: dos lugares están en el mismo si alguna cadena de rutas los une, aunque no se
    sepa cuánto se tarda."""
    component, current = {}, 0
    for start in graph:
        if start in component:
            continue
        current += 1
        component[start], stack = current, [start]
        while stack:
            for other, _, _ in graph[stack.pop()]:
                if other not in component:
                    component[other] = current
                    stack.append(other)
    return component


def place_node(name, graph, by_name, seen=None):
    """(nodo, lugar por el que se llega) de un lugar en el grafo: el propio lugar si alguna ruta pasa por
    él; si no, el sitio que lo contiene (su `ubicacion`), subiendo. (None, None) si ninguno tiene rutas."""
    key = name.lower()
    if key in graph:
        return key, name
    seen = seen if seen is not None else set()
    entry = by_name.get(key)
    if not entry or key in seen:
        return None, None
    seen.add(key)
    for prop in CONTAINER_PROPS:
        for target in entry["relaciones"].get(prop, []):
            node, via = place_node(target, graph, by_name, seen)
            if node:
                return node, via
    return None, None


def place_region(entry, by_name, seen=None):
    """La región (nota de tipo `region`) donde está un lugar, subiendo por su `region` o su `ubicacion`;
    None si no se sabe."""
    seen = seen if seen is not None else set()
    for prop in ("region", "ubicacion"):
        for target in entry["relaciones"].get(prop, []):
            other = by_name.get(target.lower())
            if not other or other["name"] in seen:
                continue
            seen.add(other["name"])
            if other["tipo"] == "region":
                return other
            found = place_region(other, by_name, seen)
            if found:
                return found
    return None


def connection_candidates(vault, index):
    """Lo que debería estar unido por una ruta y no lo está, para que el motor lo conecte:
      - `vecinos`: dos asentamientos vecinos sin ningún camino entre ellos;
      - `capital`: un asentamiento importante (relevancia 3 o más) sin camino hasta la capital de su región
        (o, sin capital, hasta el asentamiento con rutas más importante de la región);
      - `regiones`: dos regiones vecinas que ninguna ruta une;
      - `aislado`: un lugar importante al que no llega ninguna ruta, ni al sitio donde está, y que no tiene
        con quién unirse: la ruta llega a él desde donde diga su contexto (una ruina, un santuario, una torre).
    Un lugar está unido a lo que está unido el sitio que lo contiene (la taberna, a lo de su ciudad). Cada
    uno con su partida, su destino (None si lo decide el contexto), sus puntos y sus razones."""
    graph, _ = route_graph(vault, index)
    components = route_components(graph)
    by_name = {e["name"].lower(): e for e in index}

    def wanted(entry, minimum=1):
        props = entry["props"]
        if entry["tipo"] not in CONNECTABLE_TYPES or entry["estado"] == "archivado"                 or first(props.get("situacion")) in UNREACHABLE_SITUATIONS:
            return False
        if entry["tipo"] == "lugar" and first(props.get("categoria")) in CROSSED_CATEGORIES:
            return False
        return (entry["relevancia"] or 0) >= minimum

    def reached(entry):
        """Componentes del lugar y de los sitios que lo contienen."""
        found, seen, stack = set(), set(), [entry["name"]]
        while stack:
            key = stack.pop().lower()
            if key in seen:
                continue
            seen.add(key)
            if key in components:
                found.add(components[key])
            item = by_name.get(key)
            for prop in CONTAINER_PROPS:
                stack += item["relaciones"].get(prop, []) if item else []
        return found

    def relevance(entry):
        return entry["relevancia"] or 2

    candidates, seen_pairs, placed = [], set(), set()

    def add(reason, start, end, points, why):
        pair = tuple(sorted(e["name"].lower() for e in (start, end) if e))
        if pair in seen_pairs:
            return
        seen_pairs.add(pair)
        placed.update(pair)
        candidates.append({"motivo": reason, "partida": start["name"], "destino": end["name"] if end else None,
                           "puntos": points, "razones": why})

    # Vecinos sin camino entre ellos
    for entry in index:
        if entry["tipo"] != "asentamiento" or not wanted(entry):
            continue
        for target in entry["relaciones"].get("vecinos", []):
            other = by_name.get(target.lower())
            if other and other["name"] != entry["name"] and wanted(other) and not reached(entry) & reached(other):
                add("vecinos", entry, other, 4 + round((relevance(entry) + relevance(other)) / 2),
                    [f"[[{entry['name']}]] y [[{other['name']}]] son vecinos y ningún camino los une"])

    # Los asentamientos importantes de cada región, unidos a su capital (o al más importante con rutas)
    members = {}
    for entry in index:
        if entry["tipo"] == "asentamiento" and wanted(entry, 3):
            region = place_region(entry, by_name)
            if region:
                members.setdefault(region["name"], []).append(entry)
    for region_name, places in members.items():
        region = by_name[region_name.lower()]
        capital = next((by_name[t.lower()] for t in region["relaciones"].get("capital", []) if t.lower() in by_name),
                       None)
        hub = capital or max((p for p in places if reached(p)), key=relevance, default=None)
        if not hub:
            continue
        for place in places:
            if place["name"] != hub["name"] and not reached(place) & reached(hub):
                what = "la capital" if hub is capital else "el asentamiento con rutas más importante"
                add("capital", place, hub, 2 + relevance(place) + (1 if relevance(hub) >= 4 else 0),
                    [f"[[{place['name']}]] no tiene camino hasta {what} de [[{region['name']}]], [[{hub['name']}]]"])

    # Regiones vecinas que ninguna ruta une
    touched = {}
    for entry in index:
        if entry["tipo"] == ROUTE_TYPE and route_usable(entry["props"]):
            for target in entry["relaciones"].get("regiones", []):
                touched.setdefault(target.lower(), set()).add(entry["name"])
    for entry in index:
        if entry["tipo"] != "region" or entry["estado"] == "archivado":
            continue
        for target in entry["relaciones"].get("vecinos", []):
            other = by_name.get(target.lower())
            if other and other["tipo"] == "region"                     and not touched.get(entry["name"].lower(), set()) & touched.get(other["name"].lower(), set()):
                add("regiones", entry, other, 3 + round((relevance(entry) + relevance(other)) / 2),
                    [f"[[{entry['name']}]] y [[{other['name']}]] son vecinas y ninguna ruta las une"])

    # Lugares importantes a los que no llega nada
    for entry in index:
        if wanted(entry, 3) and not reached(entry) and entry["name"].lower() not in placed:
            add("aislado", entry, None, 1 + relevance(entry),
                [f"a [[{entry['name']}]] no llega ninguna ruta, ni al sitio donde está"])
    candidates.sort(key=lambda c: -c["puntos"])
    return candidates


# --- Menciones sin enlace ----------------------------------------------------
# Toda entidad va enlazada cada vez que se nombra; solo los términos (rangos, títulos, oficios,
# expresiones, meses…) van al Glosario sin enlace. Este detector busca en el cuerpo:
#   - nombres propios sin enlace, para enlazarlos o, si son términos, registrarlos en el Glosario;
#   - entidades que el Glosario registra como tales (su Tipo es un tipo de entidad) y que la nota
#     nombra sin enlazar, aunque vayan en minúscula («la feria de los faroles»).

NAME_CONNECTORS = {"de", "del", "la", "las", "los", "el", "y", "e"}
ARTICLES = ("el ", "la ", "los ", "las ")
NAME_TOKEN_RE = re.compile(r"[^\W\d_][\w'’]*|\S")
SENTENCE_STARTERS = {".", "!", "?", ":", "«", "(", "—", "-", "*", '"', "“", "¿", "¡", ">", "+"}
# Palabras con las que el Tipo de una fila del Glosario dice que es una entidad, además de los tipos
# de los módulos y de los previstos (known_types); cualquier otro Tipo (rango, título, oficio,
# expresión…) es un término
ENTITY_KIND_WORDS = {
    "ciudad", "villa", "aldea", "pueblo", "poblado", "barrio", "fortaleza", "castillo", "templo", "ruina",
    "rio", "lago", "mar", "monte", "montana", "cordillera", "sierra", "bosque", "isla", "istmo", "desierto",
    "valle", "paso", "camino", "ruta", "calzada", "sendero", "senda", "vado", "tunel", "portal", "persona",
    "figura", "heroe", "rey", "reina", "orden", "gremio", "consejo", "compania", "secta", "ejercito", "banda",
    "alianza", "casa", "dinastia", "clan", "familia", "batalla", "guerra", "catastrofe", "tratado",
    "religion", "culto", "fe", "dios", "diosa", "espiritu", "demonio", "bestia", "monstruo", "lengua",
    "dialecto", "escritura", "fiesta", "festividad", "leyenda", "profecia", "cuento", "libro", "cancion",
    "poema", "enfermedad", "plaga", "mineral", "planta", "astro", "reliquia", "artefacto", "arma", "joya",
    "magia", "tecnologia", "ley"}


def comparable(text):
    """Texto normalizado y sin signos, palabra a palabra."""
    return " ".join(re.sub(r"[^0-9a-z]+", " ", normalize(text or "")).split())


def bare_name(text):
    """Forma de comparar un nombre: normalizada, sin lo que va entre paréntesis ni el artículo inicial
    («jueces (los nueve)» → «jueces», «el Paso» → «paso»)."""
    key = comparable(re.sub(r"\(.*?\)", " ", text or ""))
    return next((key[len(a):] for a in ARTICLES if key.startswith(a)), key)


def split_terms(cell):
    """Los términos de una celda del Glosario («A / B», «A, B, C»), sin comillas ni enlaces."""
    cell = strip_links(cell).replace("«", "").replace("»", "").replace("*", "")
    return [t.strip() for t in re.split(r"\s*/\s*|,\s*", cell) if t.strip()]


def is_entity_kind(kind, types):
    """Si el Tipo de una fila del Glosario es un tipo de entidad (por su primera palabra, también
    en plural: «Lugar (parte de región)», «Costumbres», «Ciudad»)."""
    words = re.sub(r"\(.*?\)", " ", normalize(kind)).replace("_", " ").split()
    if not words:
        return False
    word = words[0]
    forms = {word, word[:-1] if word.endswith("s") else word, word[:-2] if word.endswith("es") else word}
    return bool(forms & (set(types) | ENTITY_KIND_WORDS))


def glossary_table(vault):
    """Filas de la tabla del Glosario: {termino (la celda tal cual), nombres, tipo, nota, definicion}."""
    path = vault / GLOSSARY
    rows = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line.strip().strip("|"))]
        if not line.strip().startswith("|") or len(cells) < 2 or normalize(cells[0]) in ("termino", "") \
                or SEPARATOR_CELL_RE.match(cells[0]):
            continue
        cells += [""] * (4 - len(cells))
        rows.append({"termino": cells[0], "nombres": split_terms(cells[0]), "tipo": cells[1],
                     "nota": cells[2], "definicion": cells[3]})
    return rows


def glossary_rows(vault):
    """[(nombres, Tipo)] de las filas de la tabla del Glosario."""
    return [(row["nombres"], row["tipo"]) for row in glossary_table(vault)]


def glossary_terms(vault, entity_types=()):
    """(términos, entidades) del Glosario. Términos: todos los nombres de sus filas, normalizados.
    Entidades: {nombre comparable (bare_name): (nombre, Tipo)} de las filas cuyo Tipo es un tipo de
    entidad (`entity_types` o ENTITY_KIND_WORDS)."""
    terms, entities = set(), {}
    for names, kind in glossary_rows(vault):
        terms.update(normalize(term) for term in names)
        if is_entity_kind(kind, entity_types):
            entities.update({bare_name(term): (term, kind) for term in names if bare_name(term)})
    return terms, entities


def entity_labels(index, gaps):
    """Nombres de las entidades, existan (título y alias) o estén pendientes (su enlace), en forma
    normalizada: aunque estén en el Glosario, el detector no los deja pasar sin enlace."""
    labels = {normalize(label) for entry in index for label in [entry["titulo"], *entry["aliases"]] if label}
    return labels | {normalize(gap["link"]) for gap in gaps}


def note_link_labels(text):
    """Nombres comparables (bare_name) de los enlaces de un texto: sus destinos y sus textos visibles
    (sin los de archivos, como las imágenes)."""
    labels = set()
    for target, alias in LINK_WITH_ALIAS_RE.findall(text):
        if ATTACHMENT_RE.search(target.strip()):
            continue
        labels.add(bare_name(target.replace("_", " ")))
        if alias:
            labels.add(bare_name(alias))
    return labels - {""}


def prose_lines(body):
    """Líneas del cuerpo donde se buscan menciones: sin bloques de código, títulos ni la sección Imagen."""
    in_code, section = False, ""
    for line in body:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped:
            continue
        if stripped.startswith("#"):
            section = normalize(stripped.lstrip("#"))
            continue
        if section != "imagen":
            yield stripped


def unlinked_entities(body, entities, own):
    """[(nombre, Tipo)] de las entidades del Glosario ({nombre comparable: (nombre, Tipo)}) que el
    cuerpo nombra sin enlace en alguna de sus menciones (toda mención va enlazada), en mayúscula o en
    minúscula. `own`: nombres comparables de la propia entidad, que no se enlaza a sí misma."""
    plain = (LINK_WITH_ALIAS_RE.sub(" ", INLINE_CODE_RE.sub(" ", line)) for line in prose_lines(body))
    text = f" {comparable(' '.join(plain))} "
    return [entities[name] for name in sorted(entities) if name not in own and f" {name} " in text]


def calendar_terms(calendars):
    """Nombres de meses, días, estaciones y sufijos de los calendarios, normalizados."""
    terms = set()
    for calendar in calendars:
        terms.update(normalize(m["nombre"]) for m in calendar["meses"])
        terms.update(normalize(day) for day in calendar["semana"])
        terms.update(normalize(s["nombre"]) for s in calendar["estaciones"])
        terms.update(normalize(s) for s in (calendar["sufijo"], calendar["sufijo_negativo"]) if s)
    return terms


# Palabras que, con mayúscula, suelen ser solo el principio de una frase
LEADING_WORDS = {"en", "por", "para", "con", "sin", "desde", "hasta", "pero", "cuando", "si", "como", "que",
                 "donde", "tras", "ante", "entre", "hacia", "segun", "sobre", "bajo", "durante", "mientras",
                 "aunque", "porque", "pues", "ya", "no", "solo", "nadie", "todos", "todo", "toda", "todas",
                 "cada", "algunos", "algunas", "unos", "unas", "otros", "otras", "su", "sus", "este", "esta",
                 "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella", "hoy", "nunca", "siempre",
                 "tambien", "tampoco", "asi", "entonces", "luego", "despues", "antes", "al", "a", "lo", "le",
                 "les", "se", "un", "una", "muchos", "muchas", "pocos", "pocas", "ni", "o", "u", "mas"}
# Conectores que unen dos nombres distintos, no las palabras de un mismo nombre
JOINING_CONNECTORS = {"y", "e"}


def is_capitalized(token):
    return token[:1].isalpha() and token[:1].isupper()


def name_candidates(text):
    """[(nombre, suelto)] de un fragmento: palabras con mayúscula inicial, solas o unidas por de, la,
    los, «de las», «y»… `suelto` dice si es una sola palabra al principio de una frase, que puede
    ser solo su mayúscula. Las palabras de frase que van delante (En, Por, Solo…) no son parte del
    nombre, y los enlaces no cuentan."""
    text = LINK_WITH_ALIAS_RE.sub(" \x00 ", INLINE_CODE_RE.sub(" ", text))
    tokens = NAME_TOKEN_RE.findall(text)
    found, i, start = [], 0, True
    while i < len(tokens):
        if not (is_capitalized(tokens[i]) and len(tokens[i]) > 1):
            start = tokens[i] in SENTENCE_STARTERS
            i += 1
            continue
        j, words = i, []
        while j < len(tokens):
            if is_capitalized(tokens[j]):
                words.append(tokens[j])
                j += 1
                continue
            # Conectores («de», «de las»…) solo si detrás sigue otra palabra con mayúscula
            k = j
            while k < len(tokens) and tokens[k].lower() in NAME_CONNECTORS:
                k += 1
            if k > j and k < len(tokens) and is_capitalized(tokens[k]):
                words += tokens[j:k]
                j = k
                continue
            break
        at_start = start
        # Delante del nombre puede ir una palabra de la frase: «En Puerto Viejo», «Solo Aldric»
        while words and normalize(words[0]) in LEADING_WORDS:
            words.pop(0)
            at_start = False
        # Al principio de la frase, una palabra seguida de un conector es de la frase («Guarda el
        # Libro»), salvo con «y» o «e», que unen dos nombres
        if at_start and len(words) > 1 and words[1].lower() in NAME_CONNECTORS - JOINING_CONNECTORS:
            words = words[1:]
            while words and words[0].lower() in NAME_CONNECTORS:
                words.pop(0)
            at_start = False
        if words:
            found.append((" ".join(words), at_start and sum(1 for w in words if is_capitalized(w)) < 2))
        i, start = j, False
    return found


def name_runs(text):
    """Nombres propios de un fragmento (ver name_candidates), sin las palabras sueltas al principio
    de una frase."""
    return [name for name, loose in name_candidates(text) if not loose]


def split_names(run):
    """Los nombres de una secuencia: dos nombres unidos por «y» o «e» son dos («Aldric y Tobin»)."""
    return [part for part in re.split(r"\s+[ye]\s+", run) if part]


def table_cells(line):
    return CELL_SPLIT_RE.split(line.strip("|")) if line.startswith("|") else [line]


def unlinked_mentions(body, labels, own):
    """{mención: veces} de los nombres sin enlace que nombran una entidad que la nota enlaza en otra
    parte: sus palabras están en el destino o en el texto de uno de sus enlaces («Aldric» por
    [[Aldric_Voss]]). Toda mención va enlazada, no solo la primera. Una palabra suelta al principio
    de una frase solo cuenta si la nota no la usa también en minúscula (así «Torre» al empezar una
    frase no se toma por un nombre si la nota habla de «la torre»). `own`: nombres comparables de la
    propia entidad, que no se enlaza a sí misma; pero si la nota usa ese mismo nombre como texto de un
    enlace a otra entidad, la mención es de esa otra («los Siete» en «La Huida de los Siete»)."""
    lines = list(prose_lines(body))
    lowercase = {normalize(token) for line in lines
                 for token in NAME_TOKEN_RE.findall(LINK_WITH_ALIAS_RE.sub(" ", line)) if token.islower()}
    label_words = [set(label.split()) - NAME_CONNECTORS for label in labels]
    own_words = [set(name.split()) - NAME_CONNECTORS for name in own]
    found = {}
    for line in lines:
        for cell in table_cells(line):
            for run, loose in name_candidates(cell):
                for name in split_names(run):
                    key = bare_name(name)
                    words = set(key.split()) - NAME_CONNECTORS
                    if not words or (key not in labels and any(words <= w for w in own_words if w)):
                        continue
                    if loose and normalize(name) in lowercase:
                        continue
                    if any(words <= w for w in label_words if w):
                        # «Los Varenne» y «Varenne» son la misma mención
                        name = re.sub(r"^(?:El|La|Los|Las)\s+", "", name)
                        found[name] = found.get(name, 0) + 1
    return found


def unlinked_names(body, known):
    """Nombres propios del cuerpo que no se reconocen: ni enlazados en la nota ni en `known`
    (nombres normalizados: los enlaces y títulos de la nota, los términos del Glosario, los meses…).
    Se saltan los bloques de código, los títulos y la sección Imagen."""
    known_words = [set(k.split()) - NAME_CONNECTORS for k in known]
    found, found_words = [], []
    for line in prose_lines(body):
        cells = table_cells(line)
        if line.startswith("|") and all(SEPARATOR_CELL_RE.match(c.strip()) for c in cells if c.strip()):
            continue
        for name in (part for cell in cells for run in name_runs(cell) for part in split_names(run)):
            # Un término conocido pegado delante no es parte del nombre: «412 UE la Gran Sequía…»
            parts = name.split()
            while len(parts) > 1 and normalize(parts[0]) in known:
                parts.pop(0)
                while parts and parts[0].lower() in NAME_CONNECTORS:
                    parts.pop(0)
            name = " ".join(parts)
            key = normalize(name)
            bare = next((key[len(a):] for a in ARTICLES if key.startswith(a)), key)
            words = set(bare.split()) - NAME_CONNECTORS
            if not words or key in known or bare in known or any(words <= k for k in known_words):
                continue
            # Sin repetir: «Gran Sequía» ya está dentro de «La Gran Sequía»
            if any(words <= w for w in found_words):
                continue
            found.append(name)
            found_words.append(words)
    return found
