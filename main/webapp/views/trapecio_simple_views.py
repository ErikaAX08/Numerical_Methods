import base64
import io
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from sympy import exp, sin, cos, sinh, cosh, log, symbols, lambdify, sympify
import math
from webapp.models import TrapecioHistorial

# Definir la variable simbólica
x = symbols('x')


def trapezoid_rule(func, a, b, n=1):
    """
    Implementa la regla del trapecio para integración numérica.
    
    Args:
        func: función a integrar (expresión de sympy)
        a: límite inferior
        b: límite superior
    
    Returns:
        Aproximación de la integral y los puntos utilizados
    """
    h = (b - a) 
    x_points = np.linspace(a, b)

    # Convertir la función simbólica a una función numérica
    f = lambdify(x, func, "numpy")
    y_points = f(x_points)

    # Aplicar la regla del trapecio
    integral = h/2 * (f(a) + f(b))
    return integral, x_points, y_points


def generate_trapezoid_graph(func, a, b, subintervals, integral_value):
    """
    Genera una visualización estática de la regla del trapecio.
    
    Args:
        func: función a integrar (expresión de sympy)
        a: límite inferior
        b: límite superior
        subintervals: lista de números de subintervalos a mostrar
    
    Returns:
        Buffer con la imagen PNG
    """
    try:
        import matplotlib.pyplot as plt

        # Crear una figura con varios subplots (uno para cada número de subintervalos)
        fig, axes = plt.subplots(len(subintervals), 1,
                                 figsize=(10, 3*len(subintervals)))
        if len(subintervals) == 1:
            axes = [axes]  # Para manejar el caso de un solo subplot

        # Función original para una curva suave
        original_function = lambdify(x, func, "numpy")
        original_x_values = np.linspace(a, b, 1000)
        original_y_values = original_function(original_x_values)

        # Calcular el área exacta bajo la curva (integral analítica si está disponible)
        # Esto es opcional y puede requerir cálculo simbólico
        try:
            from sympy import integrate
            exact_integral = float(integrate(func, (x, a, b)))
            has_exact = True
        except:
            has_exact = False

        for i, n in enumerate(subintervals):
            ax = axes[i]

            # Dibujar la función original
            ax.plot(original_x_values, original_y_values,
                    'b-', label=f"f(x) = {func}")

            # Calcular la regla del trapecio
            iv, x_points, y_points = trapezoid_rule(func, a, b, n)

            # Dibujar los trapecios
            for j in range(len(x_points) - 1):
                xs = [x_points[j], x_points[j], x_points[j+1], x_points[j+1]]
                ys = [0, y_points[j], y_points[j+1], 0]
                ax.fill(xs, ys, alpha=0.2, color='r')

            # Dibujar los puntos de evaluación
            ax.plot(x_points, y_points, 'ro', markersize=5)

            # Dibujar las líneas verticales para los trapezoides
            for j in range(len(x_points)):
                ax.plot([x_points[j], x_points[j]], [
                        0, y_points[j]], 'r--', alpha=0.5)

            # Dibujar las líneas horizontales para el valor de la función
            ax.plot(x_points, y_points, 'r-', linewidth=2)

            # Configurar el gráfico
            ax.grid(True)
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)

            # Añadir título y leyenda
            title = f"Regla del Trapecio con {n} subintervalo{'s' if n > 1 else ''}, ∫({a},{b}) = {integral_value:.6f}"
            ax.set_title(title)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()

        plt.tight_layout()

        # Guardar la figura en un buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=300)
        plt.close()
        buffer.seek(0)

        return buffer
    except Exception as e:
        print(f"Error en generate_trapezoid_graph: {str(e)}")
        raise e


