#!/usr/bin/env python3
"""Configura el grafo de Obsidian de la bóveda (`.obsidian/graph.json`) para que se lea el mundo de un vistazo.

  - Un grupo de color por cada tipo de entidad (`tag:#<tipo>`), con el color de su módulo (`color` en su
    modulo.json; si no lo tiene, uno que sale de su nombre). Todas las plantillas llevan su tipo como
    etiqueta. Los grupos que el usuario haya creado a mano se conservan y van primero, así que mandan.
  - Un filtro que deja fuera 00_Sistema (los MOC, la Ficha, el Glosario, los registros, la Bitácora y las
    plantillas), los README de las carpetas y los MOC de las secciones: son índices que enlazan con todo y
    enredan el grafo. Si el usuario ya tiene un filtro propio, no se toca (con --filter, se reemplaza).
  - Los nombres visibles desde más lejos al alejar el zoom. Los adjuntos (las imágenes) y las etiquetas no
    salen como nodos. Los enlaces pendientes sí: son los nodos grises, las entidades que el mundo ya nombra y
    aún no existen.
  - Dos marcadores de grafo (`.obsidian/bookmarks.json`, en el panel Marcadores): «Grafo sin secretos», que
    oculta los secretos (su carpeta y su etiqueta) para enseñar el mundo sin destripar nada, y «Grafo
    completo», que vuelve a mostrarlo todo. Abrir uno cambia el filtro, los colores y lo que se muestra.
    Los demás marcadores no se tocan.
Lo demás se queda como esté: las fuerzas, el zoom y las flechas (ensucian el grafo; se activan a mano, en
Mostrar → Flechas). Es idempotente: se puede volver a ejecutar cuando llegan tipos nuevos (los marcadores se
rehacen con la configuración que tenga el grafo en ese momento).
Con Obsidian abierto: recarga solo el grafo y los marcadores cuando cambian sus archivos, salvo que haya un
grafo abierto en una pestaña, que vuelve a guardar el suyo a los pocos segundos (y al cerrarse) y pisa el
nuevo. Ciérralo antes o, si ya pasó, abre el marcador «Grafo completo», que aplica la configuración entera
desde Obsidian.

Ejemplos:  graph_colors.py   graph_colors.py --filter   graph_colors.py --list"""
import argparse
import colorsys
import hashlib
import json
import re
import sys
import time
from pathlib import Path

# La lógica común vive en vault_lib.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vault_lib import load_modules  # noqa: E402
from vault_lib import vault_path  # noqa: E402

GRAPH_FILE = ".obsidian/graph.json"
BOOKMARKS_FILE = ".obsidian/bookmarks.json"
CORE_PLUGINS_FILE = ".obsidian/core-plugins.json"
SYSTEM_FILTER = "-path:00_Sistema -file:README -file:MOC_"
SECRET_TYPE = "secreto"
FULL_VIEW = "Grafo completo"
SAFE_VIEW = "Grafo sin secretos"
TYPE_GROUP_RE = re.compile(r"^tag:#([\w-]+)$")
COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
# Lo que se muestra: ni los adjuntos ni las etiquetas como nodos; sí los enlaces pendientes y las notas sueltas.
# Los nombres se borran al alejar el zoom: con el valor de Obsidian (textFadeMultiplier 0), al bajar de la
# mitad; con -1, al bajar de un cuarto. Las flechas no se tocan: ensucian el grafo y se activan a mano.
DISPLAY = {"showAttachments": False, "showTags": False, "hideUnresolved": False, "showOrphans": True,
           "textFadeMultiplier": -1}


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


def secret_terms(modules):
    """Los términos del filtro que deja fuera los secretos: su carpeta (la del módulo `secreto`) y su etiqueta,
    por si alguno vive fuera de ella (uno archivado, por ejemplo). Vacío si no hay módulo de secretos."""
    module = modules.get(SECRET_TYPE)
    if not module:
        return []
    folder = (module.get("carpeta") or {}).get("fija", "")
    terms = [f'-path:"{folder}"' if " " in folder else f"-path:{folder}"] if folder else []
    return terms + [f"-tag:#{SECRET_TYPE}"]


def strip_terms(query, terms):
    """La búsqueda sin esos términos, enteros (quitar `-tag:#secreto` no toca `-tag:#secretos`)."""
    for term in terms:
        query = re.sub(r"(?<!\S)" + re.escape(term) + r"(?!\S)", " ", query)
    return " ".join(query.split())


