#!/usr/bin/env python3
"""Cola de revisión: los borradores del mundo en tandas, de lo que más pesa a lo que menos, con una ficha
corta de cada uno para decidir si pasa a canon, sigue en borrador, se archiva para rehacerlo o se quita
del mundo.

- Peso: relevancia × 2 + las notas de entidades que lo enlazan. A igual peso, el más antiguo.
- Cada secreto va detrás de la primera entidad a la que afecta, si está en la cola.
- Los que ya se revisaron y siguen en borrador (`revisado`) van al final, del revisado hace más tiempo
  al más reciente.

Cada ficha: tipo, relevancia, origen y fecha; su resumen; quién la enlaza (y cuántas de esas notas
están en canon); lo que propuso y espera confirmación en Preguntas Abiertas (se confirma si pasa a
canon); sus secretos; su imagen y su mapa; los enlaces pendientes que solo nombra ella (si se quita,
desaparecen) y los avisos del auditor sobre ella. Los enlaces van en Markdown, con la ruta del archivo,
para mostrarlos en el chat.

Ejemplos:  review_queue.py                    (la tanda siguiente, de 8)
           review_queue.py --limit 4 --type personaje
           review_queue.py --origin procedural
           review_queue.py --skip Aldric_Voss --skip Puerto_Gris"""
import argparse
import os
import re
import sys
from pathlib import Path

# La lógica común vive en los scripts de crear-entidad
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "crear-entidad" / "scripts"))
from audit_world import run_audit  # noqa: E402
from vault_lib import (OPEN_QUESTIONS, SECRET_TYPE, find_gaps, first, is_confirmation, load_index,  # noqa: E402
                       strip_links)
from vault_lib import vault_path  # noqa: E402

DEFAULT_LIMIT = 8
MAX_LINKERS = 4
MAX_OWN_LINKS = 5
PROPOSED_RE = re.compile(r"propuesto al crear \[\[([^\]|#^\\]+)", re.IGNORECASE)


def md_link(vault, relative, text):
    """Enlace Markdown a un archivo de la bóveda, relativo al directorio de trabajo (se abre con un clic)."""
    target = Path(os.path.relpath(vault / relative, Path.cwd())).as_posix()
    return f"[{text}]({target.replace(' ', '%20')})"


def proposals(vault):
    """{nota en minúsculas: [confirmaciones pendientes que propuso al crearse]}."""
    path = vault / OPEN_QUESTIONS
    found = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            match = PROPOSED_RE.search(line) if is_confirmation(line) else None
            if match:
                text = strip_links(line.strip()[len("- [ ]"):].strip())
                found.setdefault(match.group(1).strip().lower(), []).append(text)
    return found


def order(drafts, weight):
    """Los borradores en orden de revisión: los no revisados por peso (y antigüedad), cada secreto detrás de la
    primera entidad a la que afecta; al final, los ya revisados que siguen en borrador."""
    secrets = [e for e in drafts if e["tipo"] == SECRET_TYPE]
    entities = [e for e in drafts if e["tipo"] != SECRET_TYPE]
    fresh = sorted((e for e in entities if not e["revisado"]), key=lambda e: (-weight(e), e["fecha"]))
    seen = sorted((e for e in entities if e["revisado"]), key=lambda e: e["revisado"])
    queue, placed = [], set()
    for entry in fresh + seen:
        queue.append(entry)
        for secret in secrets:
            targets = [t.lower() for t in secret["relaciones"].get("afecta_a", [])]
            if secret["name"] not in placed and entry["name"].lower() in targets[:1]:
                queue.append(secret)
                placed.add(secret["name"])
    loose = sorted((s for s in secrets if s["name"] not in placed), key=lambda e: (-weight(e), e["fecha"]))
    return queue + loose


