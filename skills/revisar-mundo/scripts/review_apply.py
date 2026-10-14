#!/usr/bin/env python3
"""Aplica lo decidido en una tanda de revisión de borradores.

  --canon NOTA …     Pasa a canon: `estado: canon` y la fecha. Lo que propuso al crearse y esperaba
                     confirmación en Preguntas Abiertas («Confirmar: … (propuesto al crear [[NOTA]])») queda
                     confirmado, y el Registro de Canon gana una línea.
  --keep NOTA …      Sigue en borrador: anota `revisado` con la fecha, y la cola la deja para el final.
  --rehacer NOTA …   Se archiva para crearla de nuevo, distinta: va a 00_Sistema/03_Archivados como
                     `<NOTA>_archivada`, así sus menciones vuelven a ser enlaces pendientes, con su tipo, y el
                     motor (o el usuario) la crea otra vez con el mismo nombre.
  --quitar NOTA …    Sale del mundo: va a 00_Sistema/03_Archivados con su nombre (sus menciones no quedan
                     pendientes: el auditor avisa de cada una hasta que se reescribe), y su zona en la leyenda
                     del mapa que la contiene se retira. El script lista las menciones que hay que reescribir.
  --reason TEXTO     El motivo, para el Registro de Canon y la nota archivada (opcional).

Al archivar, de cualquiera de las dos formas:
- la nota queda con `estado: archivado` y una línea que dice cuándo y por qué;
- sus imágenes (la suya, su mapa y sus ediciones o versiones anteriores) van a 02_Activos/Anteriores con
  `_archivada`, y la nota archivada las sigue enlazando. Así la imagen de la entidad rehecha no choca con la
  vieja;
- los secretos que solo la afectan a ella (o a lo que se archiva con ella) se archivan también.

Al final rehace el registro de enlaces pendientes y propone las líneas de la Bitácora (`log_entry.py`, que
además rehace las Estadísticas).

Ejemplos:  review_apply.py --canon Aldric_Voss Puerto_Gris --keep Gremio_del_Puerto
           review_apply.py --rehacer Torre_Hendida --reason "demasiado parecida a la Ciudadela"
           review_apply.py --quitar Culto_del_Pozo"""
import argparse
import datetime
import re
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[2]
# La lógica común vive en los scripts de crear-entidad; las imágenes anteriores, en los de generar-imagen
sys.path.insert(0, str(SKILLS / "crear-entidad" / "scripts"))
from map_key import frontmatter_end, legends, retire_zone, set_property  # noqa: E402
from pending_links import build  # noqa: E402
from vault_lib import (ARCHIVED_FOLDER, ATTACHMENT_RE, CANON_LOG, LINK_RE, OPEN_QUESTIONS, PENDING_NOTE,  # noqa: E402
                       SECRET_TYPE, find_gaps, first, is_confirmation, is_hidden, load_index, load_modules,
                       load_pending_types, resolve_note, strip_links)
from vault_lib import vault_path  # noqa: E402

ASSETS = "00_Sistema/02_Activos"
ARCHIVE_IMAGES = "00_Sistema/02_Activos/Anteriores"
DEFAULT_REASON = "Revisión de borradores"
LOG_SEPARATOR_RE = re.compile(r"^\|\s*-+\s*\|")
MAX_MENTION_LINES = 2


def unique(folder, stem, suffix):
    """`<stem><suffix>` en `folder` sin pisar nada: con _2, _3… si ya existe."""
    candidate, number = folder / f"{stem}{suffix}", 2
    while candidate.exists():
        candidate, number = folder / f"{stem}_{number}{suffix}", number + 1
    return candidate


def archive_images_folder(vault):
    """La carpeta de imágenes anteriores, con su README (el de generar-imagen). Devuelve (carpeta, si se creó)."""
    try:
        sys.path.insert(0, str(SKILLS / "generar-imagen" / "scripts"))
        from fetch_download import archive_folder
        return archive_folder(vault / ASSETS)
    except ImportError:
        folder = vault / ARCHIVE_IMAGES
        created = not folder.is_dir()
        folder.mkdir(parents=True, exist_ok=True)
        return folder, created


