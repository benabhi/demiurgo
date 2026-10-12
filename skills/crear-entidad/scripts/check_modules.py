#!/usr/bin/env python3
"""Revisa la coherencia de todos los módulos de crear-entidad (tipos/<tipo>/), sin mirar la bóveda.

Comprueba en cada módulo:
  - que existan tipo.md, plantilla.md y modulo.json, y que `tipo` coincida con su carpeta;
  - que la plantilla tenga todas las propiedades que nombra el módulo (relaciones, fechas,
    fecha_exacta, escalas, valores, solo_si, la propiedad de su carpeta y la de su regla de
    tiempo), que sus valores por defecto estén permitidos y que su título empiece por el emoji
    del tipo;
  - que las condiciones de `solo_si` usen valores permitidos;
  - que cada sección de `profundidad` exista en la plantilla, con una relevancia mínima del 2 al 5;
  - que cada regla de `mapa` tenga una clase conocida, categorías que el módulo admite y una relevancia
    mínima del 1 al 5, y que la plantilla tenga la sección Mapa y las propiedades `mapa`,
    `mapa_edicion` y `mapa_zonas`;
  - que las recíprocas sean relaciones del módulo y que la regla de tiempo use valores permitidos
    y una sección que exista.
Y entre módulos:
  - que cada relación con un tipo o una familia que ya tiene módulos la pueda completar alguno
    (si no, sus huecos no se completarían nunca: falta la propiedad en algún `completa`);
  - que la propiedad inversa de cada recíproca exista en la plantilla del otro lado;
  - que cada propiedad de un `completa` la use de verdad alguna relación.
Sale con código 1 si encuentra errores. Úsalo al crear o cambiar un módulo.

Ejemplo:  check_modules.py"""
import json
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import (MAP_CLASSES, MAP_SECTION, SKILL_DIR, candidate_modules, first,  # noqa: E402
                       parse_frontmatter, split_note, template_sections)


def template_of(tipo):
    """(propiedades {nombre: valor por defecto}, líneas del cuerpo) de la plantilla de un tipo."""
    frontmatter, body = split_note((SKILL_DIR / "tipos" / tipo / "plantilla.md").read_text(encoding="utf-8"))
    return {k: first(v) for k, v in parse_frontmatter(frontmatter or [], []).items()}, body


