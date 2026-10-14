#!/usr/bin/env python3
"""Las comprobaciones de la salud de una bóveda, compartidas: las usan diagnosticar-mundo (la salud de un mundo
abierto) y finalizar-mundo (la lista estricta del cierre). Cada una devuelve datos; quien la usa decide qué es un
problema en su caso y cómo lo cuenta. La bóveda se carga una sola vez (`Health`)."""
import re
import sys
from pathlib import Path

from audit_world import run_audit
from check_note import checker
from vault_lib import (CONTAINMENT_PROPS, GLOSSARY, LINK_RE, OPEN_QUESTIONS, OUTSIDE_TYPE, SECRET_TYPE, WORLD_SHEET,
                       blocked_links, find_gaps, first, index_vault, int_value, is_confirmation, is_hidden, link_value,
                       load_index, load_modules, map_applies, map_status, normalize, parse_map_key, parse_map_routes,
                       place_types, read_world, split_note)

ASSETS = "00_Sistema/02_Activos"
ARCHIVE_IMAGES = f"{ASSETS}/Anteriores"
INBOX = "00_Sistema/05_Bandeja_de_Entrada"
IMAGE_RE = re.compile(r"\.(png|jpe?g|webp|gif|svg|bmp)$", re.IGNORECASE)
# Anotaciones de trabajo: normales mientras el mundo crece, pero no pueden quedar en un mundo cerrado
WORK_NOTES = [(re.compile(r"\bpor definir\b", re.IGNORECASE), "«por definir»"),
              (re.compile(r"\bpor confirmar\b", re.IGNORECASE), "«por confirmar»"),
              (re.compile(r"\bpor decidir\b", re.IGNORECASE), "«por decidir»"),
              (re.compile(r"\*Sin cartografiar\.\*"), "«sin cartografiar»"),
              (re.compile(r"\*Se quita en la edición siguiente\.\*"), "«se quita en la edición siguiente»"),
              (re.compile(r"\(espera confirmación\)|sin módulo todavía"), "una marca del registro"),
              (re.compile(r"\{\{|\bTODO\b"), "un resto de plantilla")]
# Un enlace pendiente menor: lo nombra una sola nota, que no pesa mucho, y pocas veces
MINOR_RELEVANCE = 3
MINOR_MENTIONS = 2


class Health:
    """La bóveda cargada una vez para las comprobaciones: índice, módulos, nombres, Ficha, enlaces pendientes,
    auditoría y validación de las notas (las tres últimas, solo si se piden)."""

    def __init__(self, vault):
        self.vault = vault
        self.modules = load_modules()
        self.index = load_index(vault)
        self.by_name = {e["name"].lower(): e for e in self.index}
        self.names, _ = index_vault(vault)
        self.world = read_world(vault)
        self._gaps = self._audit = self._checks = None

    @property
    def gaps(self):
        if self._gaps is None:
            self._gaps = find_gaps(self.vault)[0]
        return self._gaps

    def audit(self):
        if self._audit is None:
            self._audit = run_audit(self.vault)
        return self._audit

    def note_checks(self):
        """[(entidad, errores, avisos)] de check_note, de todas las entidades."""
        if self._checks is None:
            run = checker(self.vault)
            self._checks = [(entry, *run(self.vault / entry["path"])[:2]) for entry in self.index]
        return self._checks


def undefined_pillars(vault):
    """Los pilares que la Ficha deja «Por definir»."""
    _, body = split_note((vault / WORLD_SHEET).read_text(encoding="utf-8"))
    return [m.group(1) for line in body for m in [re.match(r"^- \*\*(.+?):\*\*\s*Por definir\.\s*$", line)] if m]


def open_questions(vault):
    """Las preguntas sin cerrar, en su orden: (línea, si es una confirmación, si es un pilar por definir)."""
    path = vault / OPEN_QUESTIONS
    found, section = [], ""
    for line in (path.read_text(encoding="utf-8").splitlines() if path.is_file() else []):
        if line.startswith("## "):
            section = normalize(line[3:])
        if re.match(r"^\s*-\s*\[ \]", line):
            found.append((line.strip(), is_confirmation(line), section.startswith("pilares por definir")))
    return found


def pending(health):
    """Los enlaces pendientes, por lo que piden: los que se pueden crear, los que esperan una confirmación, los que
    no tienen tipo o no tienen módulo, los menores (para proponer disolverlos) y los de fuera del mundo."""
    vault = health.vault
    sheet_text = normalize((vault / WORLD_SHEET).read_text(encoding="utf-8"))
    gaps = [g for g in health.gaps if g["expected_type"] != OUTSIDE_TYPE]
    blocked = blocked_links(vault)
    ready = [g for g in gaps if g["expected_modules"] and g["link"].lower() not in blocked]
    minor = []
    for gap in ready:
        linker = health.by_name.get(Path(gap["notes"][0]).stem.lower()) if len(gap["notes"]) == 1 else None
        if linker and (linker["relevancia"] or 0) <= MINOR_RELEVANCE and len(gap["occurrences"]) <= MINOR_MENTIONS \
                and normalize(gap["link"]) not in sheet_text:
            minor.append(gap)
    return {"all": gaps, "ready": ready, "waiting": [g for g in gaps if g["link"].lower() in blocked],
            "untyped": [g for g in gaps if not g["expected_type"]],
            "no_module": [g for g in gaps if g["expected_type"] and not g["expected_modules"]],
            "minor": minor, "outside": [g for g in health.gaps if g["expected_type"] == OUTSIDE_TYPE]}