def bookmarks_enabled(vault):
    """Si el plugin principal Marcadores está activado. Sin core-plugins.json, Obsidian lo crea activado."""
    try:
        plugins = json.loads((vault / CORE_PLUGINS_FILE).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return True
    if isinstance(plugins, dict):
        return plugins.get("bookmarks", True) is not False
    return not isinstance(plugins, list) or "bookmarks" in plugins


def configure_bookmarks(vault, settings, secrets):
    """Los marcadores del grafo en `.obsidian/bookmarks.json`: «Grafo completo» y «Grafo sin secretos», con el
    filtro, los colores y lo que se muestra del grafo (el segundo, sin los secretos). Las flechas, las fuerzas
    y el zoom no van, así que abrir uno los deja como estén. Si ya estaban, se rehacen en su sitio; los demás
    marcadores se quedan como estén. Devuelve las líneas del resumen."""
    if not secrets:
        return ["Marcadores: no hay módulo de secretos, así que no hace falta una vista sin ellos."]
    path = vault / BOOKMARKS_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except json.JSONDecodeError:
        data = None
    if not isinstance(data, dict) or not isinstance(data.get("items") or [], list):
        return [f"AVISO: {BOOKMARKS_FILE} no es JSON válido; no lo toco y el grafo queda sin sus marcadores."]
    base = strip_terms(settings.get("search") or "", secrets)
    now = int(time.time() * 1000)
    view = {key: settings[key] for key in ("colorGroups", *DISPLAY) if key in settings}
    fresh = {title: {"type": "graph", "ctime": now, "title": title, "options": dict(view, search=search)}
             for title, search in ((FULL_VIEW, base), (SAFE_VIEW, " ".join([base] + secrets).strip()))}
    items, placed = [], set()
    for item in data.get("items") or []:
        title = item.get("title") if isinstance(item, dict) and item.get("type") == "graph" else None
        if title not in fresh:
            items.append(item)
        elif title not in placed:
            fresh[title]["ctime"] = item.get("ctime", now)
            items.append(fresh[title])
            placed.add(title)
    data["items"] = items + [view for title, view in fresh.items() if title not in placed]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines = [f"Marcadores: «{SAFE_VIEW}» oculta los secretos (`{' '.join(secrets)}`) para enseñar el mundo sin "
             f"destripar nada, y «{FULL_VIEW}» vuelve a mostrarlo todo."]
    if not bookmarks_enabled(vault):
        lines.append("AVISO: el plugin principal Marcadores (Bookmarks) está desactivado; actívalo en Ajustes → "
                     "Plugins principales para ver los marcadores del grafo.")
    return lines


def configure_graph(vault, modules=None, replace_filter=False):
    """Escribe o completa `.obsidian/graph.json` y los marcadores del grafo. Devuelve las líneas del resumen."""
    modules = modules if modules is not None else load_modules()
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
             + ("" if not own else " (y 1 grupo propio, que manda)" if len(own) == 1
                else f" (y {len(own)} grupos propios, que mandan)") + "."]
    secrets = secret_terms(modules)
    current = " ".join((settings.get("search") or "").split())
    # Si se quedó puesto el filtro del marcador «Grafo sin secretos», el grafo vuelve a ser el completo
    if replace_filter or strip_terms(current, secrets) in ("", SYSTEM_FILTER):
        settings["search"] = SYSTEM_FILTER
        lines.append(f"Filtro: `{SYSTEM_FILTER}` (sin las notas del sistema, los README ni los MOC).")
    else:
        lines.append(f"Filtro: se queda el tuyo (`{current}`); con --filter se reemplaza por `{SYSTEM_FILTER}`.")
    settings.update(DISPLAY)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    lines.append("Con los nombres visibles desde más lejos, sin adjuntos ni etiquetas como nodos y con los enlaces "
                 "pendientes en gris (las flechas, a mano: Mostrar → Flechas).")
    return lines + configure_bookmarks(vault, settings, secrets)


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
    print(f"Si en Obsidian había un grafo abierto, habrá guardado el suyo encima (también al cerrar Obsidian): cierra "
          f"esa pestaña y abre el marcador «{FULL_VIEW}» (panel Marcadores), que aplica esta configuración entera.")


if __name__ == "__main__":
    main()
