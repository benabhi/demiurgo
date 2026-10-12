#!/usr/bin/env python3
"""Genera nombres con la fonética de un perfil (sílabas y patrones) y descarta los ya usados.

Los perfiles se buscan primero en la bóveda (00_Sistema/06_Generacion/Nombres/<Perfil>.md,
editables en Obsidian) y, si no hay ninguno con ese nombre, en assets/nombres/ de la skill.
El perfil de una cultura se llama Nombres_<Cultura>.md, para no chocar con la nota de la
cultura; se puede pedir como --profile <Cultura> o --profile Nombres_<Cultura>.
Un nombre se descarta si ya existe en el mundo (títulos, alias, archivos o Glosario) o si se
parece demasiado a uno existente.

Ejemplos:  generate_names.py --profile Generico --count 10
           generate_names.py --profile Costero --count 5 --surnames --seed 7
           generate_names.py --list"""
import argparse
import difflib
import random
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import SKILL_DIR, load_index, normalize  # noqa: E402

VAULT_PROFILES = "00_Sistema/06_Generacion/Nombres"
SKILL_PROFILES = SKILL_DIR / "assets" / "nombres"
GLOSSARY = "00_Sistema/04_Convenciones/Glosario.md"
SIMILARITY_LIMIT = 0.85
SECTIONS = {"inicios": "I", "medios": "M", "finales": "F", "patrones": "patterns",
            "patrones de apellido": "surname_patterns", "prohibido": "forbidden"}


def profile_dirs(vault):
    return [vault / VAULT_PROFILES, SKILL_PROFILES]


def find_profile(vault, name):
    """Perfil <name>.md, o Nombres_<name>.md (el de una cultura)."""
    wanted = {normalize(name), normalize(f"Nombres_{name}")}
    for folder in profile_dirs(vault):
        if folder.is_dir():
            for path in sorted(folder.glob("*.md")):
                if normalize(path.stem) in wanted:
                    return path
    return None


def parse_profile(path):
    """{I, M, F, patterns, surname_patterns, forbidden: [elementos]} a partir del Markdown."""
    profile = {key: [] for key in SECTIONS.values()}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            current = SECTIONS.get(normalize(heading.group(1)))
            continue
        if current and line.strip():
            profile[current] += [item.strip() for item in line.split(",") if item.strip()]
    if not (profile["I"] and profile["F"] and profile["patterns"]):
        sys.exit(f"Error: el perfil {path.name} necesita al menos Inicios, Finales y Patrones.")
    profile["surname_patterns"] = profile["surname_patterns"] or profile["patterns"]
    return profile


def build(profile, pattern, rng):
    parts = []
    for letter in pattern.upper():
        pool = profile.get(letter) or profile["M"] or profile["I"]
        parts.append(rng.choice(pool))
    word = "".join(parts)
    return word[:1].upper() + word[1:]


def acceptable(word, profile):
    lowered = word.lower()
    if not 3 <= len(lowered) <= 12:
        return False
    # Ni tres letras iguales ni tres vocales seguidas ("Caluea" suena poco natural)
    if re.search(r"(.)\1\1", lowered) or re.search(r"[aeiouy]{3}", lowered):
        return False
    return not any(bad.lower() in lowered for bad in profile["forbidden"])


def existing_names(vault):
    """Nombres ya usados en el mundo, normalizados."""
    used = set()
    for entry in load_index(vault, excluded=()):
        for name in [entry["titulo"], entry["name"]] + entry["aliases"]:
            used.add(normalize(name))
            used.update(normalize(part) for part in re.split(r"[\s_]+", name) if len(part) > 3)
    glossary = vault / GLOSSARY
    if glossary.is_file():
        for line in glossary.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0] and not cells[0].startswith("-") and cells[0] != "Término":
                used.add(normalize(cells[0]))
    return used


def too_similar(word, used):
    key = normalize(word)
    if key in used:
        return True
    candidates = [u for u in used if u[:1] == key[:1] and abs(len(u) - len(key)) <= 2]
    return any(difflib.SequenceMatcher(None, key, u).ratio() >= SIMILARITY_LIMIT for u in candidates)


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--profile", default="Generico", help="Perfil de nombres (por defecto Generico)")
    parser.add_argument("--count", type=int, default=10, help="Cuántos nombres generar")
    parser.add_argument("--surnames", action="store_true", help="Añade un apellido a cada nombre")
    parser.add_argument("--seed", type=int, help="Semilla para repetir el resultado")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--list", action="store_true", help="Lista los perfiles disponibles")
    args = parser.parse_args()

    vault = Path(args.vault)
    if args.list:
        for folder in profile_dirs(vault):
            origin = "bóveda" if folder != SKILL_PROFILES else "skill (por defecto)"
            for path in sorted(folder.glob("*.md")) if folder.is_dir() else []:
                print(f"- {path.stem}  ({origin})")
        return
    path = find_profile(vault, args.profile)
    if not path:
        sys.exit(f"Error: no existe el perfil '{args.profile}'. Usa --list para ver los disponibles.")
    profile = parse_profile(path)
    used = existing_names(vault) if vault.is_dir() else set()
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()

    names, attempts = [], 0
    while len(names) < args.count and attempts < args.count * 200:
        attempts += 1
        name = build(profile, rng.choice(profile["patterns"]), rng)
        if not acceptable(name, profile) or too_similar(name, used):
            continue
        if args.surnames:
            surname = build(profile, rng.choice(profile["surname_patterns"]), rng)
            if not acceptable(surname, profile) or too_similar(surname, used):
                continue
            name = f"{name} {surname}"
        used.add(normalize(name))
        names.append(name)
    print(f"Perfil: {path.stem}" + ("" if path.parent != SKILL_PROFILES else " (por defecto de la skill)"))
    for name in names:
        print(f"- {name}")
    if len(names) < args.count:
        print(f"AVISO: solo se generaron {len(names)} nombres nuevos; el perfil está muy usado o es muy pequeño.")


if __name__ == "__main__":
    main()
