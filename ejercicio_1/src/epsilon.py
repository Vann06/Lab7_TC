"""
Paso 1:
Remover producciones ε de una gramática libre de contexto.

"""
from typing import Dict, Set, Tuple, List

Symbols = Tuple[str, ...]
Grammar = Dict[str, Set[Symbols]]

def pretty_prod(body: Symbols) -> str:
    return "ε" if len(body) == 0 else "".join(body)

def pretty_grammar(G: Grammar) -> str:
    lines = []
    for A in sorted(G.keys()):
        if not G[A]:
            continue
        bodies = " | ".join(pretty_prod(b) for b in sorted(G[A]))
        lines.append(f"{A} -> {bodies}")
    return "\n".join(lines)

def find_nullable(G: Grammar, explain: bool = False) -> Set[str]:
    """
    Devuelve el conjunto de no terminales anulables (por cierre).
    Si explain=True, imprime una narración simple y ordenada.
    """
    N: Set[str] = set()
    changed, ronda = True, 0
    if explain:
        print("Paso 1) Símbolos anulables (cierre):")
    while changed:
        changed = False
        ronda += 1
        nuevos = []
        for A, prods in G.items():
            if A in N:
                continue
            for body in prods:
                # Caso directo: A -> ε
                if len(body) == 0:
                    N.add(A)
                    nuevos.append((A, "porque tiene una producción A → ε"))
                    changed = True
                    break
                # Caso por composición: A -> X1...Xk y todos Xi anulables
                if all(s.isupper() and s in N for s in body):
                    N.add(A)
                    rhs = pretty_prod(body)
                    nuevos.append((A, f"porque A → {rhs} y todos sus símbolos ya son anulables"))
                    changed = True
                    break
        if explain and nuevos:
            print(f"  • Ronda {ronda}:")
            for A, razon in nuevos:
                print(f"    - {A} pasa a ser anulable {razon}.")
    if explain:
        if N:
            print(f"  ⇒ Resultado: {', '.join(sorted(N))}\n")
        else:
            print("  ⇒ Resultado: (ninguno)\n")
    return N

def _variants_without_epsilon(body: Symbols, anulables_idx: List[int]) -> List[Symbols]:
    """
    Genera todas las variantes de 'body' quitando o dejando
    las posiciones anulables indicadas. Descarta ε (vacía).
    """
    if not anulables_idx:
        return [body]
    m = len(anulables_idx)
    generated = set()
    for mask in range(1 << m):
        kept: List[str] = []
        for i, sym in enumerate(body):
            drop = False
            if i in anulables_idx:
                j = anulables_idx.index(i)
                if (mask >> j) & 1:
                    drop = True
            if not drop:
                kept.append(sym)
        if kept:  # evitamos ε
            generated.add(tuple(kept))
    return sorted(generated)

def eliminate_epsilon(start: str, G: Grammar, show_steps: bool = True) -> Grammar:
    if show_steps:
        print("=== Gramática original ===")
        print(pretty_grammar(G), "\n")

    # 1) Anulables con narración
    N = find_nullable(G, explain=show_steps)

    # 2) Generación de nuevas producciones sin ε
    if show_steps:
        print("Paso 2) Generar producciones sin ε:")
    newG: Grammar = {A: set() for A in G.keys()}

    for A, prods in G.items():
        for body in prods:
            if len(body) == 0:
                # Se elimina explícitamente A -> ε
                if show_steps:
                    print(f"  • {A} -> ε  (se elimina)")
                continue

            # posiciones anulables dentro del cuerpo
            idxs = [i for i, s in enumerate(body) if s.isupper() and s in N]
            rhs = pretty_prod(body)

            if show_steps:
                if idxs:
                    pos = ", ".join(str(i) for i in idxs)
                    print(f"  • {A} -> {rhs}: símbolos anulables en posiciones [{pos}]")
                else:
                    print(f"  • {A} -> {rhs}: no contiene símbolos anulables")

            variants = _variants_without_epsilon(body, idxs)
            for v in variants:
                newG[A].add(v)
                if show_steps:
                    print(f"      - Mantener/Eliminar → {A} -> {pretty_prod(v)}")

    # Limpieza: quitar no terminales sin producciones
    newG = {A: prods for A, prods in newG.items() if prods}

    if show_steps:
        print("\n=== Gramática sin ε ===")
        print(pretty_grammar(newG), "\n")

    return newG