def attachments(text, files):
    """Archivos de 02_Activos que la nota enlaza o incrusta (su imagen, su mapa, sus versiones): {nombre: ruta}."""
    found = {}
    for match in LINK_RE.finditer(text):
        name = match.group(1).strip()
        path = files.get(name.lower())
        if ATTACHMENT_RE.search(name) and path and ASSETS.lower() in path.as_posix().lower():
            found[name] = path
    return found


def rename_links(text, old, new):
    """Cambia los enlaces a `old` por `new` (con o sin `!`, con texto o tamaño detrás)."""
    return re.sub(r"(!?\[\[)" + re.escape(old) + r"(?=[\]|#^\\])", lambda m: m.group(1) + new, text, flags=re.IGNORECASE)


def mark_archived(text, today, why):
    """La nota con `estado: archivado`, la fecha y una línea bajo el título que dice cuándo y por qué."""
    lines = text.splitlines()
    end = frontmatter_end(lines)
    if end is not None:
        end = set_property(lines, end, "estado", "archivado")
        set_property(lines, end, "ultima_revision", today)
    heading = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if heading is not None:
        lines[heading + 1:heading + 1] = ["", f"> **Archivada el {today}**, {why}."]
    return "\n".join(lines) + "\n"


def archive(vault, path, mode, today, why, files, images_folder):
    """Mueve una nota a los archivados (con otro nombre al rehacer) y sus imágenes a las anteriores; `why` va en
    la línea que dice cuándo y por qué. Devuelve (ruta nueva, imágenes movidas)."""
    text = path.read_text(encoding="utf-8")
    moved = []
    for name, image in attachments(text, files).items():
        if image.parent.name == images_folder.name and image.stem.lower().endswith("_archivada"):
            continue
        target = unique(images_folder, f"{image.stem}_archivada", image.suffix)
        image.replace(target)
        files[target.name.lower()] = target
        text = rename_links(text, name, target.name)
        moved.append(target.name)
    folder = vault / ARCHIVED_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    stem = f"{path.stem}_archivada" if mode == "rehacer" else path.stem
    target = unique(folder, stem, ".md")
    target.write_text(mark_archived(text, today, why), encoding="utf-8", newline="\n")
    path.unlink()
    return target, moved


def confirm_proposals(vault, names, today):
    """Marca hechas las confirmaciones de esas notas: las que propusieron al crearse y las que las tenían como
    sujeto (su primer enlace: «Confirmar: existe [[Nota]]…»). Devuelve {nota: cuántas}."""
    path = vault / OPEN_QUESTIONS
    if not path.is_file():
        return {}
    counts, lines = {}, path.read_text(encoding="utf-8").splitlines()
    wanted = {name.lower(): name for name in names}
    for i, line in enumerate(lines):
        if not is_confirmation(line):
            continue
        proposer = re.search(r"propuesto al crear \[\[([^\]|#^\\]+)", line, re.IGNORECASE)
        subject = re.search(r"\[\[([^\]|#^\\]+)", line)
        name = next((wanted[m.group(1).strip().lower()] for m in (proposer, subject)
                     if m and m.group(1).strip().lower() in wanted), None)
        if name:
            lines[i] = line.replace("[ ]", "[x]", 1).rstrip() + f" — confirmado al pasar a canon el {today}"
            counts[name] = counts.get(name, 0) + 1
    if counts:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return counts


def log_rows(vault, rows):
    """Añade las filas arriba de la tabla del Registro de Canon (la más reciente, arriba). False si no
    encuentra la tabla."""
    if not rows:
        return True
    path = vault / CANON_LOG
    if not path.is_file():
        return False
    lines = path.read_text(encoding="utf-8").splitlines()
    at = next((i + 1 for i, line in enumerate(lines) if LOG_SEPARATOR_RE.match(line.strip())), None)
    if at is None:
        return False
    lines[at:at] = rows
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return True


