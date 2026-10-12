#!/usr/bin/env python3
"""Mueve a la bóveda la imagen recién descargada desde el navegador.

Uso en dos pasos:
  1. Antes de pulsar "descargar":  fetch_download.py mark      → imprime una marca de tiempo
  2. Después:                      fetch_download.py fetch --since <marca> --dest <carpeta> --name Retrato_X

Busca en la carpeta de descargas la imagen más reciente posterior a la marca, espera a que
termine de descargarse y la mueve con el nombre pedido. Nunca sobrescribe: si existe, usa _v2, _v3…"""
import argparse
import shutil
import sys
import time
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
PARTIAL_EXTENSIONS = {".crdownload", ".part", ".tmp"}


def newest_image(downloads, since):
    """La imagen más reciente posterior a la marca, o None (también si aún hay descargas a medias)."""
    recent = [f for f in downloads.iterdir() if f.is_file() and f.stat().st_mtime >= since]
    if any(f.suffix.lower() in PARTIAL_EXTENSIONS for f in recent):
        return None
    images = [f for f in recent if f.suffix.lower() in IMAGE_EXTENSIONS]
    return max(images, key=lambda f: f.stat().st_mtime, default=None)


def free_destination(folder, name, extension):
    """Primer nombre libre; cuenta como ocupado el mismo nombre con cualquier extensión."""
    taken = {f.stem.lower() for f in folder.iterdir() if f.is_file()}
    candidate, n = name, 2
    while candidate.lower() in taken:
        candidate, n = f"{name}_v{n}", n + 1
    return folder / f"{candidate}{extension}"


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
    args = parser.parse_args()

    if args.command == "mark":
        # Dos segundos de margen por si el reloj del archivo va algo atrasado
        print(f"{time.time() - 2:.0f}")
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
