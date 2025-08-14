import base64
import io
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from sympy import exp, sin, cos, sinh, cosh, log, symbols, lambdify, sympify
from django.views.decorators.csrf import csrf_exempt

# Definir la variable simbólica
x = symbols('x')

def simpson_3_8_rule(func, a, b, n=3):
    """
    Implementa la regla de Simpson 3/8 para integración numérica.
    
    Args:
        func: función a integrar (expresión de sympy)
        a: límite inferior
        b: límite superior
        n: número de subintervalos (debe ser múltiplo de 3)
    
    Returns:
        Aproximación de la integral y los puntos utilizados
    """
    # Asegurar que n sea múltiplo de 3
    n = max(3, n - (n % 3))
    
    h = (b - a) / n
    x_points = np.linspace(a, b, n + 1)
    
    # Convertir la función simbólica a una función numérica
    f = lambdify(x, func, "numpy")
    y_points = f(x_points)
    
    # Aplicar la regla de Simpson 3/8 compuesto
    integral = 3 * h / 8 * (y_points[0] + 3 * np.sum(y_points[1:-1:3] + y_points[2:-1:3]) + 
               2 * np.sum(y_points[3:-1:3]) + y_points[-1])
    
    return integral, x_points, y_points

def generate_simpson_graph(func, a, b, subintervals):
    """
    Genera una visualización estática de la regla de Simpson 3/8.
    
    Args:
        func: función a integrar (expresión de sympy)
        a: límite inferior
        b: límite superior
        subintervals: lista de números de subintervalos a mostrar (múltiplos de 3)
    
    Returns:
        Buffer con la imagen PNG
    """
    try:
        import matplotlib.pyplot as plt

        # Crear una figura con varios subplots
        fig, axes = plt.subplots(len(subintervals), 1, figsize=(10, 3*len(subintervals)))
        if len(subintervals) == 1:
            axes = [axes]  # Para manejar el caso de un solo subplot

        # Función original para una curva suave
        original_function = lambdify(x, func, "numpy")
        original_x_values = np.linspace(a, b, 1000)
        original_y_values = original_function(original_x_values)

        # Calcular el área exacta bajo la curva (integral analítica si está disponible)
        try:
            from sympy import integrate
            exact_integral = float(integrate(func, (x, a, b)))
            has_exact = True
        except:
            has_exact = False

        for i, n in enumerate(subintervals):
            # Asegurar que n sea múltiplo de 3
            n = max(3, n - (n % 3))
            ax = axes[i]

            # Dibujar la función original
            ax.plot(original_x_values, original_y_values, 'b-', label=f"f(x) = {func}")

            # Calcular la regla de Simpson 3/8
            integral_value, x_points, y_points = simpson_3_8_rule(func, a, b, n)

            # Dibujar los polinomios cúbicos de interpolación
            for j in range(0, len(x_points) - 1, 3):
                xs = x_points[j:j+4]
                ys = y_points[j:j+4]
                
                # Crear polinomio de interpolación cúbico
                coefs = np.polyfit(xs, ys, 3)
                poly = np.poly1d(coefs)
                
                # Evaluar el polinomio en puntos intermedios para una curva suave
                x_interp = np.linspace(xs[0], xs[-1], 50)
                y_interp = poly(x_interp)
                
                # Dibujar la curva cúbica
                ax.plot(x_interp, y_interp, 'r-', linewidth=1)
                
                # Rellenar el área bajo la curva
                ax.fill_between(x_interp, 0, y_interp, alpha=0.2, color='r')

            # Dibujar los puntos de evaluación
            ax.plot(x_points, y_points, 'ro', markersize=5)

            # Configurar el gráfico
            ax.grid(True)
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)

            # Añadir título y leyenda
            title = f"Simpson 3/8 Compuesto con {n} subintervalos, ∫({a},{b}) = {integral_value:.6f}"
            if has_exact:
                error = abs(exact_integral - integral_value)
                title += f", Error: {error:.6f}"
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
        print(f"Error en generate_simpson_graph: {str(e)}")
        raise e

