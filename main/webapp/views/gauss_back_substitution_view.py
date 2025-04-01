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
            result, steps = gauss_elimination_with_back_substitution(
                matrix, vector)

            return JsonResponse({"solution": result, "process_steps": steps})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as error:
            print("Error:", error)
            return JsonResponse({'error': str(error)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def gauss_elimination_with_back_substitution(matrix, vector):
    """
    Implementation of Gauss-Jordan elimination (full reduction)
    Returns the solution vector and detailed steps for visualization
    """
    n = len(matrix)
    augmented_matrix = []
    steps = []

    # Create augmented matrix [A|b]
    for i in range(n):
        row = matrix[i].copy()
        row.append(vector[i])
        augmented_matrix.append(row)

    steps.append({
        "step": "Initial augmented matrix",
        "matrix": [row.copy() for row in augmented_matrix]
    })

    # Forward elimination phase
    for i in range(n):
        # Find pivot row (partial pivoting)
        max_row = i
        for k in range(i + 1, n):
            if abs(augmented_matrix[k][i]) > abs(augmented_matrix[max_row][i]):
                max_row = k

        # Swap rows if necessary
        if max_row != i:
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            steps.append({
                "step": f"Swap row {i+1} with row {max_row+1}",
                "matrix": [row.copy() for row in augmented_matrix]
            })

        # Make pivot element 1
        pivot = augmented_matrix[i][i]
        if abs(pivot) < 1e-10:
            raise ValueError("Matrix is singular, cannot solve system")

        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot

        steps.append({
            "step": f"Scale row {i+1} by 1/{pivot}",
            "matrix": [row.copy() for row in augmented_matrix]
        })

        # Eliminate elements below pivot
        for k in range(i + 1, n):
            factor = augmented_matrix[k][i]
            if abs(factor) > 1e-10:  # Solo realizar la eliminación si el factor no es cero
                for j in range(i, n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
                steps.append({
                    "step": f"Eliminate below pivot in row {k+1} using row {i+1} (factor: {factor})",
                    "matrix": [row.copy() for row in augmented_matrix]
                })

        # Mostrar la matriz después de eliminar todos los elementos debajo del pivote
        steps.append({
            "step": f"Completion of elimination below pivot in column {i+1}",
            "matrix": [row.copy() for row in augmented_matrix]
        })

    # Back substitution phase (continuando con la eliminación hacia arriba - Gauss-Jordan)
    for i in range(n-1, -1, -1):
        # Eliminate elements above pivot (which is now 1)
        for k in range(i-1, -1, -1):
            factor = augmented_matrix[k][i]
            if abs(factor) > 1e-10:  # Solo realizar la eliminación si el factor no es cero
                for j in range(i, n + 1):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
                steps.append({
                    "step": f"Eliminate above pivot in row {k+1} using row {i+1} (factor: {factor})",
                    "matrix": [row.copy() for row in augmented_matrix]
                })

        # Mostrar la matriz después de eliminar todos los elementos arriba del pivote
        steps.append({
            "step": f"Completion of elimination above pivot in column {i+1}",
            "matrix": [row.copy() for row in augmented_matrix]
        })

    # Extract solution (no need for back substitution in Gauss-Jordan)
    x = [row[n] for row in augmented_matrix]

    steps.append({
        "step": "Final result (solution vector)",
        "solution": x.copy()
    })

    return x, steps