def mentions(vault, index, name):
    """Notas de entidades que todavía nombran `name`, con las líneas donde lo hacen."""
    found, pattern = [], re.compile(r"\[\[" + re.escape(name) + r"(?=[\]|#^\\])", re.IGNORECASE)
    for entry in index:
        if name.lower() not in (t.lower() for t in entry["enlaces"]):
            continue
        lines = [line.strip() for line in (vault / entry["path"]).read_text(encoding="utf-8").splitlines()
                 if pattern.search(line)]
        found.append((entry, lines))
    return found


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--canon", nargs="+", default=[], metavar="NOTA", help="Pasan a canon")
    parser.add_argument("--keep", nargs="+", default=[], metavar="NOTA", help="Siguen en borrador")
    parser.add_argument("--rehacer", nargs="+", default=[], metavar="NOTA", help="Se archivan para crearlas de nuevo")
    parser.add_argument("--quitar", nargs="+", default=[], metavar="NOTA", help="Se archivan y salen del mundo")
    parser.add_argument("--reason", default="", help="El motivo (para el Registro de Canon y la nota archivada)")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    today = datetime.date.today().isoformat()
    reason = args.reason.strip().rstrip(".")
    decided = [(n, "canon") for n in args.canon] + [(n, "keep") for n in args.keep] \
        + [(n, "rehacer") for n in args.rehacer] + [(n, "quitar") for n in args.quitar]
    if not decided:
        sys.exit("Error: indica al menos una decisión (--canon, --keep, --rehacer o --quitar).")
    index = load_index(vault)
    by_path = {e["path"]: e for e in index}
    notes = {}
    for name, decision in decided:
        path = resolve_note(name, vault)
        relative = path.relative_to(vault).as_posix() if path else None
        if relative not in by_path:
            sys.exit(f"Error: no encuentro la entidad '{name}' (o hay varias con ese nombre, o ya está archivada).")
        notes[(name, decision)] = (path, by_path[relative])

    out, log, chronicle = [], [], []
    # Canon y borrador revisado: solo cambian sus propiedades
    canon = [entry["name"] for (name, decision), (path, entry) in notes.items() if decision == "canon"]
    for (name, decision), (path, entry) in notes.items():
        if decision not in ("canon", "keep"):
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        end = frontmatter_end(lines)
        if decision == "canon":
            end = set_property(lines, end, "estado", "canon")
            set_property(lines, end, "ultima_revision", today)
        else:
            set_property(lines, end, "revisado", today)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    confirmed = confirm_proposals(vault, canon, today)
    for name in canon:
        entry = next(e for (n, d), (p, e) in notes.items() if e["name"] == name)
        title = entry["titulo"] or name
        extra = f", con {confirmed[name]} confirmación(es) que propuso" if confirmed.get(name) else ""
        out.append(f"Canon: {title}{extra}.")
        log.append(f"| {today} | [[{name}\\|{title}]] | Pasa a canon | {reason or DEFAULT_REASON} |")
        chronicle.append(f"[[{name}|{title}]]")
    kept = [e["titulo"] or e["name"] for (n, d), (p, e) in notes.items() if d == "keep"]
    if kept:
        out.append(f"Siguen en borrador (revisados hoy): {', '.join(kept)}.")

    # Archivar: los secretos que solo afectan a lo que se archiva van con ello
    archiving = {e["name"].lower(): d for (n, d), (p, e) in notes.items() if d in ("rehacer", "quitar")}
    for secret in index:
        targets = [t.lower() for t in secret["relaciones"].get("afecta_a", [])]
        if secret["tipo"] == SECRET_TYPE and secret["name"].lower() not in archiving and targets \
                and all(t in archiving for t in targets):
            notes[(secret["name"], "secreto")] = (vault / secret["path"], secret)
    files = {}
    if archiving:
        for file in vault.rglob("*"):
            relative = file.relative_to(vault)
            if file.is_file() and not is_hidden(relative):
                files.setdefault(file.name.lower(), file)
    images_folder, created_folder = archive_images_folder(vault) if archiving else (None, False)
    types, removed, archived = load_pending_types(vault), [], []
    for (name, decision), (path, entry) in notes.items():
        if decision not in ("rehacer", "quitar", "secreto"):
            continue
        mode = "quitar" if decision == "secreto" else decision
        if decision == "secreto":
            affected = [strip_links(t).replace("_", " ") for t in entry["relaciones"].get("afecta_a", [])]
            why = f"con lo que afectaba ({', '.join(affected)})"
        else:
            why = ("para rehacerla" if mode == "rehacer" else "al quitarla del mundo") + (f": {reason}" if reason else "")
        target, moved = archive(vault, path, mode, today, why, files, images_folder)
        title = entry["titulo"] or entry["name"]
        stem = target.stem
        archived.append((entry, decision, target, moved))
        if decision == "rehacer":
            # Sus menciones vuelven a ser enlaces pendientes, con el tipo que tenía
            types[entry["name"].lower()] = entry["tipo"]
            out.append(f"Archivada para rehacerla: {title} → {ARCHIVED_FOLDER}/{target.name}; sus menciones vuelven a "
                       f"ser enlaces pendientes de tipo {entry['tipo']}"
                       + (f"; imágenes a Anteriores: {', '.join(moved)}" if moved else "") + ".")
            log.append(f"| {today} | [[{stem}\\|{title}]] | Archivada para rehacerla | {reason or DEFAULT_REASON} |")
        elif decision == "quitar":
            removed.append(entry)
            out.append(f"Quitada del mundo: {title} → {ARCHIVED_FOLDER}/{target.name}"
                       + (f"; imágenes a Anteriores: {', '.join(moved)}" if moved else "") + ".")
            log.append(f"| {today} | [[{stem}\\|{title}]] | Quitada del mundo | {reason or DEFAULT_REASON} |")
        else:
            out.append(f"Secreto archivado con lo que afectaba: {title} → {ARCHIVED_FOLDER}/{target.name}.")
    if created_folder:
        out.append(f"AVISO: se creó la carpeta {ARCHIVE_IMAGES}: regístrala en «Carpetas añadidas por skills» de la "
                   f"Guía de Organización, como dice generar-imagen.")

    # Quitar del mundo: su zona en los mapas se retira, y sus menciones se reescriben
    if removed:
        index = load_index(vault)
        modules = load_modules()
        for entry in removed:
            for legend in legends(vault, index, modules):
                result = retire_zone(legend, entry["name"])
                if result:
                    out.append(f"Mapa: {result}.")
        out.append("")
        out.append("REESCRIBE estas menciones (lo que se quitó ya no existe en el mundo; en una nota en canon, deja "
                   "constancia en el Registro de Canon):")
        for entry in removed:
            for linker, lines in mentions(vault, index, entry["name"]):
                state = " (en canon)" if linker["estado"] == "canon" else ""
                out.append(f"- {linker['path']}{state}, por {entry['titulo'] or entry['name']}:")
                out += [f"    {line}" for line in lines[:MAX_MENTION_LINES]]
                if len(lines) > MAX_MENTION_LINES:
                    out.append(f"    … y {len(lines) - MAX_MENTION_LINES} línea(s) más")

    if not log_rows(vault, log):
        out.append(f"AVISO: no encuentro la tabla de {CANON_LOG}; las líneas no se añadieron.")
    if archiving:
        gaps, _ = find_gaps(vault, pending_types=types)
        (vault / PENDING_NOTE).write_text(build(vault, gaps, load_modules(), load_index(vault)), encoding="utf-8",
                                          newline="\n")
        out.append(f"Registro de enlaces pendientes rehecho ({len(gaps)}).")

    # Las líneas para la Bitácora, con los enlaces de la bóveda (las archivadas, a su nota archivada)
    lines_for_log = []
    if chronicle:
        lines_for_log.append(f"Pasan a canon: {', '.join(chronicle)}.")
    redo = [f"[[{t.stem}|{e['titulo'] or e['name']}]]" for e, d, t, m in archived if d == "rehacer"]
    gone = [f"[[{t.stem}|{e['titulo'] or e['name']}]]" for e, d, t, m in archived if d == "quitar"]
    if redo:
        lines_for_log.append(f"Archivadas para rehacerlas: {', '.join(redo)}.")
    if gone:
        lines_for_log.append(f"Quitadas del mundo: {', '.join(gone)}.")
    if kept:
        lines_for_log.append(f"Siguen en borrador: {len(kept)}.")
    print("\n".join(out).strip())
    if lines_for_log:
        print("\nPara la Bitácora, al terminar la tanda (log_entry.py --title \"Revisión de borradores\"):")
        print("\n".join(f"  --line \"{line}\"" for line in lines_for_log))


if __name__ == "__main__":
    main()
