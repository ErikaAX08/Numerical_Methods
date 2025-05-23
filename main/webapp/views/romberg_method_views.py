import base64
import io
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from sympy import exp, sin, cos, sinh, cosh, log, symbols, lambdify, sympify, integrate
from django.views.decorators.csrf import csrf_exempt

x = symbols('x')


def romberg_method_integration(func, a, b, max_level):
    """
    Calcula la tabla de Romberg para la integral de func en [a, b].
    Returns:
        romberg_table: lista de listas con los valores R[i][j]
        steps: lista de pasos intermedios como strings
    """
    f = lambdify(x, func, "numpy")
    romberg_table = []
    steps = []

    for i in range(max_level):
        n = 2 ** i
        h = (b - a) / n
        x_points = np.linspace(a, b, n + 1)
        y_points = f(x_points)
        T = h * (0.5 * y_points[0] +
                  np.sum(y_points[1:-1]) + 0.5 * y_points[-1])
        romberg_table.append([T])
        steps.append(
            f"T_{i},0 = {T:.10f} (n={n}, h={h:.5f})"
        )

    for j in range(1, max_level):
        for i in range(j, max_level):
            prev = romberg_table[i][j-1]
            prev2 = romberg_table[i-1][j-1]
            val = prev + (prev - prev2) / (4**j - 1)
            romberg_table[i].append(val)
            steps.append(
                f"T_{i},{j} = ({prev:.10f} + ({prev:.10f} - {prev2:.10f}) / ({4**j - 1})) = {val:.10f}"
            )

    return romberg_table, steps


def generate_romberg_method_plot(func, a, b, romberg_table):
    import matplotlib.pyplot as plt
    f = lambdify(x, func, "numpy")
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_vals, label="f(x)", color="blue")
    ax.set_title("Método de Romberg")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True)
    n = 2 ** (len(romberg_table) - 1)
    x_points = np.linspace(a, b, n + 1)
    y_points = f(x_points)
    ax.plot(x_points, y_points, 'ro', label="Puntos de evaluación")
    ax.legend()
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    return buffer


def generate_romberg_method_interactive_plot(func, a, b, romberg_table):
    import plotly.graph_objs as go
    f = lambdify(x, func, "numpy")
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines",
                  name="f(x)", line=dict(color="blue")))
    n = 2 ** (len(romberg_table) - 1)
    x_points = np.linspace(a, b, n + 1)
    y_points = f(x_points)
    fig.add_trace(go.Scatter(x=x_points, y=y_points, mode="markers",
                  name="Puntos de evaluación", marker=dict(color="red")))
    fig.update_layout(
        title="Método de Romberg",
        xaxis_title="x",
        yaxis_title="f(x)",
        legend=dict(orientation="h", yanchor="bottom",
                    y=1.02, xanchor="right", x=1)
    )
    return fig.to_json()


def parse_romberg_method_function(func_str):
    predefined = {
        "exp(x)": exp(x),
        "exp(-x)": exp(-x),
        "sin(x)": sin(x),
        "cos(x)": cos(x),
        "sinh(x)": sinh(x),
        "cosh(x)": cosh(x),
        "ln(1+x)": log(1 + x)
    }
    return predefined.get(func_str, sympify(func_str))


def calculate_romberg_method(request):
    try:
        func_str = request.GET.get("func")
        a = float(request.GET.get("a"))
        b = float(request.GET.get("b"))
        max_level = int(request.GET.get("maxLevel", 4))
        func = parse_romberg_method_function(func_str)

        # Obtiene tabla y pasos
        romberg_table, steps = romberg_method_integration(
            func, a, b, max_level)

        # Gráficos
        static_fig = generate_romberg_method_plot(func, a, b, romberg_table)
        image_base64 = base64.b64encode(static_fig.getvalue()).decode("utf-8")
        plot_json = generate_romberg_method_interactive_plot(
            func, a, b, romberg_table)

        try:
            exact = float(integrate(func, (x, a, b)).evalf())
        except Exception:
            exact = None

        romberg_serialized = []
        for row in romberg_table:
            romberg_serialized.append([float(val) for val in row])

        final_result = None
        if len(romberg_table) > 6 and len(romberg_table[6]) > 6:
            final_result = romberg_table[6][6]

        response = {
            "image": image_base64,
            "plot_json": plot_json,
            "romberg_table": romberg_serialized,
            "exact_value": exact,
            "final_result": final_result,
            "steps": steps,  # ✅ Agregado aquí
        }
        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def romberg_method(request):
    return render(request, "romberg_method.html")
