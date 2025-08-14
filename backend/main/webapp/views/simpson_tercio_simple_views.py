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


def simpson_simple(f_numeric, a, b):
    """
    Implementa la regla de Simpson 1/3 simple.
    """
    h = (b - a) / 2
    x_mid = (a + b) / 2
    
    integral = (h / 3) * (f_numeric(a) + 4 * f_numeric(x_mid) + f_numeric(b))
    
    return integral


def simpson_static_plot(f_numeric, a, b, approx, exact=None):
    """
    Genera un gráfico estático que muestra la función y la aproximación de Simpson 1/3 simple.
    """
    x_vals = np.linspace(a, b, 1000)
    y_vals = f_numeric(x_vals)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_vals, label="f(x)", color="blue")

    # Puntos de Simpson simple: los extremos y el punto medio
    x_points = [a, (a+b)/2, b]
    y_points = f_numeric(np.array(x_points))
    ax.plot(x_points, y_points, 'ro')

    # Crear una parábola que pasa por los tres puntos
    x_parabola = np.linspace(a, b, 100)
    coeffs = np.polyfit(x_points, y_points, 2)
    y_parabola = np.polyval(coeffs, x_parabola)
    ax.plot(x_parabola, y_parabola, '--', color="orange", label="Parábola de aproximación")
    ax.fill_between(x_parabola, y_parabola, alpha=0.3, color="orange")

    ax.set_title("Simpson 1/3 Simple")
    
    # Mostrar resultado y error si está disponible
    text_info = f"Resultado ≈ {approx:.6f}"
    if exact is not None:
        error = abs(exact - approx)
        error_rel = error / abs(exact) * 100 if exact != 0 else float('inf')
        text_info += f"\nValor exacto = {exact:.6f}"
        text_info += f"\nError absoluto = {error:.6f}"
        text_info += f"\nError relativo = {error_rel:.2f}%"
    
    ax.text(0.05, 0.95, text_info, transform=ax.transAxes, fontsize=10, 
           verticalalignment='top', bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    ax.legend()
    ax.grid(True)
    return fig


def simpson_interactive_plot(f_numeric, a, b, approx, exact=None):
    """
    Genera un gráfico interactivo para la aproximación de Simpson 1/3 simple
    mostrando todos los elementos a la vez.
    """
    x_plot = np.linspace(a, b, 1000)
    y_plot = f_numeric(x_plot)
    
    # Puntos de Simpson simple
    x_points = [a, (a+b)/2, b]
    y_points = [f_numeric(xi) for xi in x_points]
    
    # Parábola de aproximación
    coeffs = np.polyfit(x_points, y_points, 2)
    x_parabola = np.linspace(a, b, 100)
    y_parabola = np.polyval(coeffs, x_parabola)
    
    # Cálculo del error si tenemos el valor exacto
    error_text = ""
    if exact is not None:
        error = abs(exact - approx)
        error_rel = error / abs(exact) * 100 if exact != 0 else float('inf')
        error_text = f"<br>Valor exacto: {exact:.6f}"
        error_text += f"<br>Error absoluto: {error:.6f}"
        error_text += f"<br>Error relativo: {error_rel:.2f}%"
    
    # Crear figura interactiva con todos los elementos visibles
    fig = go.Figure()
    
    # Mostrar la función original
    fig.add_trace(go.Scatter(
        x=x_plot, y=y_plot, mode="lines", name="f(x)", line=dict(color="blue")
    ))
    
    # Añadir los tres puntos de evaluación
    fig.add_trace(go.Scatter(
        x=x_points, y=y_points, mode="markers", name="Puntos de evaluación",
        marker=dict(size=10, color="red")
    ))
    
    # Mostrar la parábola de aproximación
    fig.add_trace(go.Scatter(
        x=x_parabola, y=y_parabola, mode="lines", name="Parábola",
        line=dict(color="orange", dash="dash")
    ))
    
    # Mostrar el área bajo la parábola (resultado de Simpson)
    fig.add_trace(go.Scatter(
        x=x_parabola, y=y_parabola, mode="lines", name="Área aproximada",
        line=dict(color="orange"), fill='tozeroy', fillcolor='rgba(255, 165, 0, 0.3)'
    ))
    
    # Mostrar el área real bajo la curva para comparar (si está disponible)
    if exact is not None:
        fig.add_trace(go.Scatter(
            x=x_plot, y=y_plot, mode="lines", name="Área real",
            line=dict(color="blue", width=0.5), fill='tozeroy', 
            fillcolor='rgba(0, 0, 255, 0.2)'
        ))
    
    # Título y layout sin sliders
    title_text = f"Simpson 1/3 Simple<br>Resultado: {approx:.6f}{error_text}"
    
    fig.update_layout(
        title=title_text,
        xaxis_title="x",
        yaxis_title="f(x)",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        height=600
    )
    
    return fig

def calculate_simpson_tercio_simple(request):
    try:
        func_str = request.GET.get("func")
        a = float(request.GET.get("a"))
        b = float(request.GET.get("b"))
        exact_requested = request.GET.get("exact", "true").lower() == "true"

        func = parse_function(func_str)
        f_numeric = lambdify(x, func, "numpy")

        # Calcular la aproximación
        approx = simpson_simple(f_numeric, a, b)
        
        # Calcular el valor exacto (si es posible)
        exact = None
        if exact_requested:
            try:
                integral = integrate(func, (x, a, b))
                exact = float(integral.evalf())
            except Exception:
                # No pudimos calcular el valor exacto
                pass

        # Convertir imagen estática a base64
        static_fig = simpson_static_plot(f_numeric, a, b, approx, exact)
        buffer = io.BytesIO()
        static_fig.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        buffer.close()
        plt.close(static_fig)

        # Gráfica interactiva (Plotly JSON)
        interactive_fig = simpson_interactive_plot(f_numeric, a, b, approx, exact)
        plot_json = interactive_fig.to_json()

        # Tabla de puntos
        x_values = [a, (a+b)/2, b]
        y_values = [f_numeric(xi) for xi in x_values]

        response = {
            "approx": approx,
            "image": image_base64,
            "plot_json": plot_json,
            "x_values": x_values,
            "original_y_values": y_values,
        }

        if exact is not None:
            response["exact"] = exact
            response["error_abs"] = abs(exact - approx)
            response["error_rel"] = abs(exact - approx) / abs(exact) * 100 if exact != 0 else float('inf')

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def simpson_tercio_simple_page(request):
    return render(request, "simpson_tercio_simple.html")