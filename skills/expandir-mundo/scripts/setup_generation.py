#!/usr/bin/env python3
"""Prepara la carpeta del motor de generación en la bóveda (primer uso de expandir-mundo).

Copia desde assets/ lo que falte en 00_Sistema/06_Generacion (README, Tablas/, Paquetes.md y
Registro_de_Generacion.md) y crea Nombres/. Nunca sobrescribe: las tablas que el usuario ya
editó se conservan. Registra la carpeta en la tabla "Carpetas añadidas por skills" de la Guía
de Organización y enlaza el registro desde MOC_Inicio, si aún no lo están.

Ejemplo:  setup_generation.py --vault World_Building"""
import argparse
import shutil
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py, en los scripts de crear-entidad
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "crear-entidad" / "scripts"))
from vault_lib import vault_path  # noqa: E402

ASSETS = Path(__file__).resolve().parent.parent / "assets"
GENERATION_DIR = "00_Sistema/06_Generacion"
GUIDE = "00_Sistema/04_Convenciones/Guia_de_Organizacion.md"
HOME_MOC = "00_Sistema/MOC_Inicio.md"
FOLDER_ROW = ("| `00_Sistema/06_Generacion` | Motor de generación: tablas, perfiles de nombres, "
              "paquetes y registro | expandir-mundo |")
HOME_LINE = "- [[Registro_de_Generacion]] — qué creó el motor de generación en cada ciclo."


def register_folder(vault, created):
    """Añade la fila de la carpeta a la tabla 'Carpetas añadidas por skills' si falta."""
    guide = vault / GUIDE
    if not guide.is_file():
        return
    lines = guide.read_text(encoding="utf-8").splitlines()
    if any("00_Sistema/06_Generacion" in line for line in lines):
        return
    try:
        header = next(i for i, line in enumerate(lines) if line.strip().startswith("| Carpeta | Contenido | skill |"))
    except StopIteration:
        print(f"AVISO: la Guía de Organización no tiene la tabla 'Carpetas añadidas por skills'; "
              f"registra a mano: {FOLDER_ROW}")
        return
    position = header + 2  # tras la cabecera y el separador
    while position < len(lines) and lines[position].strip().startswith("|"):
        position += 1
    lines.insert(position, FOLDER_ROW)
    guide.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    created.append(f"{GUIDE} (fila de la carpeta)")


def link_from_home(vault, created):
    """Enlaza el registro desde MOC_Inicio, debajo de Preguntas_Abiertas, si falta."""
    home = vault / HOME_MOC
    if not home.is_file():
        return
    lines = home.read_text(encoding="utf-8").splitlines()
    if any("[[Registro_de_Generacion]]" in line for line in lines):
        return
    anchor = next((i for i, line in enumerate(lines) if "[[Preguntas_Abiertas]]" in line), None)
    if anchor is None:
        print(f"AVISO: no encuentro dónde enlazar el registro en MOC_Inicio; añádelo a mano: {HOME_LINE}")
        return
    lines.insert(anchor + 1, HOME_LINE)
    home.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    created.append(f"{HOME_MOC} (enlace al registro)")


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    target = vault / GENERATION_DIR
    created = []
    for source in sorted(ASSETS.rglob("*.md")):
        destination = target / source.relative_to(ASSETS)
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            created.append(destination.relative_to(vault).as_posix())
    names_dir = target / "Nombres"
    if not names_dir.exists():
        names_dir.mkdir(parents=True)
        created.append(names_dir.relative_to(vault).as_posix() + "/")
    register_folder(vault, created)
    link_from_home(vault, created)

    if created:
        print("Preparado:")
        for item in created:
            print(f"  + {item}")
    else:
        print("La carpeta de generación ya estaba preparada.")


if __name__ == "__main__":
    main()
