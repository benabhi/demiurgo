#!/usr/bin/env python3
"""Audita la coherencia del mundo entero: lo que check_note.py no ve revisando nota a nota.

Comprueba:
  - reciprocidad de relaciones (si A tiene a B como padre, B debe tener a A como hijo),
    según las `reciprocas` de cada modulo.json;
  - fechas y edades: padres mayores que sus hijos y con la madurez de su especie (12 años si
    no tiene ficha), hijos nacidos después de la muerte de sus padres, edades que no cuadran
    con el año actual y edades imposibles para la longevidad de su especie. Sin calendario,
    compara las edades;
  - personajes cuyo pueblo es de otra especie (un aviso: puede ser a propósito);
  - un solo calendario de referencia, y un año actual en la Ficha si lo hay;
  - eras: los periodos dentro de su era madre, la siguiente después de la anterior, una sola era
    actual mundial y cada entidad dentro de la era que enlaza (avisos, salvo el primero);
  - facciones: ninguna aliada y rival de otra a la vez, ni viva con un líder muerto (avisos);
  - linajes: ninguno aliado y rival de otro a la vez, ni vivo con la cabeza o el heredero muertos,
    ni extinto con miembros vivos (avisos);
  - objetos: ninguno en uso con su poseedor muerto (aviso);
  - creencias: ninguna extinta con fieles vivos (aviso);
  - afecciones: ninguna erradicada que sufra alguien vivo (aviso);
  - deidades: ninguna olvidada a la que venere una fe viva (aviso);
  - sistemas: ninguno perdido que practique alguien vivo (aviso);
  - mitos: ninguna profecía pendiente con el plazo ya pasado (aviso);
  - eventos: cada batalla dentro de su guerra (error), cada causa antes que su consecuencia,
    los participantes vivos en esas fechas y los eventos que abren o cierran una era en sus
    fechas (avisos);
  - nombres casi iguales entre entidades distintas;
  - enlaces mal formados;
  - enlaces pendientes: notas vacías (las crea un clic en un enlace pendiente en Obsidian y lo
    anulan), enlaces pendientes sin tipo y el registro Enlaces_Pendientes (que exista, que esté
    al día y que sus tipos existan) (avisos);
  - entidades que el Glosario registra como tales (por su Tipo) y que ninguna nota enlaza, y nombres
    que registra a la vez como entidad y como término (avisos);
  - entidades huérfanas (ninguna otra las enlaza);
  - borradores pendientes de revisión.
Sale con código 1 si hay errores (los avisos no cuentan).

Ejemplos:  audit_world.py     audit_world.py --json     audit_world.py --focus Aldric_Voss Forja_del_Puerto"""
import argparse
import difflib
import json
import sys
from collections import defaultdict
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (DEFAULT_EXCLUDED, bare_name, date_keys, find_gaps, first, glossary_rows,  # noqa: E402
                       glossary_terms, int_value, is_entity_kind, is_hidden, known_types, load_calendars,
                       load_index, load_modules, normalize, note_link_labels, read_registry, read_world)

MIN_PARENT_AGE = 12
LONGEVITY_MARGIN = 1.25
SIMILARITY_LIMIT = 0.9


def check_reciprocity(index, by_name, modules, report):
    for entry in index:
        reciprocal = modules.get(entry["tipo"], {}).get("reciprocas", {})
        for prop, inverse in reciprocal.items():
            for target in entry["relaciones"].get(prop, []):
                other = by_name.get(target.lower())
                if not other:
                    continue  # es un enlace pendiente: se completará más adelante
                if inverse not in modules.get(other["tipo"], {}).get("relaciones", {}):
                    continue  # su tipo no tiene la propiedad inversa (un asentamiento no lista criaturas)
                listed = [t.lower() for t in other["relaciones"].get(inverse, [])]
                if entry["name"].lower() not in listed:
                    report["errores"].append(
                        f"[[{entry['name']}]] tiene a [[{other['name']}]] en `{prop}`, "
                        f"pero [[{other['name']}]] no tiene a [[{entry['name']}]] en `{inverse}`")