def states(rule, name):
    value = rule.get(name)
    return value if isinstance(value, list) else ([value] if value else [])


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    errors, warnings, modules, templates = [], [], {}, {}
    for folder in sorted(p for p in (SKILL_DIR / "tipos").iterdir() if p.is_dir()):
        missing = [f for f in ("tipo.md", "plantilla.md", "modulo.json") if not (folder / f).is_file()]
        if missing:
            errors.append(f"{folder.name}: faltan {', '.join(missing)}")
            continue
        try:
            module = json.loads((folder / "modulo.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"{folder.name}: modulo.json no es JSON válido ({error})")
            continue
        if module.get("tipo") != folder.name:
            errors.append(f"{folder.name}: `tipo` es «{module.get('tipo')}» y debe ser «{folder.name}»")
        modules[folder.name] = module
        templates[folder.name] = template_of(folder.name)

    families = {}
    for tipo, module in modules.items():
        families.setdefault(module.get("familia", tipo), []).append(tipo)

    for tipo, module in sorted(modules.items()):
        props, body = templates[tipo]
        where = f"{tipo}"
        for key in ("emoji", "huecos_propios", "carpeta", "relaciones"):
            if key not in module:
                errors.append(f"{where}: falta `{key}` en modulo.json")
        gaps = module.get("huecos_propios", {})
        if gaps and not 0 <= gaps.get("min", 0) <= gaps.get("max", 0):
            errors.append(f"{where}: `huecos_propios` debe tener 0 ≤ min ≤ max")
        # `profundidad`: secciones de la plantilla y la relevancia desde la que van (con 1 irían siempre)
        titles = {title for _, title in template_sections(body)}
        for title, minimum in module.get("profundidad", {}).items():
            if title not in titles:
                errors.append(f"{where}: `profundidad` nombra la sección «{title}», que no está en la plantilla")
            if not isinstance(minimum, int) or not 2 <= minimum <= 5:
                errors.append(f"{where}: `profundidad` de «{title}» debe ser un número del 2 al 5 (encontrado: {minimum})")
        # `mapa`: qué lugares llevan mapa (clase, categorías y relevancia mínima)
        rules = module.get("mapa", [])
        if rules:
            categories = set(module.get("valores", {}).get("categoria", [])) | set(
                module.get("carpeta", {}).get("valores", {}) if module.get("carpeta", {}).get("propiedad") == "categoria"
                else [])
            for rule in rules:
                if rule.get("clase") not in MAP_CLASSES:
                    errors.append(f"{where}: `mapa` con una clase desconocida «{rule.get('clase')}» "
                                  f"(una de: {', '.join(MAP_CLASSES)})")
                if not isinstance(rule.get("desde"), int) or not 1 <= rule["desde"] <= 5:
                    errors.append(f"{where}: `mapa` necesita `desde`, una relevancia del 1 al 5")
                for category in rule.get("categoria", []):
                    if category not in categories:
                        errors.append(f"{where}: `mapa` nombra la categoría «{category}», que el módulo no admite")
                minimum = rule.get("zonas_minimas", 1)
                if not isinstance(minimum, int) or minimum < 1:
                    errors.append(f"{where}: `zonas_minimas` de `mapa` debe ser un número desde 1")
            if MAP_SECTION not in titles:
                errors.append(f"{where}: tiene `mapa` pero a la plantilla le falta la sección «{MAP_SECTION}»")
            for key in ("mapa", "mapa_edicion", "mapa_zonas"):
                if key not in props:
                    errors.append(f"{where}: tiene `mapa` pero a la plantilla le falta la propiedad `{key}`")
        heading = next((line for line in body if line.startswith("# ")), "")
        if module.get("emoji") and not heading.startswith(f"# {module['emoji']} "):
            errors.append(f"{where}: el título de la plantilla debe empezar por `# {module['emoji']} `")

        named = {"relaciones": list(module.get("relaciones", {})), "fechas": module.get("fechas", []),
                 "escalas": list(module.get("escalas", {})), "valores": list(module.get("valores", {}))}
        if module.get("fecha_exacta"):
            named["fecha_exacta"] = ["fecha_exacta"]
            if module["fecha_exacta"] not in module.get("fechas", []):
                errors.append(f"{where}: `fecha_exacta` precisa «{module['fecha_exacta']}», que no está en `fechas`")
        rule = module.get("carpeta", {})
        if "propiedad" in rule:
            named["carpeta"] = [rule["propiedad"]]
        time_rule = module.get("tiempo")
        if time_rule:
            named["tiempo"] = [time_rule.get("propiedad", "situacion")]
        # `solo_si`: cada propiedad y la que la condiciona están en la plantilla, y la condición usa
        # valores permitidos de esa otra propiedad
        for key, condition in module.get("solo_si", {}).items():
            for other, values in condition.items():
                named.setdefault("solo_si", []).extend([key, other])
                allowed = module.get("valores", {}).get(other)
                if allowed is None and rule.get("propiedad") == other:
                    allowed = list(rule.get("valores", {}))
                for value in values:
                    if allowed is not None and value not in allowed:
                        errors.append(f"{where}: `solo_si` de `{key}` usa «{value}», que no es un valor de `{other}`")
        for source, keys in named.items():
            for key in keys:
                if key not in props:
                    errors.append(f"{where}: `{key}` ({source}) no está en la plantilla")

        for key, allowed in module.get("valores", {}).items():
            default = props.get(key, "")
            if default and default not in allowed:
                errors.append(f"{where}: la plantilla pone `{key}: {default}`, que no está entre sus valores")
        if "propiedad" in rule:
            default = props.get(rule["propiedad"], "")
            if default and default not in rule.get("valores", {}):
                errors.append(f"{where}: la plantilla pone `{rule['propiedad']}: {default}`, que no tiene carpeta")
        if time_rule:
            allowed = module.get("valores", {}).get(time_rule.get("propiedad", "situacion"))
            for name in ("presente", "pasado", "futuro"):
                for value in states(time_rule, name):
                    if allowed and value not in allowed:
                        errors.append(f"{where}: `tiempo.{name}` usa «{value}», que no está entre los valores de situación")
            section = time_rule.get("cronologia")
            if section and f"## {section}" not in {line.strip() for line in body}:
                errors.append(f"{where}: `tiempo.cronologia` nombra la sección «{section}», que no está en la plantilla")

        relations = module.get("relaciones", {})
        for key, inverse in module.get("reciprocas", {}).items():
            if key not in relations:
                errors.append(f"{where}: la recíproca `{key}` no es una de sus relaciones")
                continue
            expected = relations[key]
            targets = families.get(expected) or ([expected] if expected in modules else [])
            if targets and not any(inverse in templates[t][0] for t in targets):
                errors.append(f"{where}: `{key}` es recíproca con `{inverse}`, pero ninguna plantilla de "
                              f"{', '.join(targets)} tiene esa propiedad")
        for key, expected in relations.items():
            exists = expected in families or expected in modules
            if exists and not candidate_modules(expected, modules, [key]):
                warnings.append(f"{where}: ningún módulo de `{expected}` completa `{key}` (añádela al `completa` "
                                f"de los que encajen; si espera un módulo futuro, ignora este aviso)")

    used = {key for module in modules.values() for key in module.get("relaciones", {})}
    for tipo, module in sorted(modules.items()):
        for key in module.get("completa", []):
            if key not in used:
                warnings.append(f"{tipo}: `completa` nombra `{key}`, que no es una relación de ningún módulo")

    print(f"Módulos: {len(modules)} | Errores: {len(errors)} | Avisos: {len(warnings)}")
    for error in errors:
        print(f"  ERROR: {error}")
    for warning in warnings:
        print(f"  AVISO: {warning}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
