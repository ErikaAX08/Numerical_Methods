import numpy as np
import copy
from fractions import Fraction


def format_number(num):
    """Format number for display, keeping fractions for exact representation"""
    # Para valores muy cercanos a cero, mostrar 0
    if abs(num) < 1e-10:
        return "0"

    # Intentar representar como fracción para precisión exacta
    frac = Fraction(num).limit_denominator(1000)
    if frac.denominator == 1:
        return str(frac.numerator)
    elif abs(num - float(frac)) < 1e-10:
        if frac.numerator < 0:
            return f"-\\frac{{{abs(frac.numerator)}}}{{{frac.denominator}}}"
        else:
            return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"
    else:
        # Formatear como decimal con precisión limitada
        return f"{num:.6g}"


def matrix_to_latex(matrix, augmented=True):
    """Convert a matrix to LaTeX format"""
    rows, cols = len(matrix), len(matrix[0])

    if augmented and cols > 1:
        # Determinar la posición de la línea vertical (último término independiente)
        bar_pos = cols - 1

        latex = "\\begin{pmatrix}\n"  # Cambiar a pmatrix en lugar de bmatrix
        for i in range(rows):
            row_str = ""
            for j in range(cols):
                num_str = format_number(matrix[i][j])
                row_str += num_str
                if j < cols - 1:
                    if j == bar_pos - 1:
                        row_str += " & | & "  # Simplificar la separación de columnas
                    else:
                        row_str += " & "
            if i < rows - 1:
                row_str += " \\\\\n"
            latex += row_str
        latex += "\n\\end{pmatrix}"
    else:
        latex = "\\begin{pmatrix}\n"  # Cambiar a pmatrix
        for i in range(rows):
            row_str = ""
            for j in range(cols):
                num_str = format_number(matrix[i][j])
                row_str += num_str
                if j < cols - 1:
                    row_str += " & "
            if i < rows - 1:
                row_str += " \\\\\n"
            latex += row_str
        latex += "\n\\end{pmatrix}"

    return latex


