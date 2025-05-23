import base64
from django.http import JsonResponse
from django.shortcuts import render
from sympy import symbols, sympify
from webapp.utils.gauss_quadrature import gauss_quadrature, generate_gauss_graph, generate_interactive_gauss_graph

# Definir la variable simbólica
x = symbols('x')

def gauss_quadrature_page(request):
    """Render the Gauss quadrature calculator page."""
    return render(request, "gauss_quadrature.html")

def calculate_gauss(request):
    """Handle the calculation of Gauss quadrature."""
    if request.method == "GET" and request.GET.get("func"):
        func = request.GET.get("func")
        a = float(request.GET.get("a"))
        b = float(request.GET.get("b"))
        n = int(request.GET.get("n", 2))

        try:
            parsed_func = sympify(func)
            
            # Calcular la integral usando cuadratura de Gauss
            integral_value, x_points, y_points, _, _, weights = gauss_quadrature(parsed_func, a, b, n)
            
            # Generar gráficos
            plot_buffer = generate_gauss_graph(parsed_func, a, b, n, integral_value)
            plot_image = base64.b64encode(plot_buffer.getvalue()).decode('utf-8')
            plot_json = generate_interactive_gauss_graph(parsed_func, a, b, n, integral_value)

            return JsonResponse({
                "error": None,
                "integral_value": float(integral_value),
                "x_values": x_points,
                "y_values": y_points,
                "weights": weights,
                "image": plot_image,
                "plot_json": plot_json
            })

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return render(request, "gauss_quadrature.html")