def species_number(entry, by_name, key):
    """Número de la ficha de la especie de una entidad (`longevidad`, `madurez`), o None."""
    targets = entry["relaciones"].get("especie", [])
    species = by_name.get(targets[0].lower()) if targets else None
    return int_value(first(species["props"].get(key))) if species else None


def check_dates(index, by_name, world_year, report):
    for entry in index:
        birth = int_value(first(entry["props"].get("nacimiento")))
        age = int_value(first(entry["props"].get("edad")))
        alive = first(entry["props"].get("situacion_vital")) in ("", "vivo")
        if world_year is not None and birth is not None and age is not None and alive                 and abs((world_year - birth) - age) > 1:
            report["errores"].append(f"[[{entry['name']}]]: edad {age} no cuadra con nacimiento {birth} "
                                     f"(año actual {world_year})")
        longevity = species_number(entry, by_name, "longevidad")
        if age is not None and longevity and alive and age > longevity * LONGEVITY_MARGIN:
            species = entry["relaciones"]["especie"][0]
            report["avisos"].append(f"[[{entry['name']}]] tiene {age} años y su especie, [[{species}]], "
                                    f"vive unos {longevity}")
        for parent_name in entry["relaciones"].get("padres", []):
            parent = by_name.get(parent_name.lower())
            if not parent:
                continue
            maturity = species_number(parent, by_name, "madurez") or MIN_PARENT_AGE
            parent_birth = int_value(first(parent["props"].get("nacimiento")))
            parent_death = int_value(first(parent["props"].get("muerte")))
            parent_age = int_value(first(parent["props"].get("edad")))
            parent_alive = first(parent["props"].get("situacion_vital")) in ("", "vivo")
            if birth is not None and parent_birth is not None:
                gap = birth - parent_birth
            elif age is not None and parent_age is not None and alive and parent_alive:
                gap = parent_age - age  # sin calendario: la diferencia de edades
            else:
                gap = None
            if gap is not None and gap <= 0:
                report["errores"].append(f"[[{parent['name']}]] no es mayor que su hijo [[{entry['name']}]]")
            elif gap is not None and gap < maturity:
                report["avisos"].append(f"[[{parent['name']}]] tenía {gap} años cuando nació [[{entry['name']}]] "
                                        f"(madurez: {maturity})")
            if birth is not None and parent_death is not None and birth > parent_death + 1:
                report["avisos"].append(f"[[{entry['name']}]] nació ({birth}) más de un año después de "
                                        f"la muerte de [[{parent['name']}]] ({parent_death})")


def check_peoples(index, by_name, report):
    """Personajes cuyo pueblo (cultura) es de otra especie: puede ser a propósito, así que es un aviso."""
    for entry in index:
        people = entry["relaciones"].get("pueblo", [])
        species = entry["relaciones"].get("especie", [])
        culture = by_name.get(people[0].lower()) if people else None
        if not culture or not species:
            continue
        culture_species = culture["relaciones"].get("especie", [])
        if culture_species and culture_species[0].lower() != species[0].lower():
            report["avisos"].append(f"[[{entry['name']}]] es de la especie [[{species[0]}]], pero su pueblo, "
                                    f"[[{culture['name']}]], es de [[{culture_species[0]}]]")


def check_calendars(vault, world_year, report):
    """El calendario de referencia es el eje de la Ficha: uno solo, y con el año actual en la Ficha."""
    calendars = load_calendars(vault)
    references = [c for c in calendars if c["referencia"]]
    if len(references) > 1:
        names = ", ".join(f"[[{c['nombre']}]]" for c in references)
        report["errores"].append(f"hay {len(references)} calendarios de referencia ({names}): solo uno puede serlo")
    elif calendars and not references:
        report["avisos"].append("hay calendarios, pero ninguno es el de referencia (`referencia: true`)")
    if references and world_year is None:
        report["avisos"].append(f"existe el calendario de referencia, [[{references[0]['nombre']}]], "
                                f"pero la Ficha no tiene año actual")


def span(entry, start_key="inicio", end_key="fin"):
    """(inicio, fin) numéricos de una entidad, o None donde falten."""
    return (int_value(first(entry["props"].get(start_key))), int_value(first(entry["props"].get(end_key))))


