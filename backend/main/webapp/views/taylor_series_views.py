import base64

import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from sympy import exp, sin, cos, sinh, cosh, log, lambdify

from ..utils.taylor_series import generate_graph, generate_interactive_graph, taylor_approximation, x

def calculate_taylor(request):
    global x
    sym_func = None
    if request.method == "GET":
        try:
            # Get the values from the form
            func = request.GET.get("func")
            a = float(request.GET.get("a"))  # Transform to float
            b = float(request.GET.get("b"))
            pt_num = int(request.GET.get("pt_num"))
            degrees = list(map(int, request.GET.get("degrees").split(",")))

            if func == "ln(1+x)":
                response = {
                    "image": "",
                    "x_values": [],
                    "original_y_values": [],
                    "taylor_data": {},
                    "error": "Cannot calculate Taylor series for ln(1+x)",
                    "message": "The function ln(1+x) does not have a valid Taylor series."
                }
                return JsonResponse(response)

            # Define the symbolic function
            if func == "exp(x)":
                sym_func = exp(x)
            elif func == "exp(-x)":
                sym_func = exp(-x)
            elif func == "sin(x)":
                sym_func = sin(x)
            elif func == "cos(x)":
                sym_func = cos(x)
            elif func == "sinh(x)":
                sym_func = sinh(x)
            elif func == "cosh(x)":
                sym_func = cosh(x)
            elif func == "ln(1+x)":
                sym_func = log(1 + x)

            # Generate graph
            graph_buffer = generate_graph(sym_func, a, b, pt_num, degrees)
            plot_json = generate_interactive_graph(sym_func, a, b, pt_num, degrees)

            # Create the x values in the range [a, b]
            x_values = np.linspace(a, b, pt_num)

            # Calculate the values of the original function
            original_function = lambdify(x, sym_func, "numpy")
            original_y_values = original_function(x_values)

            # Calculate the Taylor approximations for each degree
            taylor_data = {}
            for degree in degrees:
                taylor_values = [
                    taylor_approximation(sym_func, x, degree) for x in x_values
                ]
                taylor_data[f"Grado {degree}"] = taylor_values

            image_base64 = base64.b64encode(graph_buffer.getvalue()).decode("utf-8")

            # Return the image and the tabulated data
            response = {
                "image": image_base64,
                "plot_json": plot_json,
                "x_values": x_values.tolist(),
                "original_y_values": original_y_values.tolist(),
                "taylor_data": taylor_data,
            }
            return JsonResponse(response)
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


def taylor_series(request):
    return render(request, "taylor-series.html")
