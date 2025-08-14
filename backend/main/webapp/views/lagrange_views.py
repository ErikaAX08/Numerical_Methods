import json
from django.shortcuts import render
from django.http import JsonResponse

from ..utils.lagrange import lagrange_method

def calculate_lagrange(request):
    if request.method == 'GET':
        try:
            # Get and validate parameters
            try:
                points_str = request.GET.get('points')
                points = json.loads(points_str)
                degree = int(request.GET.get('degree'))
                valueToInterpolate = float(request.GET.get('valueToInterpolate'))
            except ValueError as e:
                return JsonResponse({
                    'error': True,
                    'message': f'Invalid parameter value: {str(e)}'
                })

            # Validate required parameters
            if not all([points, degree, valueToInterpolate]):
                return JsonResponse({
                    'error': True,
                    'message': 'Missing required parameters'
                })

            try:
                result, process_steps = lagrange_method(degree, valueToInterpolate, points)

                # Retornar el resultado y los pasos al frontend
                response = {
                    "error": False,
                    "message": "Success",
                    "result": result,
                    "process_steps": process_steps,
                }

                return JsonResponse(response)
            except Exception as e:
                return JsonResponse({
                    'error': True,
                    'message': f'Error processing request: {str(e)}'
                })

        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': f'Error processing request: {str(e)}'
            })
    else:
        return JsonResponse({
            'error': True,
            'message': 'Method not allowed'
        }, status=405)


def lagrange(request):
    return render(request, 'lagrange.html')
