# -*- coding: utf-8 -*-
"""
Ejercicio 1 - Laboratorio 7
Carga, validación y eliminación de producciones ε
"""

from typing import Dict, Set, Tuple
from pathlib import Path
import sys

from validator import validate_line, parse_line
from epsilon import find_nullable, eliminate_epsilon, pretty_grammar

Symbols = Tuple[str, ...]
Grammar = Dict[str, Set[Symbols]]

def load_and_validate(path: Path) -> Tuple[str, Grammar]:
    """Lee archivo, valida cada línea y construye la gramática interna.
       Retorna (símbolo inicial, gramática)"""
    G: Grammar = {}
    start = None
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            validate_line(line, i)
            lhs, alts = parse_line(line)
            if start is None:
                start = lhs
            G.setdefault(lhs, set()).update(alts)
    if start is None:
        raise ValueError("El archivo no contiene producciones válidas.")
    return start, G

def pick_file_interactive(grams_dir: Path) -> Path:
    files = sorted([p for p in grams_dir.glob("*.txt") if p.is_file()])
    if not files:
        raise FileNotFoundError(f"No se encontraron .txt en {grams_dir}")

    print("\nGramáticas disponibles:")
    for idx, p in enumerate(files, start=1):
        print(f"  {idx}) {p.name}")

    while True:
        choice = input("\nElige el número del archivo: ").strip()
        if not choice.isdigit():
            print("  → Ingresa un número válido.")
            continue
        i = int(choice)
        if 1 <= i <= len(files):
            return files[i - 1]
        print(f"  → Debe estar entre 1 y {len(files)}.")

def ask_show_steps() -> bool:
    while True:
        ans = input("¿Mostrar pasos del algoritmo? (s/n): ").strip().lower()
        if ans in ("s", "si", "sí"):
            return True
        if ans in ("n", "no"):
            return False
        print("  → Responde 's' o 'n'.")

def main():
    grams_dir = Path(__file__).resolve().parents[1] / "grammars"

    print("========================================")
    print("   Lab 7 — Ejercicio 1")
    print("   Carga, validación y eliminación de ε")
    print("========================================")

    try:
        file_path = pick_file_interactive(grams_dir)
        show_steps = ask_show_steps()

        print(f"\nArchivo elegido: {file_path.name}\n")
        start, G = load_and_validate(file_path)

        # Mostrar anulables por claridad (opcionales)
        N = find_nullable(G)
        print("Símbolos anulables:", ", ".join(sorted(N)) if N else "(ninguno)", "\n")

        newG = eliminate_epsilon(start, G, show_steps=show_steps)

        print("=== Resultado final (sin ε) ===")
        print(pretty_grammar(newG))
        print("\nProceso completado.\n")

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
