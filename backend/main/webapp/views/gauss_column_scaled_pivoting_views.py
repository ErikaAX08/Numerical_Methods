from django.shortcuts import render
from django.http import JsonResponse
from ..utils.gauss_column_scaled_pivoting import gauss_column_scaled_pivoting_method
import json
from django.views.decorators.csrf import csrf_exempt


def gauss_column_scaled_pivoting(request):
    return render(request, 'gauss-column-scaled-pivoting.html')


@csrf_exempt
def calculate_gauss_column_scaled_pivoting(request):
    try:
        print("Método de solicitud:", request.method)

        if request.method == 'GET':

            print("Parámetros GET:", request.GET)
            matrix_json = request.GET.get("matrix")
            print("JSON de matriz recibido:", matrix_json)

            if not matrix_json:
                return JsonResponse({"error": "Falta el parámetro 'matrix'."})

            try:
                matrix = json.loads(matrix_json)
                print("Matriz decodificada:", matrix)
            except json.JSONDecodeError as e:
                return JsonResponse({"error": f"Error al decodificar la matriz JSON: {str(e)}"}, status=400)

            # Ejecutar el algoritmo
            result = gauss_column_scaled_pivoting_method(matrix)

            if 'error' in result:
                # Envía errores matemáticos como respuesta normal, no como error HTTP
                return JsonResponse({
                    'error': result['error'],
                    'is_math_error': True,  # Añade una bandera para identificar errores matemáticos
                    'process_steps': result.get('process_steps', [])
                })

            # Formatear la solución para la respuesta
            solution_str = ", ".join([f"{key} = {value}" for key, value in result['solution'].items()])

            return JsonResponse({
                'result': solution_str,
                'solution': result['solution'],
                'process_steps': result['process_steps']
            })
        elif request.method == 'POST':
            # Mantener compatibilidad con POST
            data = json.loads(request.body)
            matrix = data.get('matrix')

            if not matrix:
                return JsonResponse({'error': 'No se recibió ninguna matriz'}, status=400)

            # Ejecutar el algoritmo
            result = gauss_column_scaled_pivoting_method(matrix)

            if 'error' in result:
                # Envía errores matemáticos como respuesta normal, no como error HTTP
                return JsonResponse({
                    'error': result['error'],
                    'is_math_error': True,  # Añade una bandera para identificar errores matemáticos
                    'process_steps': result.get('process_steps', [])
                })

            # Formatear la solución para la respuesta
            solution_str = ", ".join([f"{key} = {value}" for key, value in result['solution'].items()])

            return JsonResponse({
                'result': solution_str,
                'solution': result['solution'],
                'process_steps': result['process_steps']
            })

        return JsonResponse({'error': 'Método no soportado'}, status=405)

    except Exception as error:
        print("Error en calculate_gauss_column_scaled_pivoting:", error)
        return JsonResponse({'error': str(error)}, status=500)
