from django.shortcuts import render
from django.http import JsonResponse
from ..utils.fixed_point_iteration import fixed_point_iteration_method, generate_graph

def fixed_point_iteration_page(request):
    return render(request, 'fixed_point_iteration.html')

def calculate_fixed_point_iteration(request):
    if request.method == 'GET':
        try:
            equation = request.GET.get('equation')
            a = float(request.GET.get('a'))
            b = float(request.GET.get('b'))
            tol = float(request.GET.get('tol', 1e-6))
            max_iter = int(request.GET.get('maxIterations', 100))
            x0 = float(request.GET.get('p0', 1.0))  # Using p0 from frontend as x0

            if not equation:
                return JsonResponse({'error': True, 'message': 'Missing required parameters'})

            # Calculate result using fixed point iteration
            results = fixed_point_iteration_method(equation, tol, max_iter, x0)

            if results['error']:
                return JsonResponse({'error': True, 'message': results['message']})

            # Generate graph
            graph = generate_graph(equation, a, b, results['results'])

            return JsonResponse({
                "results": results,
                "graph": graph
            })

        except Exception as e:
            print(f"Error in calculate_fixed_point_iteration: {str(e)}")
            return JsonResponse({
                'error': True, 
                'message': f'Error processing request: {str(e)}'
            })
    
    return JsonResponse({'error': True, 'message': 'Method not allowed'}, status=405)