def generate_interactive_simpson_graph(func, a, b, max_subintervals=12):
    """
    Genera una visualización interactiva de la regla de Simpson 3/8.
    
    Args:
        func: función a integrar (expresión de sympy)
        a: límite inferior
        b: límite superior
        max_subintervals: número máximo de subintervalos a mostrar (múltiplo de 3)
    
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
        y_max = max(abs(original_y_values.min()), abs(original_y_values.max())) * 1.1

        # Calcular el área exacta bajo la curva (integral analítica si está disponible)
        try:
            from sympy import integrate
            exact_integral = float(integrate(func, (x, a, b)))
            has_exact = True
        except:
            has_exact = False

        # Lista para almacenar los pasos del slider
        steps = []
        annotations = []

        # Crear visualizaciones para diferentes números de subintervalos (múltiplos de 3)
        for n in range(3, max_subintervals + 1, 3):
            integral_value, x_points, y_points = simpson_3_8_rule(func, a, b, n)

            cubic_traces = []

            # Añadir polinomios cúbicos de interpolación
            for j in range(0, len(x_points) - 1, 3):
                xs = x_points[j:j+4]
                ys = y_points[j:j+4]
                
                # Crear polinomio de interpolación cúbico
                coefs = np.polyfit(xs, ys, 3)
                poly = np.poly1d(coefs)
                
                # Evaluar el polinomio en puntos intermedios para una curva suave
                x_interp = np.linspace(xs[0], xs[-1], 50)
                y_interp = poly(x_interp)
                
                # Añadir la curva cúbica
                cubic_traces.append(
                    go.Scatter(
                        x=x_interp,
                        y=y_interp,
                        mode='lines',
                        line=dict(color='red', width=2),
                        name='Aproximación cúbica',
                        showlegend=False,
                        visible=False,
                        hoverinfo='none'
                    )
                )
                
                # Añadir el área bajo la curva
                cubic_traces.append(
                    go.Scatter(
                        x=np.concatenate([x_interp, x_interp[::-1]]),
                        y=np.concatenate([y_interp, np.zeros_like(y_interp)[::-1]]),
                        fill='toself',
                        fillcolor='rgba(255, 0, 0, 0.2)',
                        line=dict(color='rgba(255, 0, 0, 0.5)'),
                        name='Área aproximada',
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

            # Texto para mostrar la información de la integral
            annotation_text = f"Aproximación con {n} subintervalos: {integral_value:.6f}"

            # Guardar la anotación para este paso
            annotations.append(dict(
                x=a + (b - a) / 2,
                y=y_max * 0.9,
                xref="x",
                yref="y",
                text=annotation_text,
                showarrow=False,
                font=dict(size=14, color="black"),
                align="center"
            ))

            # Añadir todas las trazas
            all_traces = cubic_traces + [points_trace]
            for trace in all_traces:
                fig.add_trace(trace)

            # Configurar el paso del slider
            step = {
                'method': 'update',
                'args': [
                    {'visible': [True] + [False] * len(fig.data[1:])},
                    {
                        'title': f"Simpson 3/8 Compuesto con {n} subintervalos",
                        'annotations': [annotations[(n//3)-1]]
                    }
                ],
                'label': str(n)
            }

            # Establecer visibilidad para este paso
            for j, _ in enumerate(fig.data):
                if j == 0:  # La función original siempre visible
                    step['args'][0]['visible'][j] = True
                elif j - 1 < len(all_traces):  # Solo las trazas actuales son visibles
                    step['args'][0]['visible'][j] = True

            steps.append(step)

        # Configurar el layout
        title = f"Simpson 3/8 Compuesto para ∫({a},{b}) {func} dx"
        if has_exact:
            title += f" (Valor exacto: {exact_integral:.6f})"

        fig.update_layout(
            title=title,
            xaxis_title="x",
            yaxis_title="f(x)",
            sliders=[{
                'active': 0,
                'currentvalue': {"prefix": "Subintervalos: "},
                'pad': {"t": 50},
                'steps': steps
            }],
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            annotations=[annotations[0]] if annotations else []
        )

        # Configurar los rangos de los ejes
        fig.update_xaxes(range=[a - 0.1 * (b-a), b + 0.1 * (b-a)])
        fig.update_yaxes(range=[-y_max, y_max])

        # Añadir una cuadrícula
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        # Hacer visible el primer conjunto de trazas
        for i in range(1, len(steps[0]['args'][0]['visible'])):
            if steps[0]['args'][0]['visible'][i]:
                fig.data[i].visible = True

        return fig.to_json()
    except Exception as e:
        print(f"Error en generate_interactive_simpson_graph: {str(e)}")
        raise e

@csrf_exempt
def calculate_simpson_3_8_compound(request):
    global x
    x = symbols('x')
    if request.method == "GET":
        try:
            func = request.GET.get("func")
            a = request.GET.get("a")
            b = request.GET.get("b")
            n = request.GET.get("n")

            # Validación de parámetros
            if func is None or a is None or b is None or n is None:
                return JsonResponse({"error": "Faltan parámetros requeridos."}, status=400)

            try:
                a = float(a)
                b = float(b)
                n = int(n)
            except Exception as e:
                return JsonResponse({"error": f"Parámetros numéricos inválidos: {str(e)}"}, status=400)

            # Parsear la función
            try:
                sym_func = sympify(func)
            except Exception as e:
                return JsonResponse({"error": f"Función no válida: {str(e)}"}, status=400)

            # Calcular la integral y los puntos para el n solicitado
            try:
                integral, x_points, y_points = simpson_3_8_rule(sym_func, a, b, n)
            except Exception as e:
                return JsonResponse({"error": f"Error en el cálculo numérico: {str(e)}"}, status=500)

            # Generar gráfico estático
            try:
                graph_buffer = generate_simpson_graph(sym_func, a, b, [n])
                image_base64 = base64.b64encode(graph_buffer.getvalue()).decode("utf-8")
            except Exception as e:
                image_base64 = ""
            
            # Generar gráfico interactivo
            try:
                plot_json = generate_interactive_simpson_graph(sym_func, a, b, max_subintervals=max(12, n))
            except Exception as e:
                plot_json = "{}"

            response = {
                "image": image_base64,
                "plot_json": plot_json,
                "x_values": x_points.tolist(),
                "original_y_values": y_points.tolist(),
                "integral": float(integral)
            }
            return JsonResponse(response)
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

def simpson_3_8_compound(request):
    return render(request, "simpson_3_8_compound.html")