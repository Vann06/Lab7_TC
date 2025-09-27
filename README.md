# Laboratorio 7 - Teoría de Computación
## Simplificación de Gramáticas Libres de Contexto

[![Video](https://img.shields.io/badge/📹_Video-Explicativo-red?style=for-the-badge&logo=youtube)](https://youtu.be/rMoZeCjakys)

### 📋 Descripción

Este proyecto implementa algoritmos fundamentales para la **simplificación de gramáticas libres de contexto**, específicamente la **eliminación de producciones épsilon (ε)**. Es una herramienta educativa que demuestra conceptos clave de la teoría de lenguajes formales y compiladores.

### 🎯 Objetivos

- ✅ Cargar y validar gramáticas libres de contexto desde archivos de texto
- ✅ Identificar símbolos anulables (que pueden generar ε)
- ✅ Eliminar producciones épsilon manteniendo la equivalencia del lenguaje
- ✅ Mostrar el proceso paso a paso para fines educativos

---

## 🏗️ Estructura del Proyecto

```
Lab7_TC/
├── ejercicio_1/
│   ├── grammars/           # Archivos de gramáticas de prueba
│   │   ├── g1.txt
│   │   ├── g2.txt
│   │   └── g3.txt
│   └── src/                # Código fuente
│       ├── main.py         # Programa principal
│       ├── epsilon.py      # Algoritmo de eliminación de ε
│       └── validator.py    # Validación de gramáticas
└── ejercicio_2/
    └── Laboratorio_7_TC-1.pdf
```

---

## 🚀 Cómo Ejecutar

### Prerrequisitos
- Python 3.7 o superior
- Sistema operativo: Windows, macOS, o Linux

### Ejecución Rápida

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Vann06/Lab7_TC.git
   cd Lab7_TC
   ```

2. **Ejecutar el programa:**
   ```bash
   # Desde la raíz del proyecto
   python ejercicio_1/src/main.py
   
   # O desde dentro de ejercicio_1
   cd ejercicio_1
   python src/main.py
   ```

3. **Seguir las instrucciones interactivas:**
   - Elegir una gramática (1, 2, o 3)
   - Decidir si mostrar pasos detallados (s/n)

### Ejemplo de Uso

```
========================================
   Lab 7 — Ejercicio 1
   Carga, validación y eliminación de ε
========================================

Gramáticas disponibles:
  1) g1.txt
  2) g2.txt
  3) g3.txt

Elige el número del archivo: 1
¿Mostrar pasos del algoritmo? (s/n): s

Archivo elegido: g1.txt

=== Gramática original ===
S -> AB | ε
A -> a | ε
B -> b

Símbolos anulables: A, S

Paso 2) Generar producciones sin ε:
  • S -> ε  (se elimina)
  • S -> AB: símbolos anulables en posiciones [0]
      - Mantener/Eliminar → S -> AB
      - Mantener/Eliminar → S -> B
  • A -> ε  (se elimina)
  • A -> a: no contiene símbolos anulables
      - Mantener/Eliminar → A -> a
  • B -> b: no contiene símbolos anulables
      - Mantener/Eliminar → B -> b

=== Resultado final (sin ε) ===
A -> a
B -> b
S -> AB | B

Proceso completado.
```

---

## 📝 Formato de Gramáticas

Los archivos de gramática deben seguir este formato:

```
# Comentarios empiezan con #
S -> AB | ε
A -> a | ε  
B -> b | cB
```

### Reglas de Formato:
- **No terminal:** Una letra mayúscula (A-Z)
- **Flecha:** `->` o `→`
- **Alternativas:** Separadas por `|`
- **Épsilon:** Usar `ε`
- **Comentarios:** Líneas que empiezan con `#`
- **El primer símbolo** del archivo es el símbolo inicial

---

## 🧠 Algoritmo Implementado

### 1. **Identificación de Símbolos Anulables**
```python
def find_nullable(G: Grammar) -> Set[str]:
    # Algoritmo de punto fijo por rondas
    # Encuentra todos los símbolos que pueden generar ε
```

**Proceso:**
- **Ronda 1:** Símbolos con producción directa a ε
- **Ronda 2:** Símbolos cuyas producciones solo usan símbolos ya anulables
- **Repetir** hasta que no haya cambios

