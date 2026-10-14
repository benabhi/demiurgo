#!/usr/bin/env python3
"""Valida notas creadas con crear-entidad contra las reglas de su módulo.

Comprueba:
  - frontmatter: YAML válido, todas las propiedades de la plantilla, tipo, estado,
    origen, relevancia (1 a 5), fecha sin comillas, fechas del mundo numéricas,
    en orden (inicio antes que fin) y coherentes con la edad, las escalas y los
    valores permitidos que declara el módulo, las propiedades que solo valen con ciertos valores
    de otra (`solo_si`) y propiedades de relación con solo enlaces;
  - cuerpo: título con el emoji del tipo, las secciones de la plantilla que pide su relevancia
    (el núcleo siempre; las de la `profundidad` del módulo, desde su relevancia mínima),
    ningún campo vacío ni texto de plantilla sin reemplazar;
  - que la nota esté en la carpeta que le corresponde según su módulo;
  - enlaces pendientes (a entidades que aún no tienen nota): los que solo nombra esta nota, dentro
    del rango del módulo escalado por su relevancia, y todos con tipo (su propiedad de relación o el registro de pendientes);
  - entidades sin enlace en el cuerpo (avisos), porque toda mención va enlazada y no solo la primera:
    las que el Glosario registra como entidades (por su Tipo), aunque vayan en minúscula; las que la
    nota ya enlaza en otra parte, también con el nombre corto; y los nombres propios que no son meses
    ni términos del Glosario;
  - enlaces del cuerpo con texto legible (un aviso si Obsidian va a mostrar guiones bajos);
  - que la nota no enlace a un secreto y que su imagen exista;
  - en los lugares con mapa (regla `mapa` del módulo): la sección Mapa cuando le toca por su categoría
    y su relevancia, y su leyenda (números del 1 al N sin repetir ni saltar, orientaciones válidas,
    conexiones con zonas que existen y en los dos sentidos, como mucho 12 zonas por nivel), las rutas
    que lo cruzan (bloque «Rutas»: zonas que existen y que la leyenda conecta), y que las imágenes de
    `mapa` existan y vayan embebidas, con `mapa_edicion` y `mapa_zonas` coherentes;
  - en un calendario, las tablas que leen los scripts (meses, estaciones, festividades);
  - en una costumbre, que solo las festividades lleven `calendario` y `fecha`, y que la fiesta esté en la
    tabla «Festividades» de su calendario con la misma fecha y un mes que existe (avisos);
  - en una ruta, su Recorrido: días que son números (o «?»), tramos encadenados de la partida al destino
    (o de vuelta a la partida, en una circular), que suman los días de `dias`, y sus paradas en él y en
    el mismo orden (avisos);
  - en los tipos con `tiempo` en su módulo (era, evento), su situación frente al año actual (lo
    que sigue en curso no tiene fin, lo pasado no termina en el futuro, lo profetizado no ha
    empezado) y su cronología dentro de sus fechas y en orden (avisos);
  - `fecha_exacta`, con los nombres del calendario de referencia y del mismo año que la fecha
    que precisa (la que indica el módulo, como `nacimiento`).
Las notas internas (MOC, Ficha, Preguntas Abiertas, Glosario, guías y registros) no son entidades:
lo dice y no las valida. Sale con código 1 si encuentra errores.

Con --depth <tipo>:<relevancia>[:<categoría>], antes de escribir una nota, dice qué secciones lleva,
cuántos enlaces pendientes nuevos puede abrir y si le toca mapa, sin validar nada.

Ejemplo:  check_note.py Aldric_Voss   check_note.py 20_Personajes/X.md 80_Secretos/Y.md
          check_note.py --depth personaje:2   check_note.py --depth lugar:3:mazmorra"""
import argparse
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (DAY_MONTH_RE, HIDDEN_DIRS, LINK_WITH_ALIAS_RE, OPTIONAL_PROPS, QUOTED_LINK_RE, ROUTE_TYPE,  # noqa: E402
                       SKILL_DIR, VARIATION_SELECTOR, bare_name, calendar_terms, date_keys, days_value,
                       display_title, format_days, link_value, route_segments,
                       entity_labels, find_gaps, first, format_year, glossary_terms, index_vault, int_value,
                       is_empty_value, is_system_note, known_types, link_exists, load_calendars, load_index,
                       load_modules, malformed_lines, MAP_ITEM_EMPTY_RE, map_applies, map_key_problems, map_rule,
                       normalize, note_link_labels, omitted_sections, own_gaps_range, parse_calendar,
                       map_routes_problems, parse_map_key, parse_map_routes,
                       parse_exact_date, parse_frontmatter, parse_moment, parse_note, read_world,
                       reference_calendar, resolve_note, section_table, split_note, table_cell,
                       unlinked_entities, unlinked_mentions, unlinked_names, unquote)
from vault_lib import CLOSING_NOTE, WORLD_CLOSED, WORLD_CLOSING, world_state  # noqa: E402
from vault_lib import vault_path  # noqa: E402

