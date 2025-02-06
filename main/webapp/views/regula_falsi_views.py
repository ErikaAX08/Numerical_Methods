from django.shortcuts import render
from django.http import JsonResponse
from ..utils.regula_falsi import regula_falsi_func

def calculate_falsi(request):
    if request.method == 'GET':
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

            # Calculate result
            result = regula_falsi_func(
                equation=equation,
                a=a,
                b=b,
                tol=tol,
                max_iter=max_iter,
                p0=p0,
                p1=p1
            )

            return JsonResponse(result)

        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': f'Error processing request: {str(e)}'
            })

    return JsonResponse({
        'error': True,
        'message': 'Method not allowed'
    }, status=405)

def regula_falsi(request):
    return render(request, "regula-falsi.html")