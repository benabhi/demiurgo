#!/usr/bin/env python3
"""Mueve a la bóveda la imagen recién descargada desde el navegador, y deja la aceptada con su nombre.

Uso:
  1. Antes de pulsar "descargar":  fetch_download.py mark      → imprime una marca de tiempo
  2. Después:                      fetch_download.py fetch --since <marca> --dest <carpeta> --name Retrato_X
  3. Al aceptar una imagen:        fetch_download.py keep --dest <carpeta> --name Retrato_X --new Retrato_X_v2.jpg [--label ed1]

`fetch` busca en la carpeta de descargas la imagen más reciente posterior a la marca, espera a que termine
de descargarse y la mueve con el nombre pedido. Nunca sobrescribe: si existe, usa _v2, _v3…
`keep` deja la imagen aceptada con el nombre de siempre (Retrato_X.jpg), así la nota no cambia de enlace.
Lo demás se archiva en `02_Activos/Anteriores`, sin borrar nada:
  - la imagen que había (otra edición del mapa, la versión anterior del retrato), como <nombre>_<etiqueta>
    (--label: ed1 para la edición 1 de un mapa; sin --label, v1, v2… según las que ya hay archivadas);
  - los intentos de esta vez que no se aceptaron (<nombre>_v2…), como <nombre>_descartada."""
import argparse
import re
import shutil
import sys
import time
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
PARTIAL_EXTENSIONS = {".crdownload", ".part", ".tmp"}
ASSETS_FOLDER = "02_Activos"
ARCHIVE_FOLDER = "Anteriores"
RECENT_ATTEMPT_SECONDS = 6 * 3600
ARCHIVE_README = """# Imágenes anteriores

Las imágenes que se reemplazaron, para volver a ellas si la nueva no gusta. Las archiva `generar-imagen`; no se borran.
- `<nombre>_ed<n>`: una edición anterior de un mapa. La nota la enlaza en su sección Mapa («Ediciones anteriores»).
- `<nombre>_v<n>`: una versión anterior de la imagen de una entidad. La nota la enlaza en su sección Imagen («Versiones anteriores»).
- `<nombre>_descartada`: un intento que no pasó la comprobación (un número repetido en un mapa, un rasgo que faltaba). Nadie la enlaza.
- `<nombre>_archivada`: una imagen de una entidad que se archivó al revisar los borradores (`revisar-mundo`). La enlaza su nota archivada.

Para volver a una anterior, pídelo: «vuelve a la edición 1 del mapa de…».
"""


def newest_image(downloads, since):
    """La imagen más reciente posterior a la marca, o None (también si aún hay descargas a medias)."""
    recent = [f for f in downloads.iterdir() if f.is_file() and f.stat().st_mtime >= since]
    if any(f.suffix.lower() in PARTIAL_EXTENSIONS for f in recent):
        return None
    images = [f for f in recent if f.suffix.lower() in IMAGE_EXTENSIONS]
    return max(images, key=lambda f: f.stat().st_mtime, default=None)


def free_destination(folder, name, extension, separator="_v"):
    """Primer nombre libre; cuenta como ocupado el mismo nombre con cualquier extensión."""
    taken = {f.stem.lower() for f in folder.iterdir() if f.is_file()}
    candidate, n = name, 2
    while candidate.lower() in taken:
        candidate, n = f"{name}{separator}{n}", n + 1
    return folder / f"{candidate}{extension}"


def archive_folder(folder):
    """`02_Activos/Anteriores` de la bóveda (junto a la carpeta de la imagen si no está en 02_Activos), con
    su README. Devuelve (carpeta, si se acaba de crear)."""
    assets = next((p for p in [folder, *folder.parents] if p.name == ASSETS_FOLDER), folder)
    target = assets / ARCHIVE_FOLDER
    created = not target.is_dir()
    target.mkdir(parents=True, exist_ok=True)
    if not (target / "README.md").is_file():
        (target / "README.md").write_text(ARCHIVE_README, encoding="utf-8", newline="\n")
    return target, created


