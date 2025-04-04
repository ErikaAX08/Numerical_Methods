from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.gauss_maximum_column_pivoting import gauss_maximum_column_pivoting_method
import json


def gauss_maximum_column_pivoting(request):
    """
    Renderiza la plantilla con la calculadora de eliminación gaussiana
    """
    return render(request, 'gauss_maximum_column_pivoting.html')


@csrf_exempt  # Solo para pruebas, en producción se debe manejar correctamente el CSRF
def calculate_gauss_maximum_column_pivoting(request):
    """
    Procesa la solicitud para calcular la solución del sistema mediante
    el método de eliminación gaussiana con pivoteo máximo de columnas.

    Acepta tanto solicitudes GET como POST.
    """
    try:
        print("Iniciando cálculo de eliminación gaussiana con pivoteo máximo de columnas...")

        # Obtener la matriz desde la solicitud GET o POST
        if request.method == "POST":
            # Para solicitudes POST con JSON
            try:
                data = json.loads(request.body.decode("utf-8"))
                matrix = data.get("matrix", [])
                print(f"Datos recibidos por POST: {data}")
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
                return JsonResponse({'error': f'Formato JSON inválido: {str(e)}'}, status=400)
        else:
            # Para solicitudes GET, obtener la matriz del formulario HTML
            try:
                rows = int(request.GET.get('rows', 0))
                cols = int(request.GET.get('cols', 0))

                if rows < 1 or cols < 2:
                    return JsonResponse({
                        'error': 'Se requieren al menos 1 fila y 2 columnas para la matriz aumentada'
                    }, status=400)

                matrix = []
                for i in range(rows):
                    row = []
                    for j in range(cols):
                        value_str = request.GET.get(f'matrix[{i}][{j}]', '')
                        try:
                            value = float(value_str) if value_str else 0
                            row.append(value)
                        except ValueError:
                            return JsonResponse({
                                'error': f'Valor inválido en la posición [{i + 1}, {j + 1}]: {value_str}'
                            }, status=400)
                    matrix.append(row)
                print(f"Datos recibidos por GET: {matrix}")
            except Exception as e:
                print(f"Error al procesar datos GET: {e}")
                return JsonResponse({'error': f'Error al procesar parámetros: {str(e)}'}, status=400)

        # Verificar que la matriz no esté vacía
        if not matrix or not matrix[0]:
            return JsonResponse({'error': 'La matriz está vacía'}, status=400)

        # Mostrar la matriz recibida (para debugging)
        print("Matriz recibida:", matrix)

        # Ejecutar el método de eliminación gaussiana con pivoteo máximo de columnas
        result, steps = gauss_maximum_column_pivoting_method(matrix)

        # Verificar si hubo un error
        if isinstance(result, str):
            return JsonResponse({
                'error': result,
                'process_steps': steps
            })

        # Devolver el resultado y los pasos
        return JsonResponse({
            "result": result,
            "process_steps": steps
        })

    except Exception as error:
        print("Error en el cálculo:", error)
        return JsonResponse({'error': str(error)}, status=500)
