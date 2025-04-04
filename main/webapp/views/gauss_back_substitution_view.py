from django.shortcuts import render
from django.http import JsonResponse
import json


def gauss_back_substitution(request):
    return render(request, 'gauss_back_substitution.html')


def calculate_gauss_back_substitution_view(request):
    if request.method == "POST":
        try:
            print("Start calculating gauss back substitution...")

            # Cargar los datos desde la petición
            data = json.loads(request.body.decode("utf-8"))
            print("Received data:", data)

            # Verificar que los datos sean correctos
            if "matrix" not in data or "vector" not in data:
                return JsonResponse({'error': 'Missing required fields: matrix and vector'}, status=400)

            # Obtener matriz y vector del JSON recibido
            matrix = data["matrix"]
            vector = data["vector"]

            # Validar dimensiones
            if len(matrix) != len(vector):
                return JsonResponse({'error': 'Matrix and vector dimensions do not match'}, status=400)

            for row in matrix:
                if len(row) != len(matrix):
                    return JsonResponse({'error': 'Matrix must be square'}, status=400)

            # Ejecutar el método de eliminación gaussiana con sustitución hacia atrás
            result = gauss_elimination_with_back_substitution(matrix, vector)

            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as error:
            print("Error:", error)
            return JsonResponse({'error': str(error)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def gauss_elimination_with_back_substitution(matrix, vector):
    n = len(matrix)
    augmented_matrix = []
    steps = []

    for i in range(n):
        row = matrix[i].copy()
        row.append(vector[i])
        augmented_matrix.append(row)

    steps.append({
        "step": "Initial augmented matrix",
        "matrix": [row.copy() for row in augmented_matrix]
    })

    # Eliminación hacia adelante
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(augmented_matrix[k][i]) > abs(augmented_matrix[max_row][i]):
                max_row = k

        if abs(augmented_matrix[max_row][i]) < 1e-10:
            continue

        if max_row != i:
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            steps.append({
                "step": f"Swap row {i+1} with row {max_row+1}",
                "matrix": [row.copy() for row in augmented_matrix]
            })

        pivot = augmented_matrix[i][i]
        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot

        steps.append({
            "step": f"Scale row {i+1} by 1/{pivot}",
            "matrix": [row.copy() for row in augmented_matrix]
        })

        for k in range(i + 1, n):
            factor = augmented_matrix[k][i]
            for j in range(i, n + 1):
                augmented_matrix[k][j] -= factor * augmented_matrix[i][j]

            steps.append({
                "step": f"Eliminate below pivot in row {k+1} using row {i+1} (factor: {factor})",
                "matrix": [row.copy() for row in augmented_matrix]
            })

        steps.append({
            "step": f"Completion of elimination below pivot in column {i+1}",
            "matrix": [row.copy() for row in augmented_matrix]
        })

    # Analizar si el sistema tiene solución única, infinitas soluciones o es inconsistente

    # Detectar inconsistencia (ninguna solución)
    inconsistent_rows = []
    for i, row in enumerate(augmented_matrix):
        if all(abs(cell) < 1e-10 for cell in row[:-1]) and abs(row[-1]) > 1e-10:
            inconsistent_rows.append({
                "row_index": i + 1,
                "row_values": row.copy()
            })

    if inconsistent_rows:
        steps.append({
            "step": "Inconsistent system detected (no solution)",
            "matrix": [r.copy() for r in augmented_matrix],
            "inconsistent_rows": inconsistent_rows
        })

        # Explicación detallada de la inconsistencia
        explanation = []
        for row_info in inconsistent_rows:
            explanation.append(
                f"Row {row_info['row_index']} suggests 0 = {row_info['row_values'][-1]}, which is impossible.")

        return {
            "status": "no_solution",
            "message": "El sistema no tiene solución (sistema inconsistente)",
            "process_steps": steps,
            "details": {
                "explanation": explanation,
                "inconsistent_rows": inconsistent_rows
            }
        }

    # Detectar infinitas soluciones
    zero_rows = []
    non_zero_rows = []

    # Identificar filas que son todas ceros y las que tienen elementos no cero
    for i, row in enumerate(augmented_matrix):
        if all(abs(cell) < 1e-10 for cell in row[:-1]):
            zero_rows.append(i)
        else:
            non_zero_rows.append(i)

    # Calcular el rango como el número de filas no cero
    rank = len(non_zero_rows)

    # Si el rango es menor que n, el sistema tiene infinitas soluciones
    if rank < n:
        # Identificar variables libres (columnas sin pivote)
        free_variables = []
        for j in range(n):
            # Verificar si hay alguna fila donde esta columna es el pivote
            is_pivot_column = False
            for i in non_zero_rows:
                # Si es la primera entrada no cero en esta fila
                if abs(augmented_matrix[i][j]) > 1e-10 and all(abs(augmented_matrix[i][k]) < 1e-10 for k in range(j)):
                    is_pivot_column = True
                    break

            if not is_pivot_column:
                free_variables.append(j + 1)  # La variable j+1 es libre

        steps.append({
            "step": "System has infinite solutions (underdetermined)",
            "matrix": [r.copy() for r in augmented_matrix],
            "rank": rank,
            "free_variables": free_variables
        })

        # Construir una descripción simple de la solución paramétrica
        parametric_description = f"El sistema tiene rango {rank} con {n} variables, lo que resulta en {n - rank} variables libres."

        return {
            "status": "infinite_solutions",
            "message": "El sistema tiene infinitas soluciones (compatible indeterminado)",
            "process_steps": steps,
            "details": {
                "rank": rank,
                "variables": n,
                "free_variables": free_variables,
                "description": parametric_description
            }
        }

    # Sustitución hacia atrás para un sistema con solución única
    for i in range(n-1, -1, -1):
        for k in range(i-1, -1, -1):
            factor = augmented_matrix[k][i]
            for j in range(i, n + 1):
                augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
            steps.append({
                "step": f"Eliminate above pivot in row {k+1} using row {i+1} (factor: {factor})",
                "matrix": [row.copy() for row in augmented_matrix]
            })

        steps.append({
            "step": f"Completion of elimination above pivot in column {i+1}",
            "matrix": [row.copy() for row in augmented_matrix]
        })

    x = [row[n] for row in augmented_matrix]

    steps.append({
        "step": "Final result (solution vector)",
        "solution": x.copy()
    })

    return {
        "status": "success",
        "solution": x,
        "process_steps": steps
    }