MAX_LOOSE = 10

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EMPTY_FIELD_RE = re.compile(r"^\s*- \*\*[^*]+:\*\*\s*$")
EMPTY_ROW_RE = re.compile(r"^\|(\s*\|)+\s*$")
# Enlace del cuerpo: (! si es un embed, destino, texto)
BODY_LINK_RE = re.compile(r"(!?)\[\[([^\]|#^]+?)\\?(?:[#^][^\]|]*)?(?:\\?\|([^\]]*))?\]\]")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
STATES = {"borrador", "canon", "archivado"}
ORIGINS = {"manual", "procedural"}
SECRETS_DIR = "80_secretos/"


def without_variation(text):
    """Quita el selector de variación de los emojis: 🗺️ y 🗺 cuentan como el mismo."""
    return text.replace(VARIATION_SELECTOR, "")


def expected_folder(module, props):
    """(carpeta esperada o None, error o None) según la regla `carpeta` del módulo."""
    rule = module.get("carpeta", {})
    if "fija" in rule:
        return rule["fija"], None
    if "propiedad" not in rule:
        return None, None
    key = rule["propiedad"]
    value = (props.get(key) or [""])[0].strip("\"'")
    if value not in rule["valores"]:
        allowed = ", ".join(rule["valores"])
        return None, f"`{key}` debe ser uno de: {allowed} (encontrado: {value or 'vacío'})"
    return rule["valores"][value], None


def timeline_problems(rule, keys, props, body, dates, world_year, calendar):
    """(errores, avisos) de los tipos con `tiempo` en su módulo (era, evento, asentamiento): su
    situación frente al año actual y su cronología (la tabla de la sección que indica) dentro de sus
    fechas y en orden. `presente`, `pasado` y `futuro` pueden ser un valor o una lista de valores."""
    errors, warnings = [], []
    key = rule.get("propiedad", "situacion")
    situation = first(props.get(key))
    start_key, end_key = keys
    start, end = dates.get(start_key), dates.get(end_key)

    def state(name):
        expected = rule.get(name)
        return situation in expected if isinstance(expected, list) else situation == expected

    present, past, future = state("presente"), state("pasado"), state("futuro")
    if present and end is not None:
        errors.append(f"con `{key}: {situation}` aún no ha terminado: deja `{end_key}` vacío")
    if world_year is not None:
        last = end if end is not None else start
        if present and start is not None and start > world_year:
            errors.append(f"con `{key}: {situation}`, `{start_key}` ({start}) no puede ser posterior al año actual ({world_year})")
        if past and last is not None and last > world_year:
            errors.append(f"con `{key}: {situation}`, no puede terminar ({last}) después del año actual ({world_year})")
        if future and start is not None and start <= world_year:
            errors.append(f"con `{key}: {situation}` todavía no ha empezado: `{start_key}` ({start}) va vacío "
                          f"o después del año actual ({world_year})")
    section = rule.get("cronologia")
    if calendar is None or not section:
        return errors, warnings
    # Sin `fin`, lo que sigue en curso llega hasta hoy y lo demás ocurrió en su año de inicio
    limit = end if end is not None else (None if present else start)

    def shown(year, missing):
        return format_year(calendar, year) if year is not None else missing

    span = f"{shown(start, '?')} – {shown(limit, 'hoy' if present else '?')}"
    header, rows = section_table(body, section)
    previous = None
    for row in rows:
        cell = table_cell(header, row, "Fecha")
        moment = parse_moment(cell, calendar) if cell else None
        if moment is None:
            continue  # fechas aproximadas o intervalos: no se comprueban
        year = moment[0]
        if (start is not None and year < start) or (limit is not None and year > limit):
            warnings.append(f"{section}: «{cell}» cae fuera de sus fechas ({span})")
        # El orden: por años y, dentro del mismo año, por mes y día si las dos filas los tienen
        if previous is not None and (year < previous[0] or (
                year == previous[0] and None not in (moment[1], previous[1]) and moment[1:] < previous[1:])):
            warnings.append(f"{section}: «{cell}» es anterior a la fila de arriba; ordénala de la más antigua a la más reciente")
        previous = moment
    return errors, warnings


def quote_separator(body, i):
    """Si la línea `>` sola de la posición i separa dos párrafos de una misma cita (un relato largo
    citado): no es un campo vacío."""
    def quoted(step):
        j = i + step
        while 0 <= j < len(body) and body[j].strip() == ">":
            j += step
        return 0 <= j < len(body) and body[j].strip().startswith(">")
    return quoted(-1) and quoted(1)