def years(start, end):
    """Un intervalo de años legible: «-120 a 0», «0 a hoy», o un solo año."""
    if start is not None and start == end:
        return str(start)
    return f"{start if start is not None else '?'} a {end if end is not None else 'hoy'}"


def period(entry):
    """(inicio, fin) de una era o un evento; un evento de un solo año que no sigue en curso termina
    el mismo año en que empieza."""
    start, end = span(entry)
    if end is None and entry["tipo"] == "evento" and first(entry["props"].get("situacion")) != "en_curso":
        end = start
    return start, end


def check_containment(index, by_name, prop, label, report):
    """Cada entidad cabe en las fechas de la que la contiene (`era_padre`, `evento_padre`)."""
    for entry in index:
        start, end = period(entry)
        for parent in (by_name.get(n.lower()) for n in entry["relaciones"].get(prop, [])):
            if not parent:
                continue
            parent_start, parent_end = period(parent)
            if (start is not None and parent_start is not None and start < parent_start) or \
                    (end is not None and parent_end is not None and end > parent_end):
                report["errores"].append(f"[[{entry['name']}]] ({years(start, end)}) se sale {label}, "
                                         f"[[{parent['name']}]] ({years(parent_start, parent_end)})")


def check_eras(index, by_name, modules, report):
    """Los periodos caben en su era madre, la era siguiente no empieza antes de que termine la
    anterior, solo hay una era actual mundial y cada entidad cae dentro de la era que enlaza."""
    check_containment(index, by_name, "era_padre", "de su era madre", report)
    eras = [e for e in index if e["tipo"] == "era"]
    for era in eras:
        start, end = span(era)
        for following in (by_name.get(n.lower()) for n in era["relaciones"].get("siguiente", [])):
            following_start = span(following)[0] if following else None
            if end is not None and following_start is not None and following_start < end:
                report["avisos"].append(f"[[{following['name']}]] empieza ({following_start}) antes de que termine "
                                        f"[[{era['name']}]] ({end})")
    current = [e for e in eras if first(e["props"].get("situacion")) == "actual"
               and first(e["props"].get("alcance")) == "mundial" and not e["relaciones"].get("era_padre")]
    if len(current) > 1:
        names = ", ".join(f"[[{e['name']}]]" for e in current)
        report["avisos"].append(f"hay {len(current)} eras actuales de alcance mundial ({names}): "
                                f"si una contiene a la otra, enlázalas con `era_padre`")
    for entry in index:
        if entry["tipo"] == "evento":
            entry_start, entry_end = period(entry)
        else:
            entry_start, entry_end = span(entry, *date_keys(modules.get(entry["tipo"], {})))
        for era in (by_name.get(n.lower()) for n in entry["relaciones"].get("era", [])):
            if not era or era["tipo"] != "era":
                continue
            era_start, era_end = span(era)
            if entry_start is not None and era_end is not None and entry_start > era_end:
                report["avisos"].append(f"[[{entry['name']}]] empieza ({entry_start}) después de que termine "
                                        f"su era, [[{era['name']}]] ({era_end})")
            elif entry_end is not None and era_start is not None and entry_end < era_start:
                report["avisos"].append(f"[[{entry['name']}]] termina ({entry_end}) antes de que empiece "
                                        f"su era, [[{era['name']}]] ({era_start})")