def drafts(health):
    return [e for e in health.index if e["estado"] == "borrador"]


def work_notes(health):
    """[(nota, [anotaciones])] de las entidades y del Glosario con anotaciones de trabajo."""
    found = []
    for entry in health.index:
        text = (health.vault / entry["path"]).read_text(encoding="utf-8")
        hits = [label for pattern, label in WORK_NOTES if pattern.search(text)]
        if hits:
            found.append((entry["name"], hits))
    glossary = health.vault / GLOSSARY
    if glossary.is_file():
        text = glossary.read_text(encoding="utf-8")
        hits = [label for pattern, label in WORK_NOTES[:3] if pattern.search(text)]
        if hits:
            found.append(("el Glosario", hits))
    return found


def missing_images(health):
    """Las entidades (no los secretos, que no llevan) sin imagen, o con una que no existe."""
    return [e["name"] for e in health.index if e["tipo"] != SECRET_TYPE
            and (link_value(first(e["props"].get("imagen")) or "") or "").lower() not in health.names]


def broken_images(health):
    """[(nota, imagen)]: imágenes que una entidad enlaza o incrusta y que no existen."""
    found = []
    for entry in health.index:
        text = (health.vault / entry["path"]).read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if IMAGE_RE.search(target) and target.lower() not in health.names:
                found.append((entry["name"], target))
    return found


def map_states(health, complete=False):
    """(mapas que toca dibujar [(nombre, razón)], lo más alto del mapa [(nombre, edición, si le toca mapa)]). Con
    `complete`, cualquier cambio sin dibujar pide una edición nueva (al cerrar el mundo)."""
    stale, tops = [], []
    containers = set(place_types(health.modules))
    for entry in health.index:
        module = health.modules.get(entry["tipo"], {})
        rule = map_applies(module, entry["props"], entry["relevancia"]) if module.get("mapa") else None
        if rule:
            _, body = split_note((health.vault / entry["path"]).read_text(encoding="utf-8"))
            zones, _ = parse_map_key(body)
            routes, _ = parse_map_routes(body)
            if zones is None:
                stale.append((entry["name"], "sin sección Mapa"))
            else:
                status = map_status(module, entry["props"], zones, entry["relevancia"], routes, complete=complete)
                if status["toca"]:
                    stale.append((entry["name"], status["razon"]))
        ups = [t for key in CONTAINMENT_PROPS for t in entry["relaciones"].get(key, []) if t.lower() in health.by_name]
        if entry["tipo"] in containers and not ups:
            tops.append((entry["name"], int_value(first(entry["props"].get("mapa_edicion"))) or 0, bool(rule)))
    return stale, tops


def loose_images(vault):
    """Imágenes de 02_Activos (fuera de Anteriores) que ninguna nota usa."""
    used = set()
    for path in vault.rglob("*.md"):
        if not is_hidden(path.relative_to(vault)):
            used |= {m.group(1).strip().lower() for m in LINK_RE.finditer(path.read_text(encoding="utf-8"))}
    folder = vault / ASSETS
    return [p for p in sorted(folder.rglob("*")) if p.is_file() and IMAGE_RE.search(p.name)
            and ARCHIVE_IMAGES not in p.relative_to(vault).as_posix() and p.name.lower() not in used] \
        if folder.is_dir() else []


def inbox(vault):
    """Las notas de la Bandeja de Entrada (sin su README)."""
    folder = vault / INBOX
    return [p.name for p in sorted(folder.glob("*")) if p.is_file() and p.name != "README.md"] if folder.is_dir() else []


def tidy_images(vault):
    """Aparta a 02_Activos/Anteriores, con `_suelta`, las imágenes que ninguna nota usa. No borra nada. Devuelve las
    líneas del resumen."""
    orphans = loose_images(vault)
    if not orphans:
        return ["No hay imágenes sueltas."]
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "generar-imagen" / "scripts"))
        from fetch_download import archive_folder
        folder, created = archive_folder(vault / ASSETS)
    except ImportError:
        folder, created = vault / ARCHIVE_IMAGES, not (vault / ARCHIVE_IMAGES).is_dir()
        folder.mkdir(parents=True, exist_ok=True)
    lines = []
    for image in orphans:
        target, number = folder / f"{image.stem}_suelta{image.suffix}", 2
        while target.exists():
            target, number = folder / f"{image.stem}_suelta_{number}{image.suffix}", number + 1
        image.replace(target)
        lines.append(f"Apartada: {image.relative_to(vault).as_posix()} → {target.relative_to(vault).as_posix()}")
    if created:
        lines.append(f"AVISO: se creó {ARCHIVE_IMAGES}: regístrala en «Carpetas añadidas por skills» de la Guía de "
                     f"Organización, como dice generar-imagen.")
    return lines
