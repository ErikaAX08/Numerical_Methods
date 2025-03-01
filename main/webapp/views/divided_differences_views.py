from django.shortcuts import render
from django.http import JsonResponse

from ..utils.newton_raphson_method import newton_raphson_method_func, generate_graph


def calculate_divided_differences(request):
    print(request.GET)

    if request.method == 'GET':
        try:
            print("newton_raphson")
            try:
                equation = request.GET.get('equation')
                a = float(request.GET.get('a'))
                b = float(request.GET.get('b'))
                tol = float(request.GET.get('tol', 1e-6))
                max_iter = int(request.GET.get('maxIterations', 100))
                p0 = float(request.GET.get('p0', 1.0))
                p1 = float(request.GET.get('p1', 2.5))
            except ValueError as e:
                return JsonResponse({'error': True, 'message': f'Invalid parameter value: {str(e)}'})

            if not all([equation, p0 is not None]):
                return JsonResponse({'error': True, 'message': 'Missing required parameters'})

            # Calculate result
            results = newton_raphson_method_func(equation, tol, max_iter, p0)

            print("results: ", results)

            if results['error']:
                return JsonResponse({'error': True, 'message': str(results['message'])})

            graph = generate_graph(equation, a, b, results['results'])

            response = {
                "results": results,
                "graph": graph
            }

            return JsonResponse(response)

        except Exception as e:
            print(e)
            return JsonResponse({'error': True, 'message': f'Error processing request: {str(e)}'})
    else:
        return JsonResponse({'error': True, 'message': 'Method not allowed'}, status=405)


def divided_differences(request):
    return render(request, 'divided-differences.html')