def check_events(index, by_name, report):
    """Cada batalla cabe en su guerra, cada causa empieza antes que su consecuencia, los
    participantes vivían entonces y los eventos que abren o cierran una era coinciden con ella."""
    check_containment(index, by_name, "evento_padre", "del evento al que pertenece", report)
    for event in (e for e in index if e["tipo"] == "evento"):
        start, end = period(event)
        for effect in (by_name.get(n.lower()) for n in event["relaciones"].get("consecuencias", [])):
            effect_start = period(effect)[0] if effect else None
            if start is not None and effect_start is not None and effect_start < start:
                report["avisos"].append(f"[[{effect['name']}]] ({effect_start}) es consecuencia de "
                                        f"[[{event['name']}]], que empieza después ({start})")
        if start is None:
            continue
        for person in (by_name.get(n.lower()) for n in event["relaciones"].get("participantes", [])):
            if not person:
                continue
            birth, death = span(person, "nacimiento", "muerte")
            if birth is not None and birth > (end if end is not None else start):
                report["avisos"].append(f"[[{person['name']}]] participó en [[{event['name']}]] "
                                        f"({years(start, end)}), pero nació después ({birth})")
            elif death is not None and death < start:
                report["avisos"].append(f"[[{person['name']}]] participó en [[{event['name']}]] "
                                        f"({years(start, end)}), pero había muerto antes ({death})")
    for era in (e for e in index if e["tipo"] == "era"):
        era_start, era_end = span(era)
        for key, year, verb in (("evento_inicio", era_start, "empieza"), ("evento_fin", era_end, "termina")):
            if year is None:
                continue
            for event in (by_name.get(n.lower()) for n in era["relaciones"].get(key, [])):
                if not event or event["tipo"] != "evento":
                    continue
                event_start, event_end = period(event)
                moments = {v for v in (event_start, event_end) if v is not None}
                if moments and year not in moments:
                    report["avisos"].append(f"[[{era['name']}]] {verb} en {year}, pero [[{event['name']}]], "
                                            f"que la {'abre' if key == 'evento_inicio' else 'cierra'}, "
                                            f"ocurre en {years(event_start, event_end)}")


def check_factions(index, by_name, report):
    """Una facción no es aliada y rival de otra a la vez, y una facción viva no tiene un líder muerto."""
    for faction in (e for e in index if e["tipo"] == "faccion"):
        both = {n.lower() for n in faction["relaciones"].get("aliados", [])} & \
            {n.lower() for n in faction["relaciones"].get("rivales", [])}
        for name in sorted(both):
            report["avisos"].append(f"[[{faction['name']}]] tiene a [[{by_name[name]['name'] if name in by_name else name}]] "
                                    f"como aliada y como rival a la vez")
        alive = first(faction["props"].get("situacion")) != "disuelta"
        for leader in (by_name.get(n.lower()) for n in faction["relaciones"].get("lider", [])):
            if alive and leader and first(leader["props"].get("situacion_vital")) == "muerto":
                report["avisos"].append(f"[[{faction['name']}]] sigue en pie, pero su líder, [[{leader['name']}]], "
                                        f"está muerto: busca quién lo sucedió")


def check_lineages(index, by_name, report):
    """Un linaje no es aliado y rival de otro a la vez; uno vivo no tiene la cabeza ni el heredero
    muertos, y uno extinto no tiene miembros vivos."""
    for house in (e for e in index if e["tipo"] == "linaje"):
        both = {n.lower() for n in house["relaciones"].get("aliados", [])} & \
            {n.lower() for n in house["relaciones"].get("rivales", [])}
        for name in sorted(both):
            report["avisos"].append(f"[[{house['name']}]] tiene a [[{by_name[name]['name'] if name in by_name else name}]] "
                                    f"como aliada y como rival a la vez")
        extinct = first(house["props"].get("situacion")) == "extinta"
        for prop, role in (("cabeza", "su cabeza"), ("heredero", "su heredero")):
            for person in (by_name.get(n.lower()) for n in house["relaciones"].get(prop, [])):
                if not extinct and person and first(person["props"].get("situacion_vital")) == "muerto":
                    report["avisos"].append(f"[[{house['name']}]] sigue viva, pero {role}, [[{person['name']}]], "
                                            f"está muerto: busca quién lo sucedió")
        if extinct:
            for prop in ("cabeza", "heredero", "miembros"):
                for person in (by_name.get(n.lower()) for n in house["relaciones"].get(prop, [])):
                    if person and first(person["props"].get("situacion_vital")) in ("", "vivo"):
                        report["avisos"].append(f"[[{house['name']}]] está extinta, pero [[{person['name']}]] sigue "
                                                f"vivo: ¿es un heredero oculto, o la casa no se extinguió?")


