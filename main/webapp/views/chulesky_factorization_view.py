from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Asegúrate de que esta ruta sea correcta para tu proyecto
from ..utils.chulesky_factorization import cholesky_factorization_method


def chulesky_factorization(request):
    """
    Renderiza la plantilla HTML para la factorización de Cholesky
    """
    return render(request, 'chulesky-factorization.html')


@csrf_exempt
def calculate_chulesky_factorization(request):
    """
    Procesa la solicitud para calcular la factorización de Cholesky y resolver
    el sistema de ecuaciones lineales.

    Acepta solicitudes POST con una matriz en formato JSON.
    """
    try:
        print("Iniciando cálculo de factorización de Cholesky...")

        # Obtener la matriz desde la solicitud POST
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
            return JsonResponse({'error': 'Método no permitido. Use POST'}, status=405)

        # Verificar que la matriz no esté vacía
        if not matrix or not matrix[0]:
            return JsonResponse({'error': 'La matriz está vacía'}, status=400)

        # Mostrar la matriz recibida (para debugging)
        print("Matriz recibida:", matrix)

        # Ejecutar el método de factorización de Cholesky
        result, steps = cholesky_factorization_method(matrix)

        # Verificar si hubo un error (resultado es string)
        if isinstance(result, str):
            return JsonResponse({
                'status': 'error',
                'message': result,
                'process_steps': steps
            })
        # Verificar si hay infinitas soluciones (resultado es diccionario)
        elif isinstance(result, dict) and result.get('status') == 'infinite_solutions':
            return JsonResponse({
                'status': 'infinite_solutions',
                'message': result.get('message', 'El sistema tiene infinitas soluciones'),
                'details': result.get('details', {}),
                'process_steps': steps
            })

        # Devolver el resultado y los pasos para una solución exitosa
        return JsonResponse({
            'status': 'success',
            'solution': result,
            'process_steps': steps
        })

    except Exception as error:
        print("Error en el cálculo:", error)
        return JsonResponse({
            'status': 'error',
            'message': f'Error en el cálculo: {str(error)}'
        }, status=500)