def festival_warnings(props, body, calendars):
    """Avisos de una costumbre con calendario: solo las festividades llevan `calendario` y `fecha`, la fecha
    usa los meses de ese calendario y la fiesta está en su tabla «Festividades» con la misma fecha."""
    warnings = []
    category = first(props.get("categoria"))
    target = link_value(first(props.get("calendario")) or "")
    date = first(props.get("fecha"))
    if category != "festividad":
        if target or date:
            warnings.append("`calendario` y `fecha` son de las festividades: en esta categoría quedan vacíos y el "
                            "texto dice cuándo se cumple")
        return warnings
    if not target:
        return warnings
    calendar = next((c for c in calendars if c["nombre"].lower() == target.lower()), None)
    if calendar is None:
        return warnings  # el calendario aún es un enlace pendiente
    title = next((display_title(line) for line in body if line.startswith("# ")), "")
    own = {normalize(title)} | {normalize(unquote(a)) for a in props.get("aliases", [])}
    row = next((f for f in calendar["festividades"] if normalize(f["nombre"]) in own), None)
    match = DAY_MONTH_RE.match(date) if date else None
    if match and normalize(match.group(2)) not in {normalize(m["nombre"]) for m in calendar["meses"]}:
        warnings.append(f"`fecha` («{date}»): «{match.group(2)}» no es un mes de [[{target}]]")
    if row is None:
        warnings.append(f"la festividad no está en la tabla «Festividades» de [[{target}]]: añade su fila"
                        + (f" con su fecha («{date}»)" if date else "") + " y su enlace en `festividades`")
    elif date and normalize(row["fecha"]) != normalize(date):
        warnings.append(f"`fecha` («{date}») no coincide con la de la tabla de [[{target}]] («{row['fecha']}»)")
    elif not date:
        warnings.append(f"falta `fecha`: en la tabla de [[{target}]] es «{row['fecha']}»")
    return warnings


def route_problems(props, body):
    """(errores, avisos) de una ruta: su Recorrido (cada tramo empieza donde acabó el anterior, el primero
    en la partida y el último en el destino o de vuelta en la partida; los días son números y suman
    `dias`) y sus paradas, que están en él y en el mismo orden."""
    errors, warnings = [], []
    layout = first(props.get("trazado"))
    uncertain = first(props.get("situacion")) == "perdida" or first(props.get("certeza")) == "dudosa"
    raw_total = first(props.get("dias"))
    total = days_value(raw_total) if raw_total else None
    if raw_total and total in (None, False):
        errors.append(f"`dias` debe ser un número de días (`6`, `2.5`) o quedar vacía (encontrado: {raw_total})")
        total = None
    elif not raw_total and not uncertain:
        warnings.append("falta `dias`: sin ella, la ruta no cuenta para las distancias del mundo")
    segments = route_segments(body)
    if segments is None:
        return errors, warnings  # sin la tabla: lo dice la comprobación de secciones o de campos vacíos
    if not segments:
        errors.append("el Recorrido no tiene tramos: al menos uno, de la partida al destino (o hasta donde se pierde)")
        return errors, warnings
    for i, segment in enumerate(segments, 1):
        if segment["dias"] is False:
            errors.append(f"Recorrido, tramo {i}: los días deben ser un número (`2`, `1,5`) o «?» si no se saben "
                          f"(encontrado: «{segment['dias_texto']}»)")
        elif segment["dias"] is None and not uncertain:
            warnings.append(f"Recorrido, tramo {i}: sin días («?»); en una ruta que se recorre, se saben")

    def same(label_a, link_a, label_b, link_b):
        if link_a or link_b:
            return bool(link_a and link_b) and link_a.split("/")[-1].lower() == link_b.split("/")[-1].lower()
        return normalize(label_a) == normalize(label_b)

    start = link_value(first(props.get("partida")) or "")
    end = link_value(first(props.get("destino")) or "")
    if layout != "red":
        for i in range(1, len(segments)):
            before, now = segments[i - 1], segments[i]
            if not same(before["hasta"], before["hasta_enlace"], now["desde"], now["desde_enlace"]):
                warnings.append(f"Recorrido: el tramo {i + 1} empieza en «{now['desde']}», pero el anterior acaba en "
                                f"«{before['hasta']}» (cada tramo empieza donde acabó el anterior)")
        first_point, last_point = segments[0], segments[-1]
        if start and not same(first_point["desde"], first_point["desde_enlace"], start, start):
            warnings.append(f"Recorrido: empieza en «{first_point['desde']}», pero `partida` es [[{start}]]")
        goal = end if layout == "lineal" else (start if layout == "circular" else None)
        if goal and not same(last_point["hasta"], last_point["hasta_enlace"], goal, goal):
            where = "`destino`" if layout == "lineal" else "su partida (es circular)"
            warnings.append(f"Recorrido: acaba en «{last_point['hasta']}», pero {where} es [[{goal}]]")
    known = [s["dias"] for s in segments if s["dias"] not in (None, False)]
    if total is not None and len(known) == len(segments):
        added = sum(known)
        if abs(added - total) > max(0.5, 0.1 * total):
            warnings.append(f"los días de los tramos del Recorrido suman {format_days(added)}, y `dias` dice "
                            f"{format_days(total)}")
    # Las paradas, en el Recorrido y en el mismo orden
    stops = [link_value(v) for v in props.get("paradas", []) if link_value(v)]
    order = []
    for segment in segments:
        for link in (segment["desde_enlace"], segment["hasta_enlace"]):
            key = link.split("/")[-1].lower() if link else None
            if key and key not in order:
                order.append(key)
    missing = [s for s in stops if s.lower() not in order]
    if missing:
        warnings.append("paradas que no están en el Recorrido: " + ", ".join(f"[[{s}]]" for s in missing))
    present = [s.lower() for s in stops if s.lower() in order]
    if present != sorted(present, key=order.index):
        warnings.append("`paradas` no va en el orden del Recorrido (de la partida al destino)")
    return errors, warnings