def check_objects(index, by_name, report):
    """Un objeto que sigue en uso no tiene un poseedor muerto."""
    for item in (e for e in index if e["tipo"] == "objeto"):
        if first(item["props"].get("situacion")) != "en_uso":
            continue
        for owner in (by_name.get(n.lower()) for n in item["relaciones"].get("poseedor", [])):
            if owner and first(owner["props"].get("situacion_vital")) == "muerto":
                report["avisos"].append(f"[[{item['name']}]] sigue en uso, pero su poseedor, [[{owner['name']}]], "
                                        f"está muerto: ¿quién lo tiene ahora?")


def check_beliefs(index, by_name, report):
    """Una creencia extinta no tiene fieles vivos: si alguien la practica, está oculta o perseguida."""
    for person in (e for e in index if e["tipo"] == "personaje"):
        if first(person["props"].get("situacion_vital")) not in ("", "vivo"):
            continue
        for belief in (by_name.get(n.lower()) for n in person["relaciones"].get("creencias", [])):
            if belief and belief["tipo"] == "creencia" and first(belief["props"].get("situacion")) == "extinta":
                report["avisos"].append(f"[[{belief['name']}]] está extinta, pero [[{person['name']}]] la "
                                        f"practica: ¿está `oculta` o `perseguida`?")


def check_afflictions(index, by_name, report):
    """Una afección erradicada no la sufre nadie vivo: si alguien la tiene, volvió (o no se erradicó)."""
    for person in (e for e in index if e["tipo"] == "personaje"):
        if first(person["props"].get("situacion_vital")) not in ("", "vivo"):
            continue
        for affliction in (by_name.get(n.lower()) for n in person["relaciones"].get("afecciones", [])):
            if affliction and affliction["tipo"] == "afeccion" \
                    and first(affliction["props"].get("prevalencia")) == "erradicada":
                report["avisos"].append(f"[[{affliction['name']}]] está erradicada, pero [[{person['name']}]] la "
                                        f"sufre: ¿volvió (`esporadica`, `epidemica`) o nunca desapareció (`latente`)?")


def check_deities(index, by_name, report):
    """Una deidad olvidada no tiene una fe viva que la venere."""
    for deity in (e for e in index if e["tipo"] == "deidad"):
        if first(deity["props"].get("situacion")) != "olvidada":
            continue
        for belief in (by_name.get(n.lower()) for n in deity["relaciones"].get("creencias", [])):
            if belief and first(belief["props"].get("situacion")) not in ("", "extinta"):
                report["avisos"].append(f"[[{deity['name']}]] está olvidada, pero la venera [[{belief['name']}]], "
                                        f"que sigue viva: ¿está `distante` o `dormida`?")


def check_myths(index, world_year, report):
    """Una profecía pendiente no tiene su plazo en el pasado: o se cumplió, o no, o se discute."""
    if world_year is None:
        return
    for myth in (e for e in index if e["tipo"] == "mito"):
        deadline = int_value(first(myth["props"].get("plazo")))
        if first(myth["props"].get("cumplimiento")) == "pendiente" and deadline is not None and deadline < world_year:
            report["avisos"].append(f"[[{myth['name']}]] sigue pendiente, pero su plazo ({deadline}) ya pasó "
                                    f"(estamos en {world_year}): ¿se cumplió, no se cumplió o se discute?")


def check_systems(index, by_name, report):
    """Un sistema perdido no lo practica nadie vivo: si alguien lo usa, se recuperó o se guarda en secreto.
    Sus practicantes son los de su propiedad y los personajes que lo tienen en sus `sistemas`."""
    for system in (e for e in index if e["tipo"] == "sistema"):
        if first(system["props"].get("situacion")) != "perdido":
            continue
        key = system["name"].lower()
        users = {n.lower() for n in system["relaciones"].get("practicantes", [])}
        users |= {e["name"].lower() for e in index if e["tipo"] == "personaje"
                  and key in {n.lower() for n in e["relaciones"].get("sistemas", [])}}
        for person in sorted(filter(None, (by_name.get(n) for n in users)), key=lambda e: e["name"]):
            if person["tipo"] == "personaje" and first(person["props"].get("situacion_vital")) in ("", "vivo"):
                report["avisos"].append(f"[[{system['name']}]] está perdido, pero [[{person['name']}]] lo practica: "
                                        f"¿alguien lo recuperó (`en_declive`, `vigente`) o lo guarda en secreto?")


