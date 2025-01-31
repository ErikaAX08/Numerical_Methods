from django.shortcuts import render
import matplotlib

matplotlib.use("Agg")  # FOR USE WITHOUT DISPLAY
import matplotlib.pyplot as plt
import io
import numpy as np
from django.http import JsonResponse
from sympy import symbols, exp, sin, cos, sinh, cosh, log, series, lambdify
import base64

def index(request):
    return render(request, "index.html")


x = symbols("x")

# Predefinied functions
# We use this funcions to compare the results of the taylor series
def functions(func, x_val):
    if func == "exp(x)":
        return float(exp(x).subs(x, x_val))
    elif func == "exp(-x)":
        return float(exp(-x).subs(x, x_val))
    elif func == "sin(x)":
        return float(sin(x).subs(x, x_val))
    elif func == "cos(x)":
        return float(cos(x).subs(x, x_val))
    elif func == "sinh(x)":
        return float(sinh(x).subs(x, x_val))
    elif func == "cosh(x)":
        return float(cosh(x).subs(x, x_val))
    elif func == "ln(1+x)":
        return float(log(1 + x).subs(x, x_val))


# Function to calculate the derivate of a function
def derivative(func, x, n, h=0.0001):
    if n == 0:
        return functions(func, x)
    else:
        return (derivative(func, x + h, n - 1) - derivative(func, x - h, n - 1)) / (
            2 * h
        )


# Calculate the Taylor approximation of a function
def taylor_approximation(func, x_val, degree):
    try:
        taylor_series = series(func, x, 0, degree + 1).removeO()
        return float(taylor_series.subs(x, x_val))
    except Exception as e:
        print(f"Error en taylor_approximation: {str(e)}")  # Debug
        raise e


# Generate the graph
def generate_graph(func, a, b, pt_num, degrees, plane_size=10):
    try:
        # Create the x values in the range [a, b]
        x_values = np.linspace(a, b, pt_num)
        print(f"x_values: {x_values}")  # Debug

        # Create the y values for the original function in the range [a, b]
        original_function = lambdify(x, func, "numpy")
        original_x_values = np.linspace(a, b, 1000)
        original_y_values = original_function(original_x_values)
        print(f"y_values: {original_y_values}")  # Debug

        # Create the graph
        plt.figure()

        # Graph the original function in the range [a, b]
        plt.plot(
            original_x_values,
            original_y_values,
            label=f"Original: {func}",
            color="black",
        )

        # Graph the Taylor series for each degree in the range [a, b]
        for degree in degrees:
            taylor_values = [taylor_approximation(func, x, degree) for x in x_values]
            print(f"Degree {degree}: {taylor_values}")  # Debug
            plt.plot(x_values, taylor_values, label=f"Degree {degree}")

        # Add labels and title
        plt.xlabel("X")
        plt.ylabel("f(x)")
        plt.title(f"Taylor approximation for {func}")
        plt.legend()
        plt.grid(True)

        # Fix the axis limits so that the plane is always in [-10, 10]
        plt.xlim(-plane_size, plane_size)
        plt.ylim(-plane_size, plane_size)

        # Save the graph in a buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=300)
        plt.close()
        buffer.seek(0)

        return buffer
    except Exception as e:
        print(f"Error en generate_graph: {str(e)}")  # Debug
        raise e


# View to calculate and display the Taylor approximation
def calculate_taylor(request):
    if request.method == "GET":
        try:
            # Get the values from the form
            func = request.GET.get("func")
            a = float(request.GET.get("a"))  # Transform to float
            b = float(request.GET.get("b"))
            pt_num = int(request.GET.get("pt_num"))
            degrees = list(map(int, request.GET.get("degrees").split(",")))
            plane_size = int(request.GET.get("plane_size"))

            print(
                f"Func: {func}, a: {a}, b: {b}, pt_num: {pt_num}, degrees: {degrees}"
            )  # Debug

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
            graph_buffer = generate_graph(sym_func, a, b, pt_num, degrees, plane_size)

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


# templates
def taylor_series(request):
    return render(request, "taylor-series.html")
