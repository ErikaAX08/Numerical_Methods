import numpy as np
from django.shortcuts import render
from django.http import JsonResponse

from ..utils.bisection_method import bisection_method_func, generate_graph


def calculate_bisection_method(request):
    print(request.GET)
    if request.method == "GET":
        try:
            # Get and validate parameters
            try:
                equation = request.GET.get('equation')
                a = float(request.GET.get('a'))
                b = float(request.GET.get('b'))
                tol = float(request.GET.get('tol', 1e-6))
                max_iter = int(request.GET.get('maxIterations', 100))
                p0 = float(request.GET.get('p0', 1.0))
                p1 = float(request.GET.get('p1', 2.5))

            except ValueError as e:
                return JsonResponse({
                    'error': True,
                    'message': f'Invalid parameter value: {str(e)}'
                })

            # Validate required parameters
            if not all([equation, a is not None, b is not None]):
                return JsonResponse({
                    'error': True,
                    'message': 'Missing required parameters'
                })

            results = bisection_method_func(equation, tol, p0, p1, max_iter)

            if results['error']:
                return JsonResponse({
                    'error': True,
                    'message': str(results['message'])
                })

            graph = generate_graph(equation, a, b, results['results'])

            response = {
                "results": results,
                "graph": graph
            }

            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': f'Error processing request: {str(e)}'
            })

    return JsonResponse({
        'error': True,
        'message': 'Method not allowed'
    }, status=405)


def bisection_method(request):
    return render(request, "bisection-method.html")