def check(path, vault, modules, names, paths, md_by_stem, world_year=None, calendar=None, gaps=None,
          known_terms=None, glossary_entities=None, calendars=None):
    errors, warnings = [], []
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_note(text)
    if frontmatter is None:
        return ["falta el frontmatter (debe empezar y terminar con ---)"], warnings, None

    props = parse_frontmatter(frontmatter, errors)
    note_type = (props.get("tipo") or [""])[0].strip("\"'")
    module = modules.get(note_type)
    if not module:
        return errors + [f"el tipo `{note_type}` no tiene módulo en crear-entidad"], warnings, note_type

    # Propiedades: las de la plantilla del tipo
    template_text = (SKILL_DIR / "tipos" / note_type / "plantilla.md").read_text(encoding="utf-8")
    template_fm, template_body = split_note(template_text)
    expected = parse_frontmatter(template_fm, [])
    for key in expected:
        if key not in props:
            errors.append(f"falta la propiedad `{key}`")
    for key in props:
        if key not in expected and key not in OPTIONAL_PROPS:
            warnings.append(f"propiedad que no está en la plantilla: `{key}`")

    # La etiqueta del tipo: el grafo de Obsidian colorea las notas por ella (graph_colors.py)
    if note_type not in [unquote(t).lstrip("#") for t in props.get("tags", [])]:
        warnings.append(f"falta la etiqueta del tipo en `tags` (`- {note_type}`): el grafo colorea las notas por ella")

    state = (props.get("estado") or [""])[0]
    if state not in STATES:
        errors.append(f"`estado` debe ser borrador, canon o archivado (encontrado: {state or 'vacío'})")
    origin = (props.get("origen") or [""])[0]
    if origin and origin not in ORIGINS:
        errors.append(f"`origen` debe ser manual o procedural (encontrado: {origin})")
    revision = (props.get("ultima_revision") or [""])[0]
    if revision.startswith(('"', "'")):
        errors.append(f"`ultima_revision` va sin comillas (encontrado: {revision})")
    elif not DATE_RE.match(revision):
        errors.append(f"`ultima_revision` debe ser una fecha AAAA-MM-DD (encontrado: {revision or 'vacío'})")

    # Relevancia: de 1 a 5. Decide la profundidad de la nota; si no es válida, se exige todo
    relevance = 5
    if "relevancia" in expected:
        raw_relevance = int_value(first(props.get("relevancia")))
        if raw_relevance is None or not 1 <= raw_relevance <= 5:
            shown = first(props.get("relevancia")) or "vacío"
            errors.append(f"`relevancia` debe ser un número del 1 al 5 (encontrado: {shown})")
        else:
            relevance = raw_relevance

    # Escalas y valores permitidos que declara el módulo (peligrosidad del 1 al 5, naturaleza…)
    for key, (low, high) in module.get("escalas", {}).items():
        raw = first(props.get(key))
        if raw and (int_value(raw) is None or not low <= int_value(raw) <= high):
            errors.append(f"`{key}` debe ser un número del {low} al {high} (encontrado: {raw})")
    for key, allowed in module.get("valores", {}).items():
        raw = first(props.get(key))
        if raw and raw not in allowed:
            errors.append(f"`{key}` debe ser uno de: {', '.join(allowed)} (encontrado: {raw})")
    # Propiedades que solo se usan con ciertos valores de otra (`solo_si`: el cumplimiento, solo en las
    # profecías): fuera de esa condición quedan vacías; dentro son obligatorias, salvo las fechas
    for key, condition in module.get("solo_si", {}).items():
        value = first(props.get(key))
        for other, allowed in condition.items():
            current = first(props.get(other))
            if current in allowed and not value and key not in module.get("fechas", []):
                errors.append(f"con `{other}: {current}`, `{key}` no puede quedar vacía")
            elif current not in allowed and value:
                errors.append(f"`{key}` solo se usa con `{other}`: {', '.join(allowed)} (aquí es "
                              f"{current or 'vacía'}): déjala vacía")

    # Fechas del mundo: números de años en el eje del calendario, o vacías
    dates = {}
    for key in module.get("fechas", []):
        raw = first(props.get(key))
        if not raw:
            continue
        if int_value(raw) is None:
            errors.append(f"`{key}` debe ser un número de años del calendario o quedar vacía (encontrado: {raw})")
        else:
            dates[key] = int_value(raw)
    start_key, end_key = date_keys(module)
    if start_key in dates and end_key in dates and dates[end_key] < dates[start_key]:
        errors.append(f"`{end_key}` ({dates[end_key]}) es anterior a `{start_key}` ({dates[start_key]})")
    age = int_value(first(props.get("edad")))
    alive = first(props.get("situacion_vital")) in ("", "vivo")
    if world_year is not None and "nacimiento" in dates and age is not None and alive:
        expected_age = world_year - dates["nacimiento"]
        if abs(expected_age - age) > 1:
            errors.append(f"`edad` ({age}) no cuadra con `nacimiento` ({dates['nacimiento']}) y el año actual "
                          f"({world_year}): debería ser {expected_age}")

    # Calendario: las tablas que leen los scripts (meses, estaciones, festividades)
    if note_type == "calendario":
        errors += parse_calendar(text, path.stem)["errores"]

    # Festividad: su calendario la tiene en su tabla «Festividades», con la misma fecha
    if note_type == "costumbre":
        warnings += festival_warnings(props, body, calendars or [])

    # Ruta: su Recorrido encadenado, con los días que suman los de `dias`, y sus paradas en él
    if note_type == ROUTE_TYPE:
        route_errors, route_warnings = route_problems(props, body)
        errors += route_errors
        warnings += route_warnings

    # Tiempo (era, evento): su situación frente al año actual y su cronología dentro de sus fechas
    if module.get("tiempo"):
        time_errors, time_warnings = timeline_problems(module["tiempo"], date_keys(module), props, body, dates,
                                                       world_year, calendar)
        errors += time_errors
        warnings += time_warnings

    # Fecha exacta: el día con los nombres del calendario de referencia, del año de la fecha que precisa
    exact = first(props.get("fecha_exacta"))
    refined = module.get("fecha_exacta")
    if exact and refined:
        if calendar is None:
            errors.append("`fecha_exacta` necesita el calendario de referencia, que aún no existe: déjala vacía")
        else:
            parsed, problem = parse_exact_date(exact, calendar)
            if problem:
                errors.append(f"`fecha_exacta` no es válida: {problem}")
            elif dates.get(refined) != parsed[0]:
                errors.append(f"`{refined}` debe ser {parsed[0]}, el año de `fecha_exacta` ({exact})")

    # Propiedades de relación: solo enlaces entre comillas, o vacías
    for key in module["relaciones"]:
        values = props.get(key, [])
        if is_empty_value(values):
            continue
        for value in values:
            if not QUOTED_LINK_RE.match(value):
                errors.append(f"`{key}`: solo admite enlaces entre comillas o quedar vacía (encontrado: {value})")
    errors += [f"enlace mal formado: {line}" for line in malformed_lines(text)]

    # Carpeta: la que manda el módulo (fija o según una propiedad, como el rol o la categoría)
    folder, folder_error = expected_folder(module, props)
    if folder_error:
        errors.append(folder_error)
    elif folder:
        try:
            actual = path.resolve().parent.relative_to(vault.resolve()).as_posix()
        except ValueError:
            actual = None
        if actual is None:
            errors.append("la nota no está dentro de la bóveda")
        elif actual.lower() != folder.lower():
            errors.append(f"la nota está en `{actual}` pero le corresponde `{folder}`")

    # Imagen: enlace a un archivo que exista, y embebido en el cuerpo
    image = props.get("imagen", [])
    if not is_empty_value(image):
        value = image[0]
        if not QUOTED_LINK_RE.match(value):
            errors.append(f"`imagen` debe ser un enlace entre comillas (encontrado: {value})")
        else:
            target = value[3:-3]
            if not link_exists(target, names, paths):
                errors.append(f"`imagen` apunta a un archivo que no existe: {target}")
            elif f"![[{target}" not in text:
                warnings.append(f"la imagen no está embebida en el cuerpo (`![[{target}|300]]`)")

    # Mapa: la leyenda de la sección Mapa y las imágenes de sus ediciones
    if module.get("mapa"):
        zones, problems = parse_map_key(body)
        errors += problems
        if zones is not None:
            key_errors, key_warnings = map_key_problems(zones)
            errors += key_errors
            warnings += key_warnings
        # Las rutas que cruzan el mapa (bloque «Rutas»): sus zonas existen y la leyenda las conecta
        routes, route_format = parse_map_routes(body)
        errors += route_format
        if routes:
            route_errors, route_warnings = map_routes_problems(routes, zones)
            errors += route_errors
            warnings += route_warnings
        edition, charted = first(props.get("mapa_edicion")), first(props.get("mapa_zonas"))
        for key, raw in (("mapa_edicion", edition), ("mapa_zonas", charted)):
            if raw and (int_value(raw) is None or int_value(raw) < 1):
                errors.append(f"`{key}` debe ser un número desde 1 o quedar vacía (encontrado: {raw})")
        maps = [value for value in props.get("mapa", []) if not is_empty_value([value])]
        for value in maps:
            if not QUOTED_LINK_RE.match(value):
                errors.append(f"`mapa` solo admite enlaces entre comillas a sus imágenes (encontrado: {value})")
            elif not link_exists(value[3:-3], names, paths):
                errors.append(f"`mapa` apunta a un archivo que no existe: {value[3:-3]}")
            elif f"![[{value[3:-3]}" not in text:
                warnings.append(f"el mapa no está embebido en la sección Mapa (`![[{value[3:-3]}|600]]`)")
        if maps and not int_value(edition):
            errors.append("`mapa` tiene imágenes pero `mapa_edicion` está vacía: tras dibujar una edición, "
                          "ejecuta `map_key.py <Nota> --charted`")
        if int_value(edition) and not maps:
            errors.append("`mapa_edicion` dice que hay una edición del mapa, pero `mapa` no tiene imágenes")
        if int_value(edition) and zones is None:
            errors.append("`mapa_edicion` dice que hay mapa, pero la nota no tiene sección Mapa")
        if zones and int_value(charted) and int_value(charted) > max(z["numero"] for z in zones):
            errors.append(f"`mapa_zonas` ({charted}) pasa del último número de la leyenda")

    # Cuerpo: título, secciones, campos vacíos y restos de la plantilla
    headings = [without_variation(line) for line in body if line.startswith("# ")]
    if not headings or not headings[0].startswith(f"# {without_variation(module['emoji'])} "):
        errors.append(f"el título debe empezar por el emoji del tipo: `# {module['emoji']} Nombre`")
    # Secciones: el núcleo siempre; las de la `profundidad` del módulo, desde su relevancia mínima.
    # Una sección opcional puede ir antes si tiene contenido real, pero nunca de relleno
    body_set = {line.strip() for line in body}
    optional = set(omitted_sections(module, template_body, relevance, props))
    for line in template_body:
        match = re.match(r"^#{2,3} (.+?)\s*$", line)
        if match and match.group(1) not in optional and line.strip() not in body_set:
            errors.append(f"falta la sección «{line.strip()}»")
    for i, line in enumerate(body):
        stripped = line.strip()
        following = next((l for l in body[i + 1:] if l.strip()), "")
        # Una etiqueta sin valor no está vacía si su contenido sigue en una sublista o un bloque de código
        has_content_below = bool(re.match(r"^\s+[-*] ", following)) or following.lstrip().startswith("```")
        if (EMPTY_FIELD_RE.match(line) and not has_content_below) or EMPTY_ROW_RE.match(stripped) \
                or stripped == "-" or MAP_ITEM_EMPTY_RE.match(stripped) \
                or (stripped == ">" and not quote_separator(body, i)):
            errors.append(f"campo vacío: {stripped}")
    leftovers = {l.strip() for l in template_body if l.startswith("> ") and len(l.strip()) > 2}
    for line in body:
        if line.strip() in leftovers or "{{" in line:
            errors.append(f"texto de plantilla sin reemplazar: {line.strip()}")

    # Enlaces pendientes (huecos): los que solo nombra esta nota son suyos y cuentan para el rango
    # del módulo; todos necesitan un tipo (su propiedad de relación o el registro)
    _, links = parse_note(text)
    try:
        relative = path.resolve().relative_to(vault.resolve()).as_posix()
    except ValueError:
        relative = None
    mine = [g for g in (gaps or []) if any(o["note"] == relative for o in g["occurrences"])]
    own = [g for g in mine if g["notes"] == [relative]]
    # Por encima del máximo es un error; por debajo del mínimo, un aviso: al completar un enlace
    # pendiente, la nota que lo nombraba se queda con menos, y está bien.
    low, high = own_gaps_range(module, relevance)
    # Con el mundo en cierre o cerrado no se piden enlaces pendientes nuevos. Que no se abra ninguno lo comprueba
    # el informe (report.py), que sabe qué es de esta vez: aquí, los de una nota anterior al cierre no son nuevos
    if world_state(vault) in (WORLD_CLOSING, WORLD_CLOSED):
        low = 0
    if len(own) > high:
        errors.append(f"enlaces pendientes nuevos: {len(own)} (con relevancia {relevance} el tipo admite entre {low} "
                      f"y {high}; deja sin nombre propio las entidades menos importantes)")
    elif len(own) < low:
        warnings.append(f"enlaces pendientes nuevos: {len(own)} (al crear la nota, con relevancia {relevance} el tipo "
                        f"pide entre {low} y {high})")
    for gap in mine:
        if not gap["expected_type"]:
            errors.append(f"el enlace pendiente [[{gap['link']}]] no tiene tipo: ponlo en su propiedad de relación "
                          f"o asígnaselo con `pending_links.py --set {gap['link']}=<tipo>`")

    # Entidades sin enlace: toda entidad que la nota nombra va enlazada cada vez que la nombra (salvo la
    # propia entidad, los títulos y la sección Imagen). Tres avisos: las que el Glosario registra como
    # entidades (aunque vayan en minúscula), las que la nota ya enlaza en otra parte y los nombres propios
    if known_terms is not None:
        frontmatter_aliases = {normalize(unquote(a)) for a in props.get("aliases", [])}
        linked = {normalize(t.replace("_", " ")) for t, _, _ in links}
        linked |= {normalize(alias) for _, alias in LINK_WITH_ALIAS_RE.findall(text) if alias}
        title = next((display_title(l) for l in body if l.startswith("# ")), path.stem.replace("_", " "))
        own_names = frontmatter_aliases | {normalize(title)}
        own = {bare_name(n) for n in own_names} - {""}
        missing = unlinked_entities(body, glossary_entities or {}, own)
        if missing:
            shown = ", ".join(f"«{term}» ({kind})" for term, kind in missing[:MAX_LOOSE]) + (
                f" y {len(missing) - MAX_LOOSE} más" if len(missing) > MAX_LOOSE else "")
            warnings.append(f"entidades del Glosario nombradas sin enlace: {shown}. Enlaza cada mención (a su nota o "
                            f"como enlace pendiente); si en realidad son términos, corrige su Tipo en el Glosario")
        repeated = unlinked_mentions(body, note_link_labels(text), own)
        if repeated:
            items = list(repeated.items())
            shown = ", ".join(f"«{name}»" + (f" ×{count}" if count > 1 else "") for name, count in items[:MAX_LOOSE]) + (
                f" y {len(items) - MAX_LOOSE} más" if len(items) > MAX_LOOSE else "")
            warnings.append(f"menciones sin enlace de entidades que la nota enlaza en otra parte: {shown}. Toda mención "
                            f"va enlazada, no solo la primera, también con el nombre corto: [[Nota|nombre]]")
        known = set(known_terms) | linked | own_names | {bare_name(term) for term, _ in missing}
        loose = unlinked_names(body, known)
        if loose:
            shown = ", ".join(f"«{n}»" for n in loose[:MAX_LOOSE]) + (f" y {len(loose) - MAX_LOOSE} más"
                                                                      if len(loose) > MAX_LOOSE else "")
            warnings.append(f"nombres propios sin enlace: {shown}. Si son entidades, enlaza cada mención "
                            f"(a su nota o como enlace pendiente); si son términos (un rango, un título, un oficio), "
                            f"regístralos en el Glosario")

    # Enlaces legibles: en el cuerpo, un enlace a un archivo con guiones bajos lleva su texto real
    unreadable, in_code = [], False
    for line in body:
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for embed, target, alias in BODY_LINK_RE.findall(INLINE_CODE_RE.sub("", line)):
            target = target.strip()
            if not embed and not (alias or "").strip() and "_" in target and target not in unreadable:
                unreadable.append(target)
    if unreadable:
        shown = ", ".join(f"[[{t}]]" for t in unreadable[:5]) + (" …" if len(unreadable) > 5 else "")
        warnings.append(f"enlaces sin texto legible en el cuerpo (Obsidian mostrará los guiones bajos): {shown}; "
                        f"escribe [[{unreadable[0]}|texto]]")

    # Secretos: la nota de lore nunca enlaza a 80_Secretos
    if note_type != "secreto":
        for target in {t.strip().lower() for t, _, _ in links}:
            resolved = md_by_stem.get(target.split("/")[-1])
            if resolved and resolved.startswith(SECRETS_DIR):
                errors.append(f"la nota enlaza a un secreto ({resolved}); los secretos enlazan a la nota, no al revés")
    return errors, warnings, note_type