def card(vault, number, entry, data):
    """La ficha de un borrador, en líneas."""
    name, key = entry["name"], entry["name"].lower()
    title = entry["titulo"] or name.replace("_", " ")
    origin = "del motor" if entry["origen"] == "procedural" else "a mano"
    head = (f"{number}. {md_link(vault, entry['path'], title)} · {entry['tipo']} · relevancia "
            f"{entry['relevancia'] if entry['relevancia'] is not None else '?'} · {origin} · {entry['fecha'] or 'sin fecha'}"
            + (f" · revisado el {entry['revisado']}, sigue en borrador" if entry["revisado"] else ""))
    lines = [head]
    if entry["resumen"]:
        lines.append(f"   {strip_links(entry['resumen'])}")
    linkers = data["linkers"].get(key, [])
    canon = [e for e in linkers if e["estado"] == "canon"]
    if entry["tipo"] == SECRET_TYPE:
        affects = [strip_links(t).replace("_", " ") for t in entry["relaciones"].get("afecta_a", [])]
        lines.append(f"   🔒 Secreto: afecta a {', '.join(affects) or 'nada todavía'}. Nadie lo enlaza; archivarlo, de "
                     f"cualquiera de las dos formas, solo lo aparta")
    else:
        shown = ", ".join(md_link(vault, e["path"], e["titulo"] or e["name"]) for e in linkers[:MAX_LINKERS])
        lines.append(f"   Enlazada desde {len(linkers)} nota(s)" + (f" ({len(canon)} en canon)" if canon else "")
                     + (f": {shown}" + (" …" if len(linkers) > MAX_LINKERS else "") if linkers else ""))
    image = first(entry["props"].get("imagen"))
    edition = first(entry["props"].get("mapa_edicion"))
    lines.append(f"   Imagen: {'sí' if image else 'no'}" + (f" · Mapa: edición {edition}" if edition else ""))
    for text in data["proposals"].get(key, []):
        lines.append(f"   Propuso (se confirma si pasa a canon): {text}")
    for secret in data["secrets"].get(key, []):
        lines.append(f"   🔒 Su secreto: {md_link(vault, secret['path'], secret['titulo'] or secret['name'])}"
                     f" ({secret['estado']})")
    own = data["own_links"].get(entry["path"], [])
    if own:
        names = ", ".join(link.replace("_", " ") for link in own[:MAX_OWN_LINKS])
        lines.append(f"   Enlaces pendientes que solo nombra ella: {len(own)} ({names}"
                     + (" …" if len(own) > MAX_OWN_LINKS else "") + "); si se quita del mundo, desaparecen")
    for warning in data["warnings"].get(key, []):
        lines.append(f"   AVISO: {strip_links(warning)}")
    return lines


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", default="World_Building", help="Carpeta de la bóveda (por defecto World_Building)")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Borradores por tanda ({DEFAULT_LIMIT})")
    parser.add_argument("--type", help="Solo los de un tipo")
    parser.add_argument("--origin", choices=("procedural", "manual"), help="Solo los del motor o solo los hechos a mano")
    parser.add_argument("--skip", action="append", default=[], metavar="NOTA",
                        help="Un borrador que no debe salir en esta tanda (repetible)")
    args = parser.parse_args()

    vault = vault_path(args.vault)
    if not vault.is_dir():
        sys.exit(f"Error: no existe la bóveda '{vault}'.")
    index = load_index(vault)
    for entry in index:
        entry["fecha"] = str(first(entry["props"].get("ultima_revision")) or "")
        entry["revisado"] = str(first(entry["props"].get("revisado")) or "")
    linkers = {}
    for entry in index:
        for target in entry["enlaces"]:
            if target.lower() != entry["name"].lower():
                linkers.setdefault(target.lower(), []).append(entry)
    secrets = {}
    for entry in index:
        if entry["tipo"] == SECRET_TYPE:
            for target in entry["relaciones"].get("afecta_a", []):
                secrets.setdefault(target.lower(), []).append(entry)
    gaps, _ = find_gaps(vault)
    own_links = {}
    for gap in gaps:
        if len(gap["notes"]) == 1:
            own_links.setdefault(gap["notes"][0], []).append(gap["link"])
    audit = run_audit(vault)
    warnings = {}
    for warning in audit["avisos"] + audit["errores"]:
        for name in re.findall(r"\[\[([^\]|#^\\]+)", warning)[:1]:
            warnings.setdefault(name.strip().lower(), []).append(warning)
    data = {"linkers": linkers, "secrets": secrets, "own_links": own_links, "warnings": warnings,
            "proposals": proposals(vault)}

    skipped = {name.strip().strip("[]").lower() for name in args.skip}
    drafts = [e for e in index if e["estado"] == "borrador" and e["name"].lower() not in skipped
              and (not args.type or e["tipo"] == args.type) and (not args.origin or e["origen"] == args.origin)]
    queue = order(drafts, lambda e: 2 * (e["relevancia"] or 0) + len(linkers.get(e["name"].lower(), [])))
    batch = queue[:max(args.limit, 1)]

    all_drafts = [e for e in index if e["estado"] == "borrador"]
    procedural = sum(1 for e in all_drafts if e["origen"] == "procedural")
    reviewed = sum(1 for e in all_drafts if e["revisado"])
    print(f"Borradores: {len(all_drafts)} ({procedural} del motor, {len(all_drafts) - procedural} a mano"
          + (f"; {reviewed} ya {'revisado que sigue' if reviewed == 1 else 'revisados que siguen'} en borrador"
             if reviewed else "") + ")"
          + f" · en canon: {sum(1 for e in index if e['estado'] == 'canon')}")
    if not batch:
        print("No hay borradores que revisar" + (" con ese filtro." if args.type or args.origin or skipped else "."))
        return
    print(f"Esta tanda: {len(batch)} · quedan después: {len(queue) - len(batch)}")
    for number, entry in enumerate(batch, 1):
        print()
        print("\n".join(card(vault, number, entry, data)))


if __name__ == "__main__":
    main()
