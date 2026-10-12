#!/usr/bin/env python3
"""Tira dados con azar real (no "imaginado" por el modelo).

Ejemplos:  roll_dice.py 1d4      roll_dice.py 2d6+1      roll_dice.py 1d100 --seed 42
Imprime el total en la primera línea y el detalle en la segunda."""
import argparse
import random
import re
import sys

DICE_RE = re.compile(r"^(\d*)d(\d+)([+-]\d+)?$")


def main():
    # UTF-8 antes de cualquier salida (incluida la ayuda de argparse)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dice", help="Notación NdM[+K], por ejemplo 1d4, 2d6+1, 1d100")
    parser.add_argument("--seed", type=int, help="Semilla para repetir una tirada")
    args = parser.parse_args()

    match = DICE_RE.match(args.dice.strip().lower())
    if not match:
        sys.exit(f"Error: '{args.dice}' no es una tirada válida (usa NdM o NdM+K).")
    count = int(match.group(1) or 1)
    sides = int(match.group(2))
    modifier = int(match.group(3) or 0)
    if not (1 <= count <= 100 and 2 <= sides <= 1000):
        sys.exit("Error: entre 1 y 100 dados, de 2 a 1000 caras.")

    # Con semilla la tirada es reproducible; sin ella se usa el azar del sistema
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    rolls = [rng.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + modifier
    print(total)
    print(f"{args.dice} = {rolls}{f' {modifier:+d}' if modifier else ''} = {total}")


if __name__ == "__main__":
    main()