def check_names(index, report):
    names = []
    for entry in index:
        for name in {entry["titulo"], *entry["aliases"]}:
            if name:
                names.append((normalize(name), name, entry["name"]))
    buckets = defaultdict(list)
    for item in names:
        buckets[item[0][:1]].append(item)
    seen = set()
    for bucket in buckets.values():
        for i, (key_a, name_a, owner_a) in enumerate(bucket):
            for key_b, name_b, owner_b in bucket[i + 1:]:
                if owner_a == owner_b or abs(len(key_a) - len(key_b)) > 2:
                    continue
                pair = tuple(sorted((owner_a, owner_b)))
                if pair in seen:
                    continue
                if key_a == key_b or difflib.SequenceMatcher(None, key_a, key_b).ratio() >= SIMILARITY_LIMIT:
                    seen.add(pair)
                    report["avisos"].append(f"nombres casi iguales: «{name_a}» ([[{owner_a}]]) "
                                            f"y «{name_b}» ([[{owner_b}]])")


def check_orphans(index, report):
    linked = set()
    for entry in index:
        linked.update(link.lower() for link in entry["enlaces"] if link.lower() != entry["name"].lower())
    for entry in index:
        # Los secretos solo enlazan hacia fuera: nadie los enlaza a propósito
        if entry["tipo"] != "secreto" and entry["name"].lower() not in linked:
            report["avisos"].append(f"[[{entry['name']}]] es huérfana: ninguna otra entidad la enlaza")


def check_pending(vault, gaps, modules, report):
    """Enlaces pendientes: notas vacías que los anulan, los que no tienen tipo y el registro."""
    for path in sorted(vault.rglob("*.md")):
        relative = path.relative_to(vault).as_posix()
        if not is_hidden(relative) and not relative.startswith(DEFAULT_EXCLUDED) \
                and not path.read_text(encoding="utf-8").strip():
            report["avisos"].append(
                f"{relative} está vacía (¿un clic en un enlace pendiente en Obsidian?): mientras exista, "
                f"el enlace deja de contar como pendiente. Bórrala o escríbela")
    for gap in gaps:
        if not gap["expected_type"]:
            named = ", ".join(f"[[{Path(n).stem}]]" for n in sorted({o["note"] for o in gap["occurrences"]})[:3])
            report["avisos"].append(f"[[{gap['link']}]] es un enlace pendiente sin tipo (lo nombra {named}): "
                                    f"asígnaselo con `pending_links.py --set {gap['link']}=<tipo>`")
    registry = read_registry(vault)
    if registry is None:
        if gaps:
            report["avisos"].append("no hay registro de enlaces pendientes: créalo con `pending_links.py`")
        return
    valid = known_types(modules)
    shown = {g["link"].lower(): g["link"] for g in gaps}
    for link, tipo in sorted(registry.items()):
        if tipo and tipo not in valid:
            report["avisos"].append(f"el registro de enlaces pendientes da a `{shown.get(link, link)}` el tipo "
                                    f"«{tipo}», que no existe: usa uno de {', '.join(sorted(valid))}")
    missing, extra = set(shown) - set(registry), set(registry) - set(shown)
    if missing or extra:
        report["avisos"].append(f"el registro de enlaces pendientes está desactualizado (faltan {len(missing)}, "
                                f"sobran {len(extra)}): regenéralo con `pending_links.py`")


