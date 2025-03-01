from .equation_handler import EquationHandler
from .random_color import random_color

import numpy as np
import plotly.graph_objects as go
import sympy as sp
from sympy import symbols, sympify, lambdify

# Crear una instancia de EquationHandler
eq_handler = EquationHandler()


def divided_differences_method_func(equation, tol=1e-6, max_iter=100, p0=1.0):
    try:
        print(
            f"Iniciando método de Newton-Raphson para la ecuación: {equation}, p0 = {p0}")

        # Preparar la ecuación
        eq_result = eq_handler.prepare_equation(equation)
        print(f"Resultado de preparar la ecuación: {eq_result}")

        if not eq_result['success']:
            return {
                'error': True,
                'message': eq_result['message']
            }

        # Obtener la función y su derivada
        f = eq_result['function']
        f_expr = eq_result['expression']
        df_expr = sp.diff(f_expr, eq_handler.x)
        df = sp.lambdify(eq_handler.x, df_expr, 'numpy')

        # Evaluar la funcion en el punto inicial
        p0_result = eq_handler.evaluate_at_point(f, p0)
        print(f"Resultado de evaluar en p0: {p0_result}")

        if not p0_result['success']:
            return {
                'error': True,
                'message': 'Error al evaluar la función en el punto inicial.'
            }

        # Inicializar resultados
        results = {
            'iterations': [],
            'p0': float(p0),
            'dp0': float(df(p0)),
            'dp1': None,
            'p1': None,
            'f(p0)': float(p0_result['value']),
            'f(p1)': None,
            'root': None,
            'converged': False
        }

        # Iteraciones del método de Newton-Raphson
        for i in range(max_iter):
            try:
                # Evaluar la funcion y su derivada en p0
                fp0 = f(p0)
                dfp0 = df(p0)

                print(f"derivada: {dfp0}")

                # Evitar division por cero
                if abs(dfp0) < 1e-10:
                    return {
                        'error': True,
                        'message': 'La derivada es cero. El método falla.'
                    }

                # Calcular la nueva aproximacion
                x1 = p0 - (fp0 / dfp0)

                print(f"Iteración {i + 1}: x1 = {x1}")

                # Guardar los resultados de la iteracion
                results['iterations'].append({
                    'iteration': i + 1,
                    'p0': p0,
                    'dp0': dfp0,
                    'p1': x1,
                    'dp1': df(x1),
                    'f(p0)': float(fp0),
                    'f(p1)': float(f(x1)),
                    'root': None,
                    'converged': False
                })

                # Verificar convergencia
                if abs(x1 - p0) < tol:
                    results['root'] = x1
                    results['converged'] = True
                    return {
                        'error': False,
                        'message': 'Cálculo completado exitosamente.',
                        'results': results
                    }

                # Actualizar p0 para la siguiente iteracion
                p0 = x1

            except Exception as e:
                print(f"Error en la iteración {i + 1}: {str(e)}")
                return {
                    'error': True,
                    'message': f'Error en la iteración {i + 1}: {str(e)}'
                }

        # Si se alcanza el maximo de iteraciones sin converger
        return {
            'error': False,
            'message': 'Se alcanzó el número máximo de iteraciones sin converger.',
            'results': results
        }

    except Exception as e:
        print(f"Error en newton_raphson_method_func: {str(e)}")
        return {
            'error': True,
            'message': f'Error procesando la solicitud: {str(e)}'
        }


def generate_graph(equation, a, b, results):
    print(equation, a, b, results)

    try:
        equation = equation.replace('^', '**')
        print(equation)

        x = symbols('x')
        original_function = lambdify(x, sympify(equation), "numpy")
        original_x_values = np.linspace(a, b, 1000)
        original_y_values = original_function(original_x_values)

        fig = go.Figure()

        # Add original function trace
        fig.add_trace(
            go.Scatter(
                x=original_x_values,
                y=original_y_values,
                mode='lines',
                name='Función original',
                line=dict(color='black')
            )
        )
        print("Funcion original agregada")

        # Add initial points
        fig.add_trace(
            go.Scatter(
                x=[results['p0']],
                y=[original_function(results['p0'])],
                mode='markers',
                name='Punto inicial p0',
                marker=dict(color=random_color(), size=10)
            )
        )
        print("Punto inicial p0 agregado")

        iteration_colors = [random_color()
                            for _ in range(len(results['iterations']))]

        print(iteration_colors)
        print(results)

        for i, iteration in enumerate(results['iterations']):
            print(
                f"Iteracion {i + 1}: p0 = {iteration['p0']}, p1 = {iteration['p1']}")

            # Point c
            fig.add_trace(
                go.Scatter(
                    x=[iteration['p1']],
                    y=[original_function(iteration['p1'])],
                    mode='markers',
                    name=f"Punto c - Iteración {i + 1}",
                    marker=dict(color=iteration_colors[i], size=8),
                    visible=False
                )
            )

            # Draw
            fig.add_trace(
                go.Scatter(
                    x=original_x_values,
                    y=generate_tangent_line_graph(
                        iteration['p0'],
                        iteration['dp0'],
                        iteration['f(p0)'],
                        original_x_values),
                    mode='lines',
                    name=f"Línea - Iteración {i + 1}",
                    line=dict(color=iteration_colors[i], width=2),
                    visible=False
                )
            )

        # Create slider steps
        steps = []
        max_iterations = len(results['iterations'])

        # Initial state
        visible_array = [True] * 3
        visible_array.extend([False] * (2 * max_iterations))

        steps.append(dict(
            method="update",
            args=[{"visible": visible_array}, {"title": "Estado inicial"}],
            label="Estado inicial"
        ))

        # Add steps for each iteration
        for i in range(max_iterations):
            # Original function and initial points always visible
            visible_array = [True] * 3
            # Two traces per iteration (point and line)
            for j in range(2 * max_iterations):
                # Show traces up to current iteration
                visible_array.append(j <= (2 * i + 1))

            steps.append(dict(
                method="update",
                args=[{"visible": visible_array},
                      {"title": f"Iteración {i + 1}"}],
                label=str(i + 1)
            ))

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Iteración: "},
            pad={"t": 50},
            steps=steps
        )]

        fig.update_layout(
            title="Aproximación de la raíz",
            xaxis_title="x",
            yaxis_title="f(x)",
            sliders=sliders,
            xaxis_range=[a, b],
            margin=dict(l=20, r=20, t=50, b=50),
        )

        return fig.to_json()

    except Exception as e:
        print(f"Unexpected error in generate_graph: {str(e)}")
        raise e


def generate_tangent_line_graph(a, slope, y_a, x):
    return y_a + slope * (x - a)
