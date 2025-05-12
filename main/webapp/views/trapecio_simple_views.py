import base64
import io
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from sympy import exp, sin, cos, sinh, cosh, log, symbols, lambdify, sympify
import math

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


def generate_interactive_trapezoid_graph(func, a, b, max_subintervals=1, integral_value = 0):
    """
    Genera una visualización interactiva de la regla del trapecio.
    
    Args:
        func: función a integrar (expresión de sympy)
        a: límite inferior
        b: límite superior
        max_subintervals: número máximo de subintervalos a mostrar
    
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
                hoverinfo='none'
            )
        )

        # Calcular el máximo valor absoluto de la función para el rango y
        y_max = max(abs(original_y_values.min()),
                    abs(original_y_values.max())) * 1.1

        # Calcular el área exacta bajo la curva (integral analítica si está disponible)
        # try:
        #     # from sympy import integrate
        #     exact_integral = float(integrate(func, (x, a, b)))
        #     has_exact = True
        # except:
        #     has_exact = False

        # Guardar las anotaciones para cada paso
        annotations = []

        # Lista para almacenar los pasos del slider
        # steps = []
        # traces_per_step = []

        # Crear visualizaciones para diferentes números de subintervalos
        for n in range(1, max_subintervals + 1):
            integral_value, x_points, y_points = trapezoid_rule(func, a, b, n)

            trapezoid_traces = []

            # Añadir trapecios
            for j in range(len(x_points) - 1):
                trapezoid_traces.append(
                    go.Scatter(
                        x=[x_points[j], x_points[j], x_points[j+1],
                            x_points[j+1], x_points[j]],
                        y=[0, y_points[j], y_points[j+1], 0, 0],
                        fill="toself",
                        fillcolor='rgba(255, 0, 0, 0.2)',
                        line=dict(color='rgba(255, 0, 0, 0.5)'),
                        name=f"Trapecio {j+1}",
                        showlegend=False,
                        visible=False,
                        hoverinfo='none'
                    )
                )

            # Añadir puntos de evaluación
            points_trace = go.Scatter(
                x=x_points,
                y=y_points,
                mode='markers',
                marker=dict(size=8, color='red'),
                name='Puntos de evaluación',
                visible=False,
                hovertemplate='x: %{x:.4f}<br>f(x): %{y:.4f}'
            )

            # Añadir líneas verticales y horizontales
            vertical_lines = go.Scatter(
                x=np.repeat(x_points, 2),
                y=np.array([[0, y] for y in y_points]).flatten(),
                mode='lines',
                line=dict(color='red', width=1, dash='dash'),
                name='Líneas verticales',
                visible=False,
                showlegend=False,
                hoverinfo='none'
            )

            horizontal_line = go.Scatter(
                x=x_points,
                y=y_points,
                mode='lines',
                line=dict(color='red', width=2),
                name='Aproximación',
                visible=False,
                hoverinfo='none'
            )

            # Texto para mostrar la información de la integral
            annotation_text = f"Aproximación con {n} subintervalo{'s' if n > 1 else ''}: {integral_value:.6f}"

            # Guardar la anotación para este paso
            annotations.append(dict(
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
            ))

            # Añadir todas las trazas de este paso
            # traces_per_step.append(trapezoid_traces + [points_trace, vertical_lines, horizontal_line])

        # Agregar todas las trazas al gráfico y guardar sus índices
        # trace_indices = []
        # for traces in traces_per_step:
        #     idxs = []
        #     for trace in traces:
        #         fig.add_trace(trace)
        #         idxs.append(len(fig.data) - 1)
        #     trace_indices.append(idxs)

        # Configurar los pasos del slider
        # for i, idxs in enumerate(trace_indices):
        #     # Visibilidad: función original siempre visible, solo las trazas de este paso visibles
        #     visible = [True] + [False] * (len(fig.data) - 1)
        #     for idx in idxs:
        #         visible[idx] = True
        #     step = {
        #         'method': 'update',
        #         'args': [
        #             {'visible': visible},
        #             {'annotations': [annotations[i]],
        #              'title': f"Regla del Trapecio con {i+1} subintervalo{'s' if i+1 > 1 else ''}"}
        #         ],
        #         'label': str(i+1)
        #     }
        #     steps.append(step)

        # Configurar el layout
        title = f"Regla del Trapecio para ∫({a},{b}) {func} dx"
        title += f" (Valor exacto: {integral_value:.6f})"
           
        fig.update_layout(
            title=title,
            xaxis_title="x",
            yaxis_title="f(x)",
            sliders=[{
                'active': 0,
                'currentvalue': {"prefix": "Subintervalos: "},
                'pad': {"t": 50},
                # 'steps': steps
            }],
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            annotations=[annotations[0]]
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
    global x
    sym_func = None
    x = symbols('x')
    if request.method == "GET":
        try:
            # Obtener los valores del formulario
            func = request.GET.get("func")
            a = float(request.GET.get("a"))  # Transformar a float
            b = float(request.GET.get("b"))
            max_subintervals = int(request.GET.get("max_subintervals", 10))
            subintervals = list(map(int, request.GET.get(
                "subintervals", "1").split(",")))

            # Definir la función simbólica
            try:
                sym_func = sympify(func)
            except Exception as e:
                return JsonResponse({
                    "error": "Función no válida",
                    "message": "No se puede interpretar la función ingresada. Error: " + str(e)
                }, status=400)
               

            # Calcular las aproximaciones para cada número de subintervalos
            trapezoid_data = {}
            integral_value = 0
            for n in range(1, max_subintervals + 1):
                integral_value, x_points, y_points = trapezoid_rule(
                    sym_func, a, b, n)
                trapezoid_data[f"n={n}"] = {
                    "x_points": x_points.tolist(),
                    "y_points": y_points.tolist(),
                    "integral": float(integral_value)
                }

            # Calcular el valor exacto de la integral si es posible
            try:
                from sympy import integrate
                exact_integral = float(integrate(sym_func, (x, a, b)))
                exact_value = exact_integral
            except:
                exact_value = None

            # Generar gráficos
            graph_buffer = generate_trapezoid_graph(
                sym_func, a, b, subintervals, float(integral_value))
            plot_json = generate_interactive_trapezoid_graph(
                sym_func, a, b, max_subintervals, float(integral_value))

            # Convertir la imagen a base64
            image_base64 = base64.b64encode(
                graph_buffer.getvalue()).decode("utf-8")

            # Devolver la imagen y los datos tabulados
            response = {
                "image": image_base64,
                "plot_json": plot_json,
                "trapezoid_data": trapezoid_data,
                "exact_value": exact_value
            }
            return JsonResponse(response)
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


def trapecio_simple(request):
    return render(request, "trapecio-simple.html")