def check_glossary(vault, index, modules, report):
    """Entidades que el Glosario registra como tales (por su Tipo) y que ninguna nota enlaza: o les
    falta su enlace pendiente donde se nombran, o en realidad son términos con el Tipo equivocado.
    Y nombres que el Glosario registra a la vez como entidad y como término (un sistema que se llama
    como la fuerza que mueve): el detector pediría enlazar cada mención del término."""
    types = known_types(modules)
    _, entities = glossary_terms(vault, types)
    if not entities:
        return
    as_term = {bare_name(term): (term, kind) for names, kind in glossary_rows(vault)
               if not is_entity_kind(kind, types) for term in names if bare_name(term)}
    for name in sorted(set(entities) & set(as_term)):
        (entity, kind), (term, term_kind) = entities[name], as_term[name]
        report["avisos"].append(f"«{entity}» figura en el Glosario como entidad ({kind}) y «{term}» como término "
                                f"({term_kind}): un nombre no puede ser las dos cosas, porque cada mención del término "
                                f"pediría el enlace de la entidad; dale otro nombre a una de las dos")
    linked = {bare_name(label) for entry in index for label in [entry["titulo"], *entry["aliases"]] if label}
    for path in vault.rglob("*.md"):
        relative = path.relative_to(vault).as_posix()
        if not is_hidden(relative) and not relative.startswith(DEFAULT_EXCLUDED):
            linked |= note_link_labels(path.read_text(encoding="utf-8"))
    for name, (term, kind) in sorted(entities.items()):
        if name not in linked:
            report["avisos"].append(f"«{term}» figura en el Glosario como entidad ({kind}), pero ninguna nota la "
                                    f"enlaza: enlázala donde se nombra (como enlace pendiente, si no tiene nota) o, "
                                    f"si es un término, corrige su Tipo")


def run_audit(vault):
    """Auditoría completa: {errores, avisos, entidades, borradores, borradores_procedurales}."""
    index = load_index(vault)
    by_name = {e["name"].lower(): e for e in index}
    report = {"errores": [], "avisos": []}
    modules = load_modules()
    check_reciprocity(index, by_name, modules, report)
    world_year = read_world(vault)["ano_actual"]
    check_dates(index, by_name, world_year, report)
    check_peoples(index, by_name, report)
    check_calendars(vault, world_year, report)
    check_eras(index, by_name, modules, report)
    check_events(index, by_name, report)
    check_factions(index, by_name, report)
    check_lineages(index, by_name, report)
    check_objects(index, by_name, report)
    check_beliefs(index, by_name, report)
    check_afflictions(index, by_name, report)
    check_deities(index, by_name, report)
    check_systems(index, by_name, report)
    check_myths(index, world_year, report)
    check_names(index, report)
    gaps, malformed = find_gaps(vault)
    report["errores"] += [f"enlace mal formado en {m['note']}: {m['line']}" for m in malformed]
    check_pending(vault, gaps, modules, report)
    check_glossary(vault, index, modules, report)
    check_orphans(index, report)
    drafts = [e for e in index if e["estado"] == "borrador"]
    report["entidades"] = len(index)
    report["borradores"] = len(drafts)
    report["borradores_procedurales"] = sum(1 for e in drafts if e["origen"] == "procedural")
    return report


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    parser.add_argument("--focus", nargs="+", metavar="NOTA",
                        help="Solo los errores y avisos de estas notas (las que creaste o tocaste) y los del "
                             "mundo en general; del resto, el recuento")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    report = run_audit(vault)
    hidden = {"errores": 0, "avisos": 0}
    if args.focus:
        # Un mensaje sin enlaces es del mundo en general (el registro, las eras actuales): se muestra siempre
        wanted = {f"[[{Path(n).stem.strip('[]').lower()}]]" for n in args.focus}
        for kind in ("errores", "avisos"):
            kept = [m for m in report[kind] if "[[" not in m or any(w in m.lower() for w in wanted)]
            hidden[kind] = len(report[kind]) - len(kept)
            report[kind] = kept

    if args.json:
        print(json.dumps({**report, "ocultos": hidden} if args.focus else report, ensure_ascii=False, indent=2))
    else:
        print(f"Entidades: {report['entidades']} | Borradores: {report['borradores']} "
              f"(procedurales: {report['borradores_procedurales']})")
        print(f"Errores: {len(report['errores'])} | Avisos: {len(report['avisos'])}"
              + (" (de estas notas y del mundo en general)" if args.focus else ""))
        for error in report["errores"]:
            print(f"  ERROR: {error}")
        for warning in report["avisos"]:
            print(f"  AVISO: {warning}")
        if args.focus and (hidden["errores"] or hidden["avisos"]):
            print(f"En el resto del mundo: {hidden['errores']} errores y {hidden['avisos']} avisos "
                  f"(sin --focus se listan todos)")
    sys.exit(1 if report["errores"] else 0)


if __name__ == "__main__":
    main()
