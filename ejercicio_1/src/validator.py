# Validación de datos de entrada 
# Detiene la ejecucción si los datos no son correctos
import re

_ARROW = r'(?:->|→)'   # una sola cadena regex que dice: o '->' o '→'
_RHS_ATOM = r'(?:[A-Za-z0-9]+|ε|ϵ|eps|epsilon)'  # o palabra, o epsilon
_RHS = rf'(?:{_RHS_ATOM}(?:\s*\|\s*{_RHS_ATOM})*)' # uno o más átomos separados por '|'
PRODUCTION_RE = re.compile(
    rf'^\s*([A-Z])\s*{_ARROW}\s*({_RHS})\s*$'
)

EPS_TOKENS = {"ε"}

def validate_line(line: str, lineno: int) -> None:
    stripped_line = line.strip()
    if stripped_line == "" or stripped_line.startswith("#"):
        return
    if not PRODUCTION_RE.match(stripped_line):
        raise ValueError(f"Línea {lineno}: La línea no es una producción válida.")


# Parsea una línea ya validada y devuelve (no_terminal, [alternativas])
def parse_line(line: str):
    match = PRODUCTION_RE.match(line.strip())
    if not match:
        raise ValueError("Línea no válida")
    lhs = match.group(1) # parte izquierda - no terminal
    rhs = match.group(2) # parte derecha de la producción

    alternatives = []
    for alt in (a.strip() for a in rhs.split("|")):
        if alt in EPS_TOKENS:
            alternatives.append(tuple()) #tupla vacía para epsilon
        else:
            #tupla de caracteres una por simbolo
            alternatives.append(tuple(ch for ch in alt))
    return lhs, alternatives