def print_depth(spec, vault=None):
    """Imprime la profundidad de una nota de un tipo, una relevancia y, si se da, una categoría;
    devuelve el código de salida."""
    tipo, _, rest = spec.partition(":")
    raw, _, category = rest.partition(":")
    modules = load_modules()
    module, relevance = modules.get(tipo), int_value(raw)
    if not module:
        print(f"Error: el tipo `{tipo}` no tiene módulo (hay: {', '.join(sorted(modules))}).")
        return 1
    if relevance is None or not 1 <= relevance <= 5:
        print(f"Error: la relevancia debe ser un número del 1 al 5 (encontrado: {raw or 'vacío'}).")
        return 1
    _, template_body = split_note((SKILL_DIR / "tipos" / tipo / "plantilla.md").read_text(encoding="utf-8"))
    props = {"categoria": [category]} if category else None
    omitted = [t for t in omitted_sections(module, template_body, relevance, props or {})
               if t != "Mapa" or category]
    depth = module.get("profundidad", {})
    low, high = own_gaps_range(module, relevance)
    print(f"{tipo} con relevancia {relevance}:")
    if vault is not None and vault.is_dir() and world_state(vault) == WORLD_CLOSING:
        print(f"  Enlaces pendientes nuevos: ninguno ({CLOSING_NOTE}: lo menor, sin nombre propio).")
    else:
        print(f"  Enlaces pendientes nuevos: entre {low} y {high}.")
    optional = [t for t in omitted if depth.get(t) == 0]
    left_out = [t for t in omitted if t not in optional]
    if left_out:
        print("  Omite (no las escribas): " + ", ".join(
            f"«{t}»" + (f" (desde {depth[t]})" if t in depth else "") for t in left_out) + ".")
    if optional:
        print("  Opcionales (solo si hay algo real que contar): " + ", ".join(f"«{t}»" for t in optional) + ".")
    if not omitted:
        print("  Lleva todas las secciones de la plantilla.")
    if module.get("mapa"):
        if category:
            rule = map_applies(module, props, relevance)
            if rule:
                minimum = rule.get("zonas_minimas", 1)
                print(f"  Mapa: lleva la sección Mapa con su leyenda (mapa {rule['clase']}"
                      + (f"; la imagen, desde {minimum} zonas" if minimum > 1 else "") + ").")
            elif map_rule(module, props):
                print(f"  Mapa: con la categoría {category}, desde relevancia {map_rule(module, props)['desde']}.")
            else:
                print(f"  Mapa: la categoría {category} no lleva mapa.")
        else:
            print("  Mapa: depende de la categoría: " + "; ".join(
                f"{', '.join(rule.get('categoria', ['todas']))} desde {rule['desde']}" for rule in module["mapa"])
                + f". Indícala: --depth {tipo}:{relevance}:<categoría>.")
    print("  En las que lleva, escribe solo lo que aporta: un dato que no sabes no se inventa para llenar.")
    return 0


