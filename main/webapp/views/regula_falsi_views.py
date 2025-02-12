from django.shortcuts import render
from django.http import JsonResponse
from ..utils.regula_falsi import regula_falsi_func, regula_falsi_modified_func, generate_graph


def calculate_falsi(request):
    print(request.GET)
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
            results_regula_falsi = regula_falsi_func(
                equation=equation,
                tol=tol,
                max_iter=max_iter,
                p0=p0,
                p1=p1
            )

            results_regula_falsi_modified = regula_falsi_modified_func(
                equation=equation,
                tol=tol,
                max_iter=max_iter,
                p0=p0,
                p1=p1
            )

            print("results_regula_falsi: ", results_regula_falsi)
            print("results_regula_falsi_modified: ", results_regula_falsi_modified)

            if results_regula_falsi['error'] or results_regula_falsi_modified['error']:
                return JsonResponse({
                    'error': True,
                    'message': str(results_regula_falsi['message'])
                })

            plot_results_regula_falsi_json = generate_graph(equation, a, b, results_regula_falsi['results'])
            plot_results_regula_falsi_modified_json = generate_graph(equation, a, b,
                                                                     results_regula_falsi_modified['results'])

            response = {
                "graph_results_regula_falsi": plot_results_regula_falsi_json,
                "graph_results_regula_falsi_modified": plot_results_regula_falsi_modified_json,
                "results_regula_falsi": results_regula_falsi,
                "results_regula_falsi_modified": results_regula_falsi_modified
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


def regula_falsi(request):
    return render(request, "regula-falsi.html")
