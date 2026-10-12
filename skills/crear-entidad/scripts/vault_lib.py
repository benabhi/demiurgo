"""Biblioteca común de los scripts de crear-entidad y expandir-mundo.

Lee la bóveda como la entiende Obsidian: enlaces, frontmatter, módulos de tipos, la Ficha
del Mundo y un índice compacto con una entrada por entidad. No tiene línea de comandos."""
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
# El registro no cuenta como una nota que nombra entidades
DEFAULT_EXCLUDED = ("00_Sistema/01_Plantillas", "00_Sistema/03_Archivados", PENDING_NOTE)


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
    del módulo reserva para una relevancia mayor, con sus subsecciones. El resto es el núcleo.
    La sección Mapa solo la necesita una nota a la que le toca mapa (por su categoría y su relevancia,
    según la regla `mapa` del módulo); sin las propiedades de la nota, cuenta como no necesaria."""
    depth = module.get("profundidad", {})
    needs_map = bool(map_applies(module, props, relevance)) if props is not None else False
    omitted, parent_omitted = [], False
    for level, title in template_sections(template_body):
        own = depth.get(title, 1) > relevance
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
MAP_ITEM_RE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+·\s+(.+?)\s+[—–-]\s+(.*)$")
MAP_POSITION_RE = re.compile(r"^(?:nivel\s+(\d+)\s*,\s*)?([a-z]+)$")
CONNECTS_RE = re.compile(r"Conecta con ([\d ,y]+?)\.", re.IGNORECASE)


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


def format_connections(numbers):
    """«Conecta con 2.», «Conecta con 2 y 5.», «Conecta con 1, 3 y 5.»"""
    numbers = [str(n) for n in sorted(set(numbers))]
    if not numbers:
        return ""
    joined = numbers[0] if len(numbers) == 1 else ", ".join(numbers[:-1]) + " y " + numbers[-1]
    return f"Conecta con {joined}."


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
        if not re.match(r"^\d+\.", stripped) or re.match(r"^\d+\.\s*$", stripped):
            continue
        match = MAP_ITEM_RE.match(stripped)
        if not match:
            problems.append(f"zona de la leyenda con formato no válido: «{stripped}» (debe ser "
                            f"`N. **Nombre** · orientación — descripción.`)")
            continue
        number, name, position, rest = match.groups()
        place = MAP_POSITION_RE.match(normalize(position))
        orientation = ORIENTATION_SYNONYMS.get(place.group(2), place.group(2)) if place else ""
        if orientation not in ORIENTATIONS:
            problems.append(f"zona {number}: orientación no válida «{position}» (una de: {', '.join(ORIENTATIONS)}; "
                            f"en una mazmorra, con su nivel: «nivel 2, norte»)")
        link = LINK_RE.search(name)
        connects = CONNECTS_RE.search(rest)
        zones.append({"numero": int(number), "linea": i, "nombre": strip_links(name).strip(),
                      "enlace": link.group(1).rstrip("\\").strip() if link else None,
                      "nivel": int(place.group(1)) if place and place.group(1) else 1,
                      "orientacion": orientation,
                      "conecta": [int(n) for n in re.findall(r"\d+", connects.group(1))] if connects else [],
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
        for other in zone["conecta"]:
            if other == zone["numero"] or other not in known:
                errors.append(f"leyenda del mapa: la zona {zone['numero']} conecta con {other}, que no existe")
            elif not any(z["numero"] == other and zone["numero"] in z["conecta"] for z in zones):
                warnings.append(f"leyenda del mapa: la zona {zone['numero']} conecta con {other}, pero {other} no "
                                f"conecta con {zone['numero']} (las conexiones van en los dos sentidos)")
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


def map_status(module, props, zones, relevance):
    """Estado del mapa de una nota: si le toca leyenda, su clase, la edición, cuántas zonas hay y cuántas
    faltan por cartografiar, y si toca dibujar (`toca`: "primera", "nueva" o None, con su razón y
    los niveles que hay que dibujar)."""
    rule = map_applies(module, props, relevance)
    zones = zones or []
    edition = int_value(first(props.get("mapa_edicion"))) or 0
    charted = int_value(first(props.get("mapa_zonas"))) or 0
    uncharted = [z for z in zones if z["numero"] > charted] if edition else list(zones)
    status = {"aplica": bool(rule), "clase": rule["clase"] if rule else None,
              "desde": rule["desde"] if rule else None, "edicion": edition, "zonas": len(zones),
              "cartografiadas": len(zones) - len(uncharted) if edition else 0,
              "sin_cartografiar": len(uncharted) if edition else 0, "toca": None, "niveles": [], "razon": ""}
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
    elif uncharted and (len(uncharted) >= NEW_EDITION_ZONES or 4 * len(uncharted) >= max(charted, 1)):
        status.update(toca="nueva", niveles=sorted({z["nivel"] for z in uncharted}),
                      razon=f"{len(uncharted)} zona(s) sin cartografiar")
    elif uncharted:
        status["razon"] = (f"{len(uncharted)} zona(s) sin cartografiar; la edición nueva toca con "
                           f"{NEW_EDITION_ZONES} o con un cuarto de las cartografiadas")
    return status


def date_keys(module):
    """(propiedad de inicio, propiedad de fin) de un tipo: las dos primeras de sus `fechas`
    (`nacimiento` y `muerte`, `inicio` y `fin`, `fundacion` y `abandono`…), con None si faltan."""
    keys = list(module.get("fechas", [])) + [None, None]
    return keys[0], keys[1]


def place_types(modules=None):
    """Tipos de la familia `lugar` (región, asentamiento…): los que pueden contener a otros."""
    modules = modules if modules is not None else load_modules()
    return {tipo for tipo, module in modules.items() if module.get("familia") == "lugar"}


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
    return {t for t in types if t}


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
        properties = {o["property"] for o in gap["occurrences"] if o["property"]}
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


def describe_expected(gap):
    """Texto del tipo esperado y de los módulos que pueden completarlo."""
    expected = gap["expected_type"]
    if not expected:
        return "desconocido"
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
        return {"props": {}, "ano_actual": None, "foco": "", "calendario": ""}
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
            "foco": body_field("Foco inicial"), "calendario": body_field("Calendario", "Presente y calendario")}


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
    "valle", "paso", "camino", "ruta", "calzada", "persona", "figura", "heroe", "rey", "reina", "orden",
    "gremio", "consejo", "compania", "secta", "ejercito", "banda", "alianza", "casa", "dinastia", "clan",
    "familia", "batalla", "guerra", "catastrofe", "tratado", "religion", "culto", "fe", "dios", "diosa",
    "espiritu", "demonio", "bestia", "monstruo", "lengua", "dialecto", "escritura", "fiesta", "festividad",
    "leyenda", "profecia", "cuento", "libro", "cancion", "poema", "enfermedad", "plaga", "mineral", "planta",
    "astro", "reliquia", "artefacto", "arma", "joya", "magia", "tecnologia", "ley"}


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