def keep(folder, name, accepted, label):
    """Deja `accepted` como la imagen vigente (<name>.<ext>) y archiva la que había y los intentos descartados.
    Devuelve las líneas del resumen."""
    accepted = folder / accepted
    if not accepted.is_file():
        sys.exit(f"Error: no existe la imagen aceptada '{accepted}'.")
    images = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS and f != accepted]
    previous = [f for f in images if f.stem.lower() == name.lower()]
    # Los intentos de esta vez: los _v2, _v3… recientes (uno viejo es de antes y no se toca)
    attempts = [f for f in images if re.fullmatch(re.escape(name) + r"_v\d+", f.stem, flags=re.I)
                and time.time() - f.stat().st_mtime < RECENT_ATTEMPT_SECONDS]
    lines = []
    if previous or attempts:
        archive, created = archive_folder(folder)
        if created:
            lines.append(f"Carpeta nueva: {archive.as_posix()} (regístrala en «Carpetas añadidas por skills» "
                         "de la Guía de Organización)")
        for old in previous:
            tag = label
            if not tag:
                done = [f for f in archive.iterdir() if re.fullmatch(re.escape(name) + r"_v\d+", f.stem, flags=re.I)]
                tag = f"v{len(done) + 1}"
            target = free_destination(archive, f"{name}_{tag}", old.suffix.lower(), separator="_")
            shutil.move(str(old), str(target))
            lines.append(f"Anterior archivada:\t{target.name}")
        for attempt in sorted(attempts):
            target = free_destination(archive, f"{name}_descartada", attempt.suffix.lower(), separator="_")
            shutil.move(str(attempt), str(target))
            lines.append(f"Descartada archivada:\t{target.name} (era {attempt.name})")
    final = folder / f"{name}{accepted.suffix.lower()}"
    if accepted != final:
        accepted.rename(final)
    return [f"Vigente:\t{final.name}"] + lines


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("mark", help="Imprime la marca de tiempo actual")
    fetch = commands.add_parser("fetch", help="Mueve la imagen descargada a la bóveda")
    fetch.add_argument("--since", type=float, required=True, help="Marca impresa por 'mark'")
    fetch.add_argument("--dest", required=True, help="Carpeta de destino dentro de la bóveda")
    fetch.add_argument("--name", required=True, help="Nombre sin extensión, p. ej. Retrato_Nombre")
    fetch.add_argument("--downloads", default=str(Path.home() / "Downloads"), help="Carpeta de descargas")
    fetch.add_argument("--timeout", type=int, default=60, help="Segundos máximos de espera")
    keeper = commands.add_parser("keep", help="Deja la imagen aceptada con su nombre y archiva las demás")
    keeper.add_argument("--dest", required=True, help="Carpeta de la imagen dentro de la bóveda")
    keeper.add_argument("--name", required=True, help="Nombre sin extensión, p. ej. Mapa_Nombre")
    keeper.add_argument("--new", required=True, help="Archivo de la imagen aceptada, en esa carpeta")
    keeper.add_argument("--label", help="Etiqueta de la imagen que había: ed1 para la edición 1 de un mapa "
                                        "(sin ella, v1, v2…)")
    args = parser.parse_args()

    if args.command == "mark":
        # Dos segundos de margen por si el reloj del archivo va algo atrasado
        print(f"{time.time() - 2:.0f}")
        return
    if args.command == "keep":
        folder = Path(args.dest)
        if not folder.is_dir():
            sys.exit(f"Error: no existe la carpeta '{folder}'.")
        for line in keep(folder, args.name, Path(args.new).name, args.label):
            print(line)
        return

    downloads = Path(args.downloads)
    deadline = time.time() + args.timeout
    image = None
    while time.time() < deadline and not (image := newest_image(downloads, args.since)):
        time.sleep(1)
    if not image:
        sys.exit(f"Error: no apareció ninguna imagen nueva en {downloads} en {args.timeout} s.")
    time.sleep(1)  # margen para que el navegador cierre el archivo

    folder = Path(args.dest)
    folder.mkdir(parents=True, exist_ok=True)
    final = free_destination(folder, args.name, image.suffix.lower())
    shutil.move(str(image), str(final))
    print(f"{final.name}\t{final.stat().st_size / 1024:.0f} KB\t(de {image.name})")


if __name__ == "__main__":
    main()
