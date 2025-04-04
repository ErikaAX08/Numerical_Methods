from django.shortcuts import render
from django.http import JsonResponse
from ..utils.gauss_maximum_column_pivoting import gauss_maximum_column_pivoting_method
import json


def gauss_maximum_column_pivoting(request):
    return render(request, 'gauss_maximum_column_pivoting.html')


def calculate_gauss_maximum_column_pivoting(request):
    if request.method == "POST":
        try:
            print("Start calculating gauss elimination with maximum column pivoting...")

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

            # Crear la matriz aumentada
            augmented_matrix = [row + [vector[i]] for i, row in enumerate(matrix)]

            # Ejecutar el método de eliminación gaussiana con pivoteo máximo de columnas
            result, steps = gauss_maximum_column_pivoting_method(augmented_matrix)

            if isinstance(result, str):  # Error en la ejecución
                return JsonResponse({'error': result}, status=400)

            return JsonResponse({"solution": result, "process_steps": steps})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as error:
            print("Error:", error)
            return JsonResponse({'error': str(error)}, status=500)