def generate_interactive_trapezoid_graph(func, a, b, max_subintervals=1, integral_value=0):
    """
    Genera una visualización interactiva de la regla del trapecio mostrando
    toda la información de una sola vez.
    
    Args:
        func: función a integrar (expresión de sympy)
        a: límite inferior
        b: límite superior
        max_subintervals: número de subintervalos a mostrar
        integral_value: valor de la integral calculada
    
    Returns:
        JSON con el gráfico interactivo de Plotly
    """
    try:
        import plotly.graph_objects as go

        # Crear una figura de Plotly
        fig = go.Figure()

        # Función original para una curva suave
        original_function = lambdify(x, func, "numpy")
        original_x_values = np.linspace(a, b, 1000)
        original_y_values = original_function(original_x_values)

        # Añadir la curva original
        fig.add_trace(
            go.Scatter(
                x=original_x_values,
                y=original_y_values,
                name=f"f(x) = {func}",
                line=dict(color='blue', width=2),
                hovertemplate='x: %{x:.4f}<br>f(x): %{y:.4f}'
            )
        )

        # Calcular el máximo valor absoluto de la función para el rango y
        y_max = max(abs(original_y_values.min()),
                    abs(original_y_values.max())) * 1.1

        # Calcular la regla del trapecio
        integral_value, x_points, y_points = trapezoid_rule(func, a, b, max_subintervals)

        # Añadir trapecios
        for j in range(len(x_points) - 1):
            fig.add_trace(
                go.Scatter(
                    x=[x_points[j], x_points[j], x_points[j+1],
                        x_points[j+1], x_points[j]],
                    y=[0, y_points[j], y_points[j+1], 0, 0],
                    fill="toself",
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    line=dict(color='rgba(255, 0, 0, 0.5)'),
                    name=f"Trapecio {j+1}",
                    showlegend=(j == 0),  # Solo mostrar uno en la leyenda
                    hoverinfo='none'
                )
            )

        # Añadir puntos de evaluación
        fig.add_trace(
            go.Scatter(
                x=x_points,
                y=y_points,
                mode='markers',
                marker=dict(size=8, color='red'),
                name='Puntos de evaluación',
                hovertemplate='x: %{x:.4f}<br>f(x): %{y:.4f}'
            )
        )

        # Añadir líneas verticales
        fig.add_trace(
            go.Scatter(
                x=np.repeat(x_points, 2),
                y=np.array([[0, y] for y in y_points]).flatten(),
                mode='lines',
                line=dict(color='red', width=1, dash='dash'),
                name='Líneas verticales',
                showlegend=True,
                hoverinfo='none'
            )
        )

        # Añadir línea horizontal (aproximación)
        fig.add_trace(
            go.Scatter(
                x=x_points,
                y=y_points,
                mode='lines',
                line=dict(color='red', width=2),
                name='Aproximación',
                hoverinfo='none'
            )
        )

        # Texto para mostrar la información de la integral
        annotation_text = f"Aproximación con {max_subintervals} subintervalo{'s' if max_subintervals > 1 else ''}: {integral_value:.6f}"

        # Configurar el layout
        title = f"Regla del Trapecio para ∫({a},{b}) {func} dx"
        title += f"<br>Valor aproximado: {integral_value:.6f}"
           
        fig.update_layout(
            title=title,
            xaxis_title="x",
            yaxis_title="f(x)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            annotations=[dict(
                x=a + (b-a)/2,
                y=y_max * 0.95,
                xref="x",
                yref="y",
                text=annotation_text,
                showarrow=False,
                font=dict(size=14, color="black"),
                align="center",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="black",
                borderwidth=1,
                borderpad=4
            )]
        )

        # Configurar los rangos de los ejes
        fig.update_xaxes(range=[a - 0.1 * (b-a), b + 0.1 * (b-a)])
        fig.update_yaxes(range=[-y_max, y_max])

        # Añadir una cuadrícula
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        return fig.to_json()
    except Exception as e:
        print(f"Error en generate_interactive_trapezoid_graph: {str(e)}")
        raise e


def calculate_trapezoid(request):
    # Si es GET con parámetros (cálculo desde el frontend)
    if request.method == "GET" and request.GET.get("func"):
        # Obtener los parámetros desde la URL
        func = request.GET.get("func")
        a = float(request.GET.get("a"))
        b = float(request.GET.get("b"))

        try:
            # Validar y convertir la función
            parsed_func = sympify(func)

            # Crear función evaluable
            f = lambdify(x, parsed_func, "numpy")

            # Aplicar la regla del trapecio
            integral_value, x_values, y_values = trapezoid_rule(
                parsed_func, a, b, 1)

            # Generar el gráfico estático
            plot_buffer = generate_trapezoid_graph(
                parsed_func, a, b, [1], integral_value)
            plot_image = base64.b64encode(
                plot_buffer.getvalue()).decode('utf-8')

            # Generar el gráfico interactivo
            plot_json = generate_interactive_trapezoid_graph(
                parsed_func, a, b, 1, integral_value)

            # Guardar en historial
            TrapecioHistorial.objects.create(
                funcion=func,
                limite_inferior=a,
                limite_superior=b,
                subintervalos=1,
                resultado=float(integral_value)
            )

            # Devolver los resultados como JSON
            return JsonResponse({
                "error": None,
                "integral_value": float(integral_value),
                "x_values": x_values.tolist(),
                "original_y_values": y_values.tolist(),
                "image": plot_image,
                "plot_json": plot_json
            })

        except Exception as e:
            return JsonResponse({"error": str(e)})

    # Si es GET sin parámetros (petición AJAX para cargar últimos valores usados)
    elif request.method == "GET" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        ultimo = TrapecioHistorial.objects.order_by("-id").first()
        if ultimo:
            return JsonResponse({
                "funcion": ultimo.funcion,
                "limite_inferior": ultimo.limite_inferior,
                "limite_superior": ultimo.limite_superior,
                "subintervalos": ultimo.subintervalos
            })
        else:
            return JsonResponse({"error": "No hay datos guardados"})

    # Vista inicial
    return render(request, "trapecio-simple.html")

def trapecio_simple(request):
    return render(request, "trapecio-simple.html")