### 2. **Eliminación de Producciones ε**
```python
def eliminate_epsilon(start: str, G: Grammar) -> Grammar:
    # Genera todas las variantes sin ε
    # Mantiene equivalencia del lenguaje
```

**Proceso:**
- Eliminar producciones `A -> ε`
- Para cada producción con símbolos anulables, generar todas las variantes
- Ejemplo: `S -> AB` con A anulable → `S -> AB | B`

### 3. **Generación de Variantes**
```python
def _variants_without_epsilon(body: Symbols, anulables_idx: List[int]) -> List[Symbols]:
    # Usa máscaras binarias para generar todas las combinaciones
```

**Ejemplo:**
- Producción: `S -> ABC`
- Anulables: A, C (posiciones 0, 2)
- Variantes generadas: `ABC`, `AB`, `BC`, `B`

---

## 🎥 Video Explicativo

[![Mira el video explicativo](https://img.youtube.com/vi/rMoZeCjakys/maxresdefault.jpg)](https://youtu.be/rMoZeCjakys)

**[Ver Video Completo en YouTube](https://youtu.be/rMoZeCjakys)**

El video incluye:
- 📚 Explicación teórica de gramáticas libres de contexto
- 🔧 Demostración práctica del programa
- 📊 Análisis paso a paso del algoritmo
- 💡 Ejemplos con gramáticas reales

---

## 📚 Fundamentos Teóricos

### ¿Qué es una Producción Épsilon?
Una producción de la forma `A -> ε` donde un no terminal deriva directamente en la cadena vacía.

### ¿Por qué Eliminar ε?
1. **Simplifica el análisis sintáctico**
2. **Reduce ambigüedades** en la gramática
3. **Prepara para otros algoritmos** (como la eliminación de recursión izquierda)
4. **Mantiene equivalencia** del lenguaje generado

### Ejemplo de Transformación:
```
ANTES:                    DESPUÉS:
S -> AB | ε              S -> AB | A | B
A -> a | ε        →      A -> a
B -> b | ε               B -> b
```

**Resultado:** Mismo lenguaje, sin producciones ε.

---

## 🧪 Casos de Prueba

### `g1.txt` - Caso Básico
```
S -> AB | ε
A -> a | ε
B -> b
```

### `g2.txt` - Caso Complejo
```
S -> AB
A -> aA | ε
B -> bB | ε
```

### `g3.txt` - Caso Avanzado
```
S -> AB | C
A -> aA | ε
B -> bB | cC
C -> ε
```

---

## 🛠️ Arquitectura del Código

### `main.py` - Coordinador Principal
- `load_and_validate()`: Carga y valida gramáticas
- `pick_file_interactive()`: Interfaz de selección
- `main()`: Orquesta todo el proceso

### `validator.py` - Validación de Entrada
- `validate_line()`: Verifica formato de producciones
- `parse_line()`: Convierte texto a formato interno

### `epsilon.py` - Algoritmo Core
- `find_nullable()`: Identifica símbolos anulables
- `eliminate_epsilon()`: Algoritmo principal
- `_variants_without_epsilon()`: Generador de combinaciones

---

## 🤝 Contribuciones

¿Quieres contribuir? ¡Genial!

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

### Ideas para Contribuir:
- 🆕 Más casos de prueba
- 🎨 Interfaz gráfica
- 📊 Visualización del algoritmo
- 🧪 Tests unitarios
- 📖 Más documentación

---

## 📋 Requisitos Técnicos

- **Python:** 3.7+
- **Librerías:** Solo librerías estándar (typing, pathlib, sys, re)
- **Encoding:** UTF-8 para caracteres especiales (ε)
- **OS:** Multiplataforma (Windows, macOS, Linux)

---

## 📄 Licencia

Este proyecto es de uso educativo para el curso de Teoría de Computación.

---

## 👥 Autor

**Vianka** - [@Vann06](https://github.com/Vann06)

---

## 🔗 Enlaces Útiles

- 📹 **[Video Explicativo](https://youtu.be/rMoZeCjakys)**
- 📚 **[Teoría de Lenguajes Formales](https://es.wikipedia.org/wiki/Lenguaje_formal)**
- 🎓 **[Gramáticas Libres de Contexto](https://es.wikipedia.org/wiki/Gram%C3%A1tica_libre_de_contexto)**

---

⭐ **¡Si te sirvió este proyecto, dale una estrella!** ⭐