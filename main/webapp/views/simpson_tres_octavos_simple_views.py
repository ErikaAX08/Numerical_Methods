from django.http import JsonResponse
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from django.shortcuts import render
from sympy import symbols, sympify, lambdify, integrate, sin, cos, sinh, cosh, exp, log
import io
import base64

# Importar la función utilitaria usando import relativo
from ..utils.simpson_tres_octavos_simple import simpson_tres_octavos_simple

x = symbols("x")

def parse_function(func_str):
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

def simpson_static_plot(f_numeric, a, b, approx, x_points):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f_numeric(x_vals)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_vals, label="f(x)", color="blue")

    y_points = f_numeric(np.array(x_points))
    ax.plot(x_points, y_points, 'ro')

    coeffs = np.polyfit(x_points, y_points, 3)
    x_poly = np.linspace(a, b, 200)
    y_poly = np.polyval(coeffs, x_poly)
    ax.fill_between(x_poly, y_poly, alpha=0.3, color="orange")

    ax.set_title("Simpson 3/8 Simple (Estática)")
    ax.text(0.05, 0.95, f"Resultado ≈ {approx:.6f}", transform=ax.transAxes,
            fontsize=12, verticalalignment='top',
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    ax.legend()
    ax.grid(True)
    return fig

def simpson_interactive_plot(f_numeric, a, b, approx, x_points):
    x_plot = np.linspace(a, b, 1000)
    y_plot = f_numeric(x_plot)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_plot, y=y_plot, mode="lines", name="f(x)", line=dict(color="blue")))

    y_partition = f_numeric(np.array(x_points))
    fig.add_trace(go.Scatter(x=x_points, y=y_partition, mode="markers+lines", name="Puntos Simpson 3/8"))

    fig.update_layout(
        title="Simpson 3/8 Simple",
        xaxis_title="x",
        yaxis_title="f(x)",
        annotations=[dict(
            text=f"Resultado aproximado: {approx:.6f}",
            xref="paper", yref="paper",
            x=0.5, y=1.1, showarrow=False,
            font=dict(size=14),
            bgcolor="white"
        )]
    )
    return fig

def calculate_simpson_tres_octavos_simple(request):
    try:
        func_str = request.GET.get("func")
        a = float(request.GET.get("a"))
        b = float(request.GET.get("b"))
        pt_num = request.GET.get("pt_num")  # No se usa, pero se acepta para compatibilidad
        exact = request.GET.get("exact", "false").lower() == "true"

        func = parse_function(func_str)
        # Usar la función utilitaria para obtener el resultado y los puntos
        approx = simpson_tres_octavos_simple(func, a, b)
        # Calcular los puntos de evaluación
        h = (b - a) / 3
        x_points = [a, a + h, a + 2*h, b]

        f_numeric = lambdify(x, func, "numpy")

        # Imagen estática
        static_fig = simpson_static_plot(f_numeric, a, b, approx, x_points)
        buffer = io.BytesIO()
        static_fig.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        buffer.close()
        plt.close(static_fig)

        # Gráfica interactiva
        interactive_fig = simpson_interactive_plot(f_numeric, a, b, approx, x_points)
        plot_json = interactive_fig.to_json()

        y_values = [f_numeric(xi) for xi in x_points]

        response = {
            "approx": approx,
            "image": image_base64,
            "plot_json": plot_json,
            "x_values": x_points,
            "original_y_values": y_values,
        }

        if exact:
            integral = integrate(func, (x, a, b))
            response["exact"] = float(integral.evalf())
            response["error"] = abs(response["exact"] - approx)

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def simpson_tres_octavos_simple(request):
    return render(request, "simpson-tres-octavos-simple.html")
