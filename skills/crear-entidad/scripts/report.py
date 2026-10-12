#!/usr/bin/env python3
"""Informe de lo generado, para mostrar al usuario al final de cualquier generador.

Detecta qué cambió en la bóveda y lo presenta con datos reales y enlaces que se pueden abrir:
  - entidades nuevas: tipo, resumen, carpeta, relevancia, estado, imagen, relaciones con lo que
    ya existía, quién la enlaza y enlaces pendientes que introduce (entidades que nombra y que
    todavía no tienen nota);
  - secretos nuevos (aparte, porque son solo para el autor);
  - notas existentes modificadas (enlaces añadidos y quitados) y enlaces pendientes completados
    (con una nota del mismo nombre, o sustituidos por el nombre definitivo);
  - imágenes nuevas, archivos de sistema nuevos o modificados y notas eliminadas;
  - lo que necesita una decisión del usuario ("Confirmar:") y las preguntas abiertas nuevas;
  - términos nuevos del Glosario;
  - commits hechos desde el inicio (cada uno se deshace con git revert);
  - estado del mundo: auditor, borradores pendientes, enlaces pendientes que ya se pueden crear
    (y cuántos por entidad) y los que no tienen tipo.

Fuentes de los cambios:
  --snapshot [ruta]   ANTES de generar: guarda el estado de la bóveda e imprime la ruta de la
                      instantánea (por defecto, en la carpeta temporal del sistema);
  --baseline <ruta>   lo cambiado desde esa instantánea. Es la fuente más precisa: no confunde lo
                      generado con cambios del usuario que ya estaban sin confirmar, y no necesita git;
  --since <commit>    lo cambiado desde ese commit, incluido lo aún no confirmado (por defecto HEAD);
  --notes A B …       solo esas notas, como nuevas (sin git ni instantánea).

Bitácora (00_Sistema/Bitacora.md), la crónica del mundo para su autor:
  --log TÍTULO        además del informe, añade arriba de la Bitácora una entrada breve con lo esencial
                      (lo creado y modificado, imágenes y mapas, enlaces pendientes, Glosario y lo que
                      queda por decidir). Las notas que existen van enlazadas; los enlaces pendientes,
                      como texto. Si no cambió nada, no añade nada;
  --cycles 7-9        en una tanda del motor, los ciclos que hizo: la entrada lista la acción de cada
                      uno (del Registro de Generación) y remite a su detalle técnico.

Ejemplos:  report.py --snapshot              report.py --baseline <ruta que imprimió --snapshot>
           report.py --since 3b1981f         report.py --notes Aldric_Voss
           report.py --baseline <ruta> --log "Crear entidad: Aldric Voss"
           report.py --baseline <ruta> --log "Expandir el mundo: 3 ciclos" --cycles 7-9"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict
from pathlib import Path

# La lógica común vive en vault_lib.py y audit_world.py (mismo directorio)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_world import run_audit  # noqa: E402
from vault_lib import (CHRONICLE, LINK_WITH_ALIAS_RE, PENDING_NOTE, add_chronicle_entry,  # noqa: E402
                       blocked_links, find_gaps, first, int_value, is_confirmation, load_index, load_modules,
                       parse_note, readable_links)

GLOSSARY = "00_Sistema/04_Convenciones/Glosario.md"
OPEN_QUESTIONS = "00_Sistema/Preguntas_Abiertas.md"
TRACKED_TEXTS = (GLOSSARY, OPEN_QUESTIONS)
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
MAX_LISTED = 8
MAX_ERRORS = 15
# En la Bitácora, listas cortas: es un resumen para leer de un vistazo
LOG_LISTED = 6
LOG_PENDING = 4
GENERATION_LOG = "00_Sistema/06_Generacion/Registro_de_Generacion.md"
MAPS_FOLDER = "00_Sistema/02_Activos/Mapas/"
CYCLE_RE = re.compile(r"^## Ciclo (\d+)\b")


# --- Archivos de la bóveda ---------------------------------------------------

def visible(relative):
    """Fuera de carpetas y archivos ocultos (.obsidian, .trash, .git…)."""
    return not any(part.startswith(".") for part in Path(relative).parts)


def is_note(relative):
    return relative.lower().endswith(".md")


def is_image(relative):
    return relative.lower().endswith(IMAGE_EXTENSIONS)


def vault_files(vault):
    """{ruta relativa: Path} de los archivos visibles de la bóveda."""
    return {path.relative_to(vault).as_posix(): path for path in sorted(vault.rglob("*"))
            if path.is_file() and visible(path.relative_to(vault))}


def read_text(path):
    return path.read_bytes().decode("utf-8", errors="replace")


def fingerprint(path):
    """Huella de un archivo: hash del contenido en las notas; tamaño y fecha en el resto."""
    if is_note(path.name):
        return hashlib.sha1(path.read_bytes()).hexdigest()
    stat = path.stat()
    return f"{stat.st_size}:{stat.st_mtime_ns}"


def links_of(text):
    """Enlaces de una nota: {destino en minúsculas: destino como se escribió}."""
    _, links = parse_note(text)
    return {target.strip().lower(): target.strip() for target, _, _ in links if target.strip()}


def names_of(paths):
    """Nombres que resolvían un enlace en ese conjunto de archivos, en minúsculas."""
    names = set()
    for relative in paths:
        name = relative.rsplit("/", 1)[-1].lower()
        names.add(name)
        if is_note(name):
            names.add(name[:-3])
    return names


def new_lines(old_text, new_text):
    """Líneas de new_text que no estaban en old_text (respetando las repeticiones)."""
    remaining = Counter(old_text.splitlines())
    added = []
    for line in new_text.splitlines():
        if remaining[line]:
            remaining[line] -= 1
        else:
            added.append(line)
    return added


# --- Git ---------------------------------------------------------------------

def git(args, cwd):
    result = subprocess.run(["git", "-c", "core.quotePath=false", *args], cwd=cwd, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git falló")
    return result.stdout


def git_head(vault):
    """Commit actual, o None si la bóveda no está en git."""
    try:
        return git(["rev-parse", "HEAD"], vault).strip()
    except (RuntimeError, FileNotFoundError):
        return None


def commits_since(vault, head):
    """Commits que tocan la bóveda hechos después de `head`, del más antiguo al más reciente."""
    if not head:
        return []
    try:
        return git(["log", "--oneline", "--reverse", f"{head}..HEAD", "--", "."], vault).splitlines()
    except (RuntimeError, FileNotFoundError):
        return []


# --- Fuentes de los cambios --------------------------------------------------
# Todas devuelven {status: {A, M, D}, old_links: {nota modificada: enlaces de antes},
# old_names: nombres que existían antes, added: {archivo seguido: líneas nuevas}, commits}, y
# history: False si no hay estado anterior (--notes).

def take_snapshot(vault):
    files, links, texts = {}, {}, {}
    for relative, path in vault_files(vault).items():
        files[relative] = fingerprint(path)
        if is_note(relative):
            text = read_text(path)
            links[relative] = sorted(links_of(text).values())
            if relative in TRACKED_TEXTS:
                texts[relative] = text
    return {"vault": str(vault.resolve()), "head": git_head(vault), "fecha": time.strftime("%Y-%m-%d %H:%M"),
            "files": files, "links": links, "texts": texts}


def changes_from_snapshot(vault, snapshot):
    current = vault_files(vault)
    old = snapshot["files"]
    status = {"A": sorted(set(current) - set(old)), "D": sorted(set(old) - set(current)),
              "M": sorted(p for p in set(current) & set(old) if fingerprint(current[p]) != old[p])}
    old_links = {p: {t.lower(): t for t in snapshot["links"].get(p, [])} for p in status["M"] if is_note(p)}
    added = {f: new_lines(snapshot["texts"].get(f, ""), read_text(current[f]))
             for f in TRACKED_TEXTS if f in status["A"] or f in status["M"]}
    return {"status": status, "old_links": old_links, "old_names": names_of(old), "added": added,
            "commits": commits_since(vault, snapshot.get("head"))}


def changes_from_git(vault, since):
    def run(*args):
        return git(list(args), vault)

    def old_text(path):
        try:
            return run("show", f"{since}:./{path}")
        except RuntimeError:
            return ""

    # Desde la carpeta de la bóveda, --relative y ls-files dan rutas relativas a ella
    status = {"A": set(), "M": set(), "D": set()}
    for line in run("diff", "--relative", "--no-renames", "--name-status", since, "--", ".").splitlines():
        code, path = line.split("\t", 1)
        status["A" if code[0] in "AC" else "D" if code[0] == "D" else "M"].add(path)
    status["A"].update(run("ls-files", "--others", "--exclude-standard", "--", ".").splitlines())
    status = {k: sorted(p for p in v if visible(p)) for k, v in status.items()}
    old_links = {p: links_of(old_text(p)) for p in status["M"] if is_note(p)}
    added = {f: new_lines(old_text(f) if f in status["M"] else "", read_text(vault / f))
             for f in TRACKED_TEXTS if f in status["A"] or f in status["M"]}
    return {"status": status, "old_links": old_links,
            "old_names": names_of(run("ls-tree", "-r", "--name-only", since).splitlines()),
            "added": added, "commits": commits_since(vault, run("rev-parse", since).strip())}


def changes_from_notes(names, index):
    by_name = {e["name"].lower(): e for e in index}
    found = [by_name[n.lower()]["path"] for n in names if n.lower() in by_name]
    missing = [n for n in names if n.lower() not in by_name]
    # Sin estado anterior: no se sabe qué enlazaban antes las demás notas
    return {"status": {"A": found, "M": [], "D": []}, "old_links": {}, "old_names": set(), "added": {},
            "commits": [], "history": False}, missing


# --- Informe -----------------------------------------------------------------

def plural(count, singular, plural_form=None):
    """'1 región', '3 regiones'… (plural regular si no se indica otro)."""
    if count == 1:
        return f"1 {singular}"
    if plural_form is None:
        plural_form = singular + ("s" if singular[-1] in "aeiouáéíóú" else "es")
    return f"{count} {plural_form}"


def listed(items, limit=MAX_LISTED):
    shown = ", ".join(items[:limit])
    return shown + (f" y {len(items) - limit} más" if len(items) > limit else "")


def gap_label(gap):
    """Tipo esperado de un enlace pendiente, legible: 'personaje', 'faccion, sin módulo todavía'…"""
    expected = gap["expected_type"]
    if not expected:
        return "sin tipo"
    if not gap["expected_modules"]:
        return f"{expected}, sin módulo todavía"
    if gap["expected_modules"] == [expected]:
        return expected
    return f"{expected}: {', '.join(gap['expected_modules'])}"


def glossary_rows(lines):
    """(término, tipo, definición) de las filas de tabla del Glosario."""
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.strip().startswith("|") and len(cells) >= 4 and cells[0] and cells[0] != "Término" \
                and not set(cells[0]) <= set("-: "):
            rows.append((cells[0], cells[1], cells[3]))
    return rows


def cycle_lines(vault, spec):
    """(acciones, remisión, avisos) de los ciclos `spec` («7-9» o «7») del Registro de Generación: la acción
    de cada uno, numerada con su ciclo, y la línea que remite a su detalle técnico."""
    match = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", spec)
    if not match:
        return [], [], [f"--cycles debe ser un ciclo o un rango (7 o 7-9), no «{spec}»"]
    low, high = int(match.group(1)), int(match.group(2) or match.group(1))
    path = vault / GENERATION_LOG
    if not path.is_file():
        return [], [], ["no encuentro el Registro de Generación: la entrada va sin la lista de ciclos"]
    actions, current = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = CYCLE_RE.match(line)
        if heading:
            current = int(heading.group(1))
        elif current is not None and current not in actions and line.strip().startswith("- **Acción:**"):
            actions[current] = line.split("**Acción:**", 1)[1].strip()
    lines, missing = [], []
    for number in range(low, high + 1):
        action = actions.get(number)
        if action is None:
            missing.append(str(number))
            continue
        action = readable_links(action)
        action = action[0].upper() + action[1:] if action else action
        lines.append(f"{number}. {action}" + ("" if action.endswith((".", "»", ")")) else "."))
    span = f"ciclo {low}" if low == high else f"ciclos {low} a {high}"
    footer = [f"- **Detalle técnico:** {span} del [[Registro_de_Generacion|Registro de Generación]]."]
    warnings = [f"el Registro de Generación no tiene los ciclos {', '.join(missing)}"] if missing else []
    return lines, footer, warnings


def build_report(vault, prefix, changes):
    index = load_index(vault)
    by_path = {e["path"]: e for e in index}
    by_name = {e["name"].lower(): e for e in index}
    modules = load_modules()
    gaps, _ = find_gaps(vault)
    files = vault_files(vault)
    file_by_name = {}
    for relative in files:
        name = relative.rsplit("/", 1)[-1].lower()
        file_by_name.setdefault(name, relative)
        if is_note(name):
            file_by_name.setdefault(name[:-3], relative)
    status = changes["status"]

    # Enlaces Markdown relativos al directorio de trabajo: se abren con un clic en el chat
    def link(text, relative):
        target = f"{prefix}/{relative}" if prefix not in ("", ".") else relative
        return f"[{text}](<{target}>)" if " " in target else f"[{text}]({target})"

    def entity_link(entry):
        return link(entry["titulo"], entry["path"])

    def path_link(relative):
        return entity_link(by_path[relative]) if relative in by_path else link(relative.rsplit("/", 1)[-1], relative)

    def target_link(target):
        """Enlace a una entidad o archivo que existe; si no existe (un enlace pendiente), su nombre en código."""
        entry = by_name.get(target.lower())
        if entry:
            return entity_link(entry)
        relative = file_by_name.get(target.rsplit("/", 1)[-1].lower())
        return path_link(relative) if relative else f"`{target}`"

    def linkify(text):
        """[[Nota|texto]] → enlace que se abre; si la nota no existe, el texto legible."""
        def replace(match):
            target, alias = match.group(1).rstrip("\\").strip(), match.group(2)
            entry = by_name.get(target.lower())
            return link(alias or entry["titulo"], entry["path"]) if entry else (alias or target.replace("_", " "))
        return LINK_WITH_ALIAS_RE.sub(replace, text)

    def emoji_of(entry):
        emoji = modules.get(entry["tipo"], {}).get("emoji", "")
        return f"{emoji} " if emoji else ""

    created = sorted((by_path[p] for p in status["A"] if p in by_path),
                     key=lambda e: (-(e["relevancia"] or 0), e["tipo"], e["name"]))
    secrets = [e for e in created if e["tipo"] == "secreto"]
    entities = [e for e in created if e["tipo"] != "secreto"]
    modified = [by_path[p] for p in status["M"] if p in by_path]
    images = [p for p in status["A"] if is_image(p)]
    questions = [l.strip() for l in changes["added"].get(OPEN_QUESTIONS, []) if l.strip().startswith("- [ ]")]
    decisions = [q for q in questions if is_confirmation(q)]
    others = [q for q in questions if q not in decisions]
    terms = glossary_rows(changes["added"].get(GLOSSARY, []))
    # El Glosario y las Preguntas abiertas tienen su propia sección cuando aportan algo nuevo
    shown_apart = {GLOSSARY} if terms else set()
    shown_apart |= {OPEN_QUESTIONS} if questions else set()
    system_new = [p for p in status["A"] if p not in by_path and not is_image(p) and p not in shown_apart]
    system_changed = [p for p in status["M"] if p not in by_path and not is_image(p) and p not in shown_apart]

    # Enlaces añadidos y quitados en cada nota modificada
    added_links, removed_links = {}, {}
    for path, old in changes["old_links"].items():
        if path in files:
            new = links_of(read_text(files[path]))
            added_links[path] = {k: v for k, v in new.items() if k not in old}
            removed_links[path] = {k: v for k, v in old.items() if k not in new}

    # Enlaces pendientes sustituidos por el nombre definitivo (un nombre de rol, como Madre_de_X, que se
    # cambia por el de la entidad creada): enlaces quitados que no existían, cambiados por el mismo en todas sus notas
    removed_gaps = defaultdict(list)
    for path, removed in removed_links.items():
        for key, target in removed.items():
            if key.rsplit("/", 1)[-1] not in changes["old_names"]:
                removed_gaps[key].append((path, target))
    created_names = {e["name"].lower() for e in created}
    completed = []
    for key, places in sorted(removed_gaps.items()):
        candidates = None
        for path, _ in places:
            here = {k for k in added_links.get(path, {}) if k in by_name}
            candidates = here if candidates is None else candidates & here
        candidates = candidates or set()
        preferred = (candidates & created_names) or candidates
        replacement = by_name[next(iter(preferred))] if len(preferred) == 1 else None
        completed.append((places[0][1], replacement, [p for p, _ in places]))

    # Quién enlaza a cada entidad (sin contar secretos, que solo enlazan hacia fuera)
    backlinks = defaultdict(list)
    for entry in index:
        if entry["tipo"] == "secreto":
            continue
        for target in entry["enlaces"]:
            if target.lower() != entry["name"].lower():
                backlinks[target.lower()].append(entry)

    # Enlaces pendientes completados creando una nota con su mismo nombre: notas que ya existían y ya la nombraban
    def linked_before(path, key):
        old = changes["old_links"].get(path)
        if old is not None:
            return any(k.rsplit("/", 1)[-1] == key for k in old)
        return path not in status["M"]

    named = []
    for entry in entities if changes.get("history", True) else []:
        key = entry["name"].lower()
        before = [b["path"] for b in backlinks.get(key, []) if b["path"] not in status["A"]
                  and not b["path"].startswith("00_Sistema/") and linked_before(b["path"], key)]
        if before:
            named.append((entry, before))
    created_paths = {e["path"] for e in created}

    by_type = Counter(e["tipo"] for e in entities)
    created_text = ", ".join(plural(n, t) for t, n in sorted(by_type.items())) or "ninguna entidad"
    out = ["# Informe de lo generado", "",
           f"**Creado:** {created_text} · {plural(len(images), 'imagen', 'imágenes')} · "
           f"{plural(len(secrets), 'secreto')}",
           f"**Modificado:** {plural(len(modified), 'nota existente', 'notas existentes')} · "
           f"{plural(len(completed) + len(named), 'enlace pendiente completado', 'enlaces pendientes completados')} · "
           f"Glosario: {plural(len(terms), 'término nuevo', 'términos nuevos')} · "
           f"Preguntas abiertas: {plural(len(questions), 'nueva', 'nuevas')}"]
    if not any(status.values()):
        out += ["", "No hay cambios en la bóveda."]

    if entities:
        out += ["", "## Entidades nuevas"]
        for entry in entities:
            relevance = entry["relevancia"] if entry["relevancia"] is not None else "?"
            folder = entry["path"].rsplit("/", 1)[0] if "/" in entry["path"] else "(raíz)"
            out += ["", f"### {emoji_of(entry)}{entity_link(entry)} — {entry['tipo']} · relevancia {relevance}"]
            if entry["resumen"]:
                out.append(f"> {entry['resumen']}")
            out.append(f"- **Dónde:** `{folder}` · {entry['estado'] or 'sin estado'} ({entry['origen']})")
            image = entry["relaciones"].get("imagen")
            out.append(f"- **Imagen:** {target_link(image[0]) if image else 'sin imagen'}")
            relations = []
            for prop, targets in entry["relaciones"].items():
                existing = [by_name[t.lower()] for t in targets if t.lower() in by_name]
                if prop != "imagen" and existing:
                    relations.append(f"{prop}: " + ", ".join(entity_link(e) for e in existing))
            out.append("- **Relaciones con lo existente:** " + (" · ".join(relations) or "ninguna"))
            linked_from = [entity_link(e) for e in backlinks.get(entry["name"].lower(), [])]
            out.append("- **Enlazada desde:** " + (listed(linked_from) or "ninguna entidad todavía"))
            # Los que introduce: entidades que nombra y que solo nombra lo creado ahora
            mine = [g for g in gaps if entry["path"] in g["notes"]]
            own = [g for g in mine if set(g["notes"]) <= created_paths]
            shown = [f"`{g['link']}` ({gap_label(g)})" for g in own]
            out.append(f"- **Enlaces pendientes que introduce ({len(own)}):** " + (", ".join(shown) or "ninguno"))
            # Entidades por crear que ya nombraban otras notas (la especie, la región…)
            pending = [f"`{g['link']}`" for g in mine if g not in own]
            if pending:
                out.append("- **Nombra otras entidades por crear:** " + listed(pending))
    if secrets:
        out += ["", "## Secretos nuevos (solo para ti)"]
        for entry in secrets:
            affected = ", ".join(target_link(t) for t in entry["relaciones"].get("afecta_a", [])) or "—"
            out.append(f"- 🔒 {entity_link(entry)} — afecta a {affected}: {entry['resumen']}")
    if modified:
        out += ["", "## Notas existentes modificadas"]
        for entry in modified:
            added = added_links.get(entry["path"], {})
            removed = removed_links.get(entry["path"], {})
            parts = []
            if added:
                parts.append("añade " + listed([target_link(t) for t in added.values()]))
            if removed:
                parts.append("quita " + listed([f"`{t}`" for t in removed.values()]))
            if entry["path"] not in changes["old_links"]:
                parts.append("modificada")
            detail = "; ".join(parts) or "cambios de texto, sin enlaces nuevos"
            out.append(f"- {emoji_of(entry)}{entity_link(entry)} ({entry['tipo']}): {detail}")
    if completed or named:
        out += ["", "## Enlaces pendientes completados"]
        for entry, places in named:
            out.append(f"- {entity_link(entry)}: ya la nombraban {listed([path_link(p) for p in places])}")
        for gap, replacement, places in completed:
            where = listed([path_link(p) for p in places])
            if replacement:
                out.append(f"- `{gap}` → {entity_link(replacement)} (en {where})")
            else:
                out.append(f"- `{gap}`: quitado de {where}, sin un sustituto claro")
    if images:
        out += ["", "## Imágenes nuevas", *[f"- {path_link(p)}" for p in images]]
    if system_new or system_changed:
        out += ["", "## Archivos de sistema"]
        if system_new:
            out.append("- **Nuevos:** " + listed([path_link(p) for p in system_new], 20))
        if system_changed:
            out.append("- **Modificados:** " + listed([path_link(p) for p in system_changed], 20))
    if status["D"]:
        out += ["", "## Eliminados o movidos", *[f"- `{p}`" for p in status["D"]]]
    if decisions:
        out += ["", "## Necesita tu decisión", *[linkify(q) for q in decisions]]
    if others:
        out += ["", "## Preguntas abiertas nuevas", *[linkify(q) for q in others]]
    if terms:
        out += ["", "## Términos nuevos en el Glosario",
                *[f"- **{linkify(term)}** ({kind}): {linkify(definition)}" for term, kind, definition in terms]]
    if changes["commits"]:
        out += ["", "## Commits"]
        for line in changes["commits"]:
            commit, _, message = line.partition(" ")
            out.append(f"- `{commit}` {message}")
        out += ["", "Cada uno se deshace por separado con `git revert <hash>`."]

    audit = run_audit(vault)
    touched = {e["name"].lower() for e in created + modified}
    own_warnings = [w for w in audit["avisos"] if any(f"[[{n}]]" in w.lower() for n in touched)]
    # Los enlaces pendientes que esperan una confirmación no se pueden crear todavía
    blocked = blocked_links(vault)
    ready = [g for g in gaps if g["expected_modules"] and g["link"].lower() not in blocked]
    ready.sort(key=lambda g: -len(g["notes"]))
    untyped = [g for g in gaps if not g["expected_type"]]
    auditor = (f"- **Auditor:** {plural(len(audit['errores']), 'error', 'errores')}, "
               f"{plural(len(audit['avisos']), 'aviso')}")
    out += ["", "## Estado del mundo",
            auditor + (f" ({len(own_warnings)} sobre lo generado)" if own_warnings else "")]
    out += [f"  - ERROR: {linkify(e)}" for e in audit["errores"][:MAX_ERRORS]]
    if len(audit["errores"]) > MAX_ERRORS:
        out.append(f"  - … y {len(audit['errores']) - MAX_ERRORS} errores más (audit_world.py los lista todos)")
    out += [f"  - AVISO: {linkify(w)}" for w in own_warnings]
    out += [f"- **Entidades en el mundo:** {audit['entidades']}",
            f"- **Borradores pendientes de revisión:** {audit['borradores']} "
            f"(procedurales: {audit['borradores_procedurales']})",
            f"- **Enlaces pendientes que ya se pueden crear:** {len(ready)}, "
            f"{len(ready) / max(len(index), 1):.1f} por entidad"
            + (f" (p. ej. {', '.join('`' + g['link'] + '`' for g in ready[:3])})" if ready else "")]
    if untyped:
        out.append(f"- **Enlaces pendientes sin tipo:** {len(untyped)} "
                   f"({listed(['`' + g['link'] + '`' for g in untyped])}): asígnaselo con "
                   f"`pending_links.py --set <Enlace>=<tipo>`")
    if (vault / PENDING_NOTE).is_file():
        out.append(f"- **Registro de enlaces pendientes:** {path_link(PENDING_NOTE)}")

    # Bitácora: lo esencial, con enlaces de Obsidian a lo que existe y los enlaces pendientes como texto
    def wiki(entry):
        title = entry["titulo"] or entry["name"].replace("_", " ")
        return f"[[{entry['name']}|{title}]]" if title != entry["name"] else f"[[{entry['name']}]]"

    log = []
    if entities:
        described = []
        for entry in entities:
            extras = (["imagen"] if entry["relaciones"].get("imagen") else []) + \
                     (["mapa"] if int_value(first(entry["props"].get("mapa_edicion"))) else [])
            relevance = entry["relevancia"] if entry["relevancia"] is not None else "?"
            described.append(f"{wiki(entry)} ({entry['tipo']}, relevancia {relevance}"
                             + (f", con {' y '.join(extras)}" if extras else "") + ")")
        log.append("- **Creadas:** " + listed(described, LOG_LISTED) + ".")
    if secrets:
        log.append(f"- **Secretos:** {plural(len(secrets), 'nuevo', 'nuevos')}, solo para ti (en `80_Secretos`).")
    if modified:
        log.append("- **Modificadas:** " + listed([wiki(e) for e in modified], LOG_LISTED) + ".")
    # Las imágenes y los mapas de lo creado ya los dice su línea («con imagen y mapa»): aquí, los de las
    # notas que ya existían (una imagen regenerada, una edición nueva de un mapa)
    other_images = [p for p in images if not any(n in p.rsplit("/", 1)[-1].lower() for n in created_names)]
    if other_images:
        log.append(f"- **Imágenes:** {plural(len(other_images), 'nueva', 'nuevas')}"
                   + (" de notas que ya existían" if created else "") + ".")
    mapped = []
    for path in other_images:
        if path.startswith(MAPS_FOLDER):
            stem = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            base = re.sub(r"(_Nivel_\d+)?(_v\d+)?$", "", stem[len("Mapa_"):] if stem.startswith("Mapa_") else stem)
            entry = by_name.get(base.lower())
            if entry and entry not in mapped:
                mapped.append(entry)
    if mapped:
        log.append("- **Mapas:** " + listed([f"{wiki(e)} (edición {first(e['props'].get('mapa_edicion')) or '?'})"
                                             for e in mapped], LOG_LISTED) + ".")
    # Enlaces pendientes nuevos: los que solo nombran notas creadas ahora o que acaban de enlazarlos
    new_pending = [g for g in gaps if g["notes"] and all(
        note in created_paths or g["link"].lower() in added_links.get(note, {}) for note in g["notes"])]
    done = [wiki(e) for e, _ in named] + [wiki(r) for _, r, _ in completed if r]
    if new_pending or completed or named:
        parts = []
        if new_pending:
            parts.append(f"{plural(len(new_pending), 'nuevo', 'nuevos')} ("
                         + listed([g["link"].replace("_", " ") for g in new_pending], LOG_PENDING) + ")")
        if completed or named:
            parts.append(plural(len(completed) + len(named), "completado", "completados")
                         + (f" ({listed(done, LOG_PENDING)})" if done else ""))
        log.append("- **Enlaces pendientes:** " + "; ".join(parts) + ".")
    if terms:
        log.append(f"- **Glosario:** {plural(len(terms), 'término nuevo', 'términos nuevos')}.")
    if decisions or others:
        parts = ([plural(len(decisions), "confirmación", "confirmaciones")] if decisions else []) + \
                ([plural(len(others), "pregunta nueva", "preguntas nuevas")] if others else [])
        log.append("- **Para decidir:** " + " y ".join(parts) + " en [[Preguntas_Abiertas|Preguntas Abiertas]].")
    deleted = [p for p in status["D"] if is_note(p)]
    if deleted:
        log.append("- **Archivadas o eliminadas:** "
                   + listed([p.rsplit("/", 1)[-1][:-3].replace("_", " ") for p in deleted], LOG_LISTED) + ".")
    return out, log


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--snapshot", nargs="?", const="", metavar="RUTA",
                        help="Antes de generar: guarda el estado de la bóveda e imprime la ruta de la instantánea")
    source.add_argument("--baseline", metavar="RUTA", help="Informa de lo cambiado desde esa instantánea")
    source.add_argument("--since", metavar="COMMIT", help="Informa de lo cambiado desde ese commit (por defecto HEAD)")
    source.add_argument("--notes", nargs="+", metavar="NOTA", help="Informa solo de estas notas, como nuevas")
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--log", metavar="TÍTULO", help="Añade a la Bitácora una entrada breve con lo generado")
    parser.add_argument("--cycles", metavar="DESDE-HASTA", help="Con --log, los ciclos del motor de la tanda (7-9)")
    args = parser.parse_args()
    if args.cycles and not args.log:
        parser.error("--cycles va con --log")

    vault = Path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")

    if args.snapshot is not None:
        stamp = time.strftime("%Y%m%d_%H%M%S")
        target = Path(args.snapshot) if args.snapshot else \
            Path(tempfile.gettempdir()) / f"world_snapshot_{stamp}_{os.getpid()}.json"
        target.write_text(json.dumps(take_snapshot(vault), ensure_ascii=False), encoding="utf-8")
        print(target)
        return

    if args.notes:
        changes, missing = changes_from_notes(args.notes, load_index(vault))
        if missing:
            print(f"AVISO: no encuentro estas notas: {', '.join(missing)}")
    elif args.baseline:
        path = Path(args.baseline)
        if not path.is_file():
            sys.exit(f"Error: no existe la instantánea '{path}'. Usa --since <commit> o --notes.")
        snapshot = json.loads(path.read_text(encoding="utf-8"))
        if Path(snapshot["vault"]) != vault.resolve():
            print(f"AVISO: la instantánea es de otra bóveda ({snapshot['vault']}).")
        changes = changes_from_snapshot(vault, snapshot)
    else:
        try:
            changes = changes_from_git(vault, args.since or "HEAD")
        except (RuntimeError, FileNotFoundError) as error:
            sys.exit(f"Error: no puedo leer los cambios con git ({error}). Usa --snapshot y --baseline, o --notes.")

    out, log = build_report(vault, Path(args.vault).as_posix(), changes)
    print("\n".join(out))
    if args.log:
        actions, footer, warnings = cycle_lines(vault, args.cycles) if args.cycles else ([], [], [])
        if not log and not args.cycles:
            print("\nBitácora: no hay cambios en la bóveda; no añado ninguna entrada.")
            return
        body = actions + (log or ["- Sin cambios en la bóveda."]) + footer
        warnings += add_chronicle_entry(vault, args.log.strip(), body)
        print(f"\nBitácora: añadida la entrada «{args.log.strip()}» en {CHRONICLE}.")
        for warning in warnings:
            print(f"AVISO: {warning}")


if __name__ == "__main__":
    main()
