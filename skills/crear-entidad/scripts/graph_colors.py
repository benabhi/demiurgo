#!/usr/bin/env python3
"""Configura el grafo de Obsidian de la bóveda (`.obsidian/graph.json`) para que se lea el mundo de un vistazo.

  - Un grupo de color por cada tipo de entidad (`tag:#<tipo>`), con el color de su módulo (`color` en su
    modulo.json; si no lo tiene, uno que sale de su nombre). Todas las plantillas llevan su tipo como
    etiqueta. Los grupos que el usuario haya creado a mano se conservan y van primero, así que mandan.
  - Un filtro que deja fuera 00_Sistema (los MOC, la Ficha, el Glosario, los registros, la Bitácora y las
    plantillas), los README de las carpetas y los MOC de las secciones: son índices que enlazan con todo y
    enredan el grafo. Si el usuario ya tiene un filtro propio, no se toca (con --filter, se reemplaza).
  - Los adjuntos (las imágenes) y las etiquetas no salen como nodos. Los enlaces pendientes sí: son los
    nodos grises, las entidades que el mundo ya nombra y aún no existen.
Lo demás (las fuerzas, el zoom, las flechas) se queda como esté. Es idempotente: se puede volver a ejecutar
cuando llegan tipos nuevos. Obsidian lee el archivo al abrir el grafo; si está abierto, recárgalo sin guardar
(paleta de comandos: «Reload app without saving») para verlo.

Ejemplos:  graph_colors.py   graph_colors.py --filter   graph_colors.py --list"""
import argparse
import colorsys
import hashlib
import json
import re
import sys
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import load_modules  # noqa: E402
from vault_lib import vault_path  # noqa: E402

GRAPH_FILE = ".obsidian/graph.json"
SYSTEM_FILTER = "-path:00_Sistema -file:README -file:MOC_"
TYPE_GROUP_RE = re.compile(r"^tag:#([\w-]+)$")
COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
# Lo que se muestra: ni los adjuntos ni las etiquetas como nodos; sí los enlaces pendientes y las notas sueltas
DISPLAY = {"showAttachments": False, "showTags": False, "hideUnresolved": False, "showOrphans": True}


def fallback_color(name):
    """Un color estable para un tipo sin `color` en su módulo, sacado de su nombre."""
    hue = int(hashlib.md5(name.encode("utf-8")).hexdigest()[:4], 16) / 0xFFFF
    red, green, blue = colorsys.hls_to_rgb(hue, 0.55, 0.6)
    return "#{:02X}{:02X}{:02X}".format(round(red * 255), round(green * 255), round(blue * 255))


def type_colors(modules=None):
    """[(tipo, color «#RRGGBB»)] de todos los módulos, en orden alfabético."""
    modules = modules if modules is not None else load_modules()
    pairs = []
    for tipo in sorted(modules):
        color = modules[tipo].get("color", "")
        pairs.append((tipo, color if COLOR_RE.match(color) else fallback_color(tipo)))
    return pairs


def configure_graph(vault, modules=None, replace_filter=False):
    """Escribe o completa `.obsidian/graph.json`. Devuelve las líneas del resumen."""
    path = vault / GRAPH_FILE
    try:
        settings = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except json.JSONDecodeError:
        return [f"AVISO: {GRAPH_FILE} no es JSON válido; no lo toco (arréglalo o bórralo y vuelve a ejecutar)."]
    colors = type_colors(modules)
    known = {tipo for tipo, _ in colors}
    groups = settings.get("colorGroups") or []
    # Los grupos propios del usuario se quedan, primero; los de los tipos se rehacen detrás
    own = [g for g in groups if not (TYPE_GROUP_RE.match(g.get("query", "").strip())
                                     and TYPE_GROUP_RE.match(g["query"].strip()).group(1) in known)]
    settings["colorGroups"] = own + [{"query": f"tag:#{tipo}", "color": {"a": 1, "rgb": int(color[1:], 16)}}
                                     for tipo, color in colors]
    lines = [f"Grafo: {len(colors)} tipos con su color"
             + (f" (y {len(own)} grupos propios, que mandan)" if own else "") + "."]
    current = (settings.get("search") or "").strip()
    if not current or replace_filter or current == SYSTEM_FILTER:
        settings["search"] = SYSTEM_FILTER
        lines.append(f"Filtro: `{SYSTEM_FILTER}` (sin las notas del sistema, los README ni los MOC).")
    else:
        lines.append(f"Filtro: se queda el tuyo (`{current}`); con --filter se reemplaza por `{SYSTEM_FILTER}`.")
    settings.update(DISPLAY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines.append("Sin adjuntos ni etiquetas como nodos; los enlaces pendientes salen en gris.")
    return lines


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--filter", action="store_true", help="Reemplaza el filtro del grafo aunque tengas uno propio")
    parser.add_argument("--list", action="store_true", help="Solo muestra el color de cada tipo")
    args = parser.parse_args()
    if args.list:
        for tipo, color in type_colors():
            print(f"{tipo}: {color}")
        return
    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    for line in configure_graph(vault, replace_filter=args.filter):
        print(line)
    print("Si Obsidian está abierto, recárgalo sin guardar («Reload app without saving») para ver el grafo nuevo.")


if __name__ == "__main__":
    main()