def gauss_column_scaled_pivoting_method(matrix):
    """
    Implementación del algoritmo de eliminación gaussiana con pivoteo escalado de columna

    Args:
        matrix: La matriz aumentada del sistema de ecuaciones

    Returns:
        dict: Un diccionario conteniendo la solución y los pasos del proceso
    """
    # Convertir a lista de listas para manipulación más sencilla
    if isinstance(matrix, np.ndarray):
        matrix = matrix.tolist()

    # Hacer una copia para manipular
    A = copy.deepcopy(matrix)

    rows = len(A)
    cols = len(A[0])
    n = cols - 1  # Número de variables

    # Verificar si la matriz es consistente con el número esperado de variables
    if rows > n:
        return {"error": "El sistema tiene más ecuaciones que variables"}

    # Inicializar registro de pasos
    steps = []
    steps.append({
        "description": "Matriz original",
        "matrix": matrix_to_latex(A)
    })

    # Vector para tracking de los intercambios de filas (necesario para ordenar la solución final)
    row_tracker = list(range(rows))

    # Encontrar los factores de escala para cada fila
    s = []
    for i in range(rows):
        max_abs_val = max([abs(A[i][j]) for j in range(n)])
        if max_abs_val == 0:
            return {"error": "La matriz tiene una fila de ceros, el sistema no tiene solución única"}
        s.append(max_abs_val)

    steps.append({
        "description": "Factores de escala calculados",
        "details": f"s = [{', '.join([format_number(val) for val in s])}]"
    })

    # Eliminación hacia adelante (Forward Elimination)
    for k in range(n - 1):
        # Encontrar el pivote usando pivoteo escalado por columna
        pivot_row = k
        max_ratio = -1

        for i in range(k, rows):
            if s[i] == 0:
                continue
            ratio = abs(A[i][k] / s[i])
            if ratio > max_ratio:
                max_ratio = ratio
                pivot_row = i

        # Verificar si el pivote es cero (puede indicar un sistema singular)
        if abs(A[pivot_row][k]) < 1e-10:
            continue

        # Intercambiar filas si es necesario
        if pivot_row != k:
            A[k], A[pivot_row] = A[pivot_row], A[k]
            s[k], s[pivot_row] = s[pivot_row], s[k]
            row_tracker[k], row_tracker[pivot_row] = row_tracker[pivot_row], row_tracker[k]

            steps.append({
                "description": f"Intercambio de filas {pivot_row + 1} y {k + 1}",
                "matrix": matrix_to_latex(A)
            })

        # Eliminación
        for i in range(k + 1, rows):
            factor = A[i][k] / A[k][k]

            if abs(factor) > 1e-10:  # Solo registrar operaciones significativas
                description = f"Restar {format_number(factor)} veces la fila {k + 1} de la fila {i + 1}"

                A[i][k] = 0  # Exactamente cero para evitar errores de redondeo
                for j in range(k + 1, cols):
                    A[i][j] -= factor * A[k][j]

                steps.append({
                    "description": description,
                    "matrix": matrix_to_latex(A)
                })

    # Verificar si es un sistema de rango completo
    for i in range(min(rows, n)):
        if abs(A[i][i]) < 1e-10:
            return {
                "error": "El sistema no tiene solución única (matriz singular)",
                "process_steps": steps
            }

    # Sustitución hacia atrás (Back Substitution)
    solution = [0] * n
    back_steps = []

    for i in range(min(rows, n) - 1, -1, -1):
        # Ecuación original
        original_eq = f"\\text{{Fila}}: {i + 1}, \\text{{Ecuación}}: "
        eq_terms = []

        for j in range(n):
            if abs(A[i][j]) > 1e-10:
                coef = format_number(A[i][j])
                if j > 0 and A[i][j] > 0:
                    eq_terms.append(f"+{coef}x_{j + 1}")
                else:
                    eq_terms.append(f"{coef}x_{j + 1}")

        original_eq += " ".join(eq_terms) + f" = {format_number(A[i][n])}"

        # Preparar el despeje
        sum_val = 0
        sum_terms = []
        for j in range(i + 1, n):
            if abs(A[i][j]) > 1e-10:
                sum_val += A[i][j] * solution[j]
                sum_terms.append(f"{format_number(A[i][j])} \\cdot {format_number(solution[j])}")

        # Calcular la solución
        solution[i] = (A[i][n] - sum_val) / A[i][i]

        # Mostrar paso a paso el despeje
        despeje = [
            f"\\text{{Ecuación original}}: {original_eq}",
            f"\\text{{Despejando}} x_{i + 1}:"
        ]

        # Si hay términos para sustituir
        if sum_terms:
            despeje.append(f"{format_number(A[i][i])}x_{i + 1} = {format_number(A[i][n])} - ({' + '.join(sum_terms)})")
            despeje.append(f"{format_number(A[i][i])}x_{i + 1} = {format_number(A[i][n] - sum_val)}")
            despeje.append(f"x_{i + 1} = \\frac{{{format_number(A[i][n] - sum_val)}}}{{{format_number(A[i][i])}}}")
        else:
            despeje.append(f"{format_number(A[i][i])}x_{i + 1} = {format_number(A[i][n])}")
            despeje.append(f"x_{i + 1} = \\frac{{{format_number(A[i][n])}}}{{{format_number(A[i][i])}}}")

        despeje.append(f"x_{i + 1} = {format_number(solution[i])}")

        back_steps.append({
            "description": f"Calculando x_{i + 1} por sustitución hacia atrás",
            "equation": " \\\\ ".join(despeje)  # Usar múltiples líneas para mostrar el proceso
        })

    # Agregar los pasos de sustitución hacia atrás a los pasos generales
    steps.extend(back_steps)

    # Formatear la solución final
    formatted_solution = {f"x_{i + 1}": format_number(solution[i]) for i in range(n)}

    return {
        "solution": formatted_solution,
        "process_steps": steps
    }