def checker(vault):
    """Prepara una vez lo que hace falta para validar notas de la bóveda y devuelve la función que valida una:
    nota → (errores, avisos, tipo). La usan este script y finalizar-mundo, que valida el mundo entero."""
    modules = load_modules()
    names, paths = index_vault(vault)
    world = read_world(vault)
    world_year = world["ano_actual"]
    calendars = load_calendars(vault)
    calendar = reference_calendar(calendars)
    gaps, _ = find_gaps(vault)
    # Lo que el detector de nombres sin enlace deja pasar: los términos del Glosario que no son el
    # nombre de una entidad (existente, pendiente o registrada como tal), los meses y el nombre del mundo
    terms, glossary_entities = glossary_terms(vault, known_types(modules))
    entity_names = entity_labels(load_index(vault), gaps) | {normalize(term) for term, _ in glossary_entities.values()}
    known_terms = (terms - entity_names) | calendar_terms(calendars)
    if world["props"].get("mundo"):
        known_terms.add(normalize(world["props"]["mundo"]))
    md_by_stem = {p.stem.lower(): p.relative_to(vault).as_posix().lower()
                  for p in vault.rglob("*.md") if not HIDDEN_DIRS & set(p.relative_to(vault).parts)}

    def run(path):
        return check(path, vault, modules, names, paths, md_by_stem, world_year, calendar, gaps, known_terms,
                     glossary_entities, calendars)
    return run


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("notes", nargs="*", help="Ruta o nombre de cada nota a validar")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--depth", metavar="TIPO:RELEVANCIA",
                        help="Dice qué secciones lleva una nota de ese tipo y relevancia, y cuántos enlaces "
                             "pendientes nuevos puede abrir (personaje:2)")
    args = parser.parse_args()
    if args.depth:
        sys.exit(print_depth(args.depth, vault_path(args.vault)))
    if not args.notes:
        parser.error("indica las notas a validar, o --depth <tipo>:<relevancia>")

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    run = checker(vault)

    total_errors = 0
    for argument in args.notes:
        path = resolve_note(argument, vault)
        if not path:
            print(f"\nERROR: no encuentro la nota '{argument}' (o hay varias con ese nombre).")
            total_errors += 1
            continue
        try:
            shown = path.resolve().relative_to(vault.resolve()).as_posix()
        except ValueError:
            shown = str(path)
        # Las notas internas (MOC, Ficha, Preguntas Abiertas, Glosario, guías, registros) no son entidades
        frontmatter, _ = split_note(path.read_text(encoding="utf-8"))
        note_type = first(parse_frontmatter(frontmatter or [], []).get("tipo"))
        if is_system_note(shown, note_type) or (shown.startswith("00_Sistema/") and not note_type):
            print(f"\n{shown} ({note_type or 'sin tipo'})\n  Nota interna (no es una entidad): no se valida.")
            continue
        errors, warnings, note_type = run(path)
        print(f"\n{shown} ({note_type or 'sin tipo'})")
        for error in errors:
            print(f"  ERROR: {error}")
        for warning in warnings:
            print(f"  AVISO: {warning}")
        print("  Correcta." if not errors else f"  {len(errors)} errores.")
        total_errors += len(errors)
    sys.exit(1 if total_errors else 0)


if __name__ == "__main__":
    main()
