from django.http import JsonResponse
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from django.shortcuts import render
from sympy import symbols, sympify, lambdify, integrate, sin, cos, sinh, cosh, exp, log
import io
import base64

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


def simpson_compuesta(f_numeric, a, b, n):
    if n % 2 == 1:
        raise ValueError(
            "Simpson 1/3 compuesta requiere un número par de subintervalos.")

    h = (b - a) / n
    x_vals = np.linspace(a, b, n + 1)
    y_vals = f_numeric(x_vals)

    integral = y_vals[0] + y_vals[-1]
    integral += 4 * np.sum(y_vals[1:-1:2])  # impares
    integral += 2 * np.sum(y_vals[2:-2:2])  # pares
    integral *= h / 3

    return integral


def simpson_static_plot(f_numeric, a, b, n, approx):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f_numeric(x_vals)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_vals, label="f(x)", color="blue")

    x_partition = np.linspace(a, b, n + 1)
    y_partition = f_numeric(x_partition)
    ax.plot(x_partition, y_partition, 'ro')

    for i in range(0, n, 2):
        x_parabola = np.linspace(x_partition[i], x_partition[i+2], 100)
        xi, xi1, xi2 = x_partition[i], x_partition[i+1], x_partition[i+2]
        yi, yi1, yi2 = y_partition[i], y_partition[i+1], y_partition[i+2]
        coeffs = np.polyfit([xi, xi1, xi2], [yi, yi1, yi2], 2)
        y_parabola = np.polyval(coeffs, x_parabola)
        ax.fill_between(x_parabola, y_parabola, alpha=0.3, color="orange")

    ax.set_title("Simpson 1/3 Compuesta (Estática)")


    ax.text(0.05, 0.95, f"Resultado ≈ {approx:.6f}", transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    ax.legend()
    ax.grid(True)
    return fig


def simpson_interactive_plot(f_numeric, a, b, max_n, approx):
    if max_n % 2 == 1:
        max_n += 1  # debe ser par

    x_plot = np.linspace(a, b, 1000)
    y_plot = f_numeric(x_plot)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_plot, y=y_plot, mode="lines",
                             name="f(x)", line=dict(color="blue")))

    for n in range(2, max_n + 1, 2):
        x_partition = np.linspace(a, b, n + 1)
        y_partition = f_numeric(x_partition)

        fig.add_trace(go.Scatter(
            x=x_partition, y=y_partition,
            mode="markers+lines",
            name=f"n = {n}",
            visible=False
        ))

    fig.data[1].visible = True

    steps = []
    for i in range(1, len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [True] + [j == i for j in range(1, len(fig.data))]},
                  {"title": f"Simpson 1/3 Compuesta — Subintervalos: {2 * i}"}],
            label=f"{2 * i}"
        )
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Subintervalos: "},
        pad={"t": 30},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders,
        title="Aproximación Interactiva — Simpson 1/3 Compuesta",
        xaxis_title="x",
        yaxis_title="f(x)"
    )
    
    fig.add_annotation(
        text=f"Resultado aproximado (n = {max_n}): {approx:.6f}",
        xref="paper", yref="paper",
        x=0.5, y=1.1, showarrow=False,
        font=dict(size=14),
        bgcolor="white"
    )


    return fig


def calculate_simpson(request):
    try:
        func_str = request.GET.get("func")
        a = float(request.GET.get("a"))
        b = float(request.GET.get("b"))
        n = int(request.GET.get("pt_num", 10))  # CAMBIO: usar "pt_num"
        max_n = int(request.GET.get("max_subintervals", 20))
        exact = request.GET.get("exact", "false").lower() == "true"

        if n % 2 == 1:
            n += 1
        if max_n % 2 == 1:
            max_n += 1

        func = parse_function(func_str)
        f_numeric = lambdify(x, func, "numpy")

        approx = simpson_compuesta(f_numeric, a, b, n)

        # Convertir imagen a base64
        static_fig = simpson_static_plot(f_numeric, a, b, n, approx)
        buffer = io.BytesIO()
        static_fig.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        buffer.close()
        plt.close(static_fig)

        # Gráfica interactiva (Plotly JSON)
        interactive_fig = simpson_interactive_plot(f_numeric, a, b, max_n, approx)
        plot_json = interactive_fig.to_json()

        # Tabla de puntos
        h = (b - a) / n
        x_values = [a + i * h for i in range(n + 1)]
        y_values = [f_numeric(xi) for xi in x_values]

        response = {
            "approx": approx,
            "image": image_base64,
            "plot_json": plot_json,
            "x_values": x_values,
            "original_y_values": y_values,
        }

        if exact:
            integral = integrate(func, (x, a, b))
            response["exact"] = float(integral.evalf())
            response["error"] = abs(response["exact"] - approx)

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def simpson_tercio_compuesto(request):
    return render(request, "simpson-tercio-compuesto.html")
