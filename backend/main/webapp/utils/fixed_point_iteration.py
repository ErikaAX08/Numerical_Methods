from .equation_handler import EquationHandler
from .random_color import random_color

import numpy as np
import plotly.graph_objects as go
import sympy as sp
from sympy import symbols, sympify, lambdify

eq_handler = EquationHandler()


def fixed_point_iteration_method(equation, tol=1e-6, max_iter=100, x0=1.0):
    try:
        print(f"Iniciando método de Punto Fijo para la ecuación: {equation}, x0 = {x0}")

        # Preparar la ecuación g(x)
        eq_result = eq_handler.prepare_equation(equation)
        print(f"Resultado de preparar la ecuación: {eq_result}")

        if not eq_result['success']:
            return {
                'error': True,
                'message': eq_result['message']
            }

        # Obtener la función g(x)
        g = eq_result['function']
        g_expr = eq_result['expression']

        # Inicializar resultados
        results = {
            'iterations': [],
            'x0': float(x0),
            'root': None,
            'converged': False
        }

        # Iteraciones del método de punto fijo
        x_n = x0
        for i in range(max_iter):
            try:
                # Calcular x_{n+1} = g(x_n)
                x_n1 = float(g(x_n))
                error = abs(x_n1 - x_n)

                # Guardar los resultados de la iteración
                results['iterations'].append({
                    'iteration': i + 1,
                    'x_n': x_n,
                    'x_n1': x_n1,
                    'g(x)': x_n1,
                    'error': error
                })

                # Verificar convergencia
                if error < tol:
                    results['root'] = x_n1
                    results['converged'] = True
                    return {
                        'error': False,
                        'message': 'Cálculo completado exitosamente.',
                        'results': results
                    }

                x_n = x_n1

            except Exception as e:
                return {
                    'error': True,
                    'message': f'Error en la iteración {i + 1}: {str(e)}'
                }

        return {
            'error': False,
            'message': 'Se alcanzó el número máximo de iteraciones sin converger.',
            'results': results
        }

    except Exception as e:
        print(f"Error en fixed_point_iteration_method: {str(e)}")
        return {
            'error': True,
            'message': f'Error procesando la solicitud: {str(e)}'
        }


def generate_graph(equation, a, b, results):
    try:
        equation = equation.replace('^', '**')
        x = symbols('x')
        g_function = lambdify(x, sympify(equation), "numpy")
        x_values = np.linspace(a, b, 1000)
        y_values = g_function(x_values)

        fig = go.Figure()

        # Add y = g(x)
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines',
                name='g(x)',
                line=dict(color='blue')
            )
        )

        # Add y = x line
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=x_values,
                mode='lines',
                name='y = x',
                line=dict(color='black', dash='dash')
            )
        )

        # Add initial point
        fig.add_trace(
            go.Scatter(
                x=[results['x0']],
                y=[g_function(results['x0'])],
                mode='markers',
                name='Punto inicial x₀',
                marker=dict(color=random_color(), size=10)
            )
        )

        # Add convergence point if method converged
        if results.get('converged', False) and results.get('root') is not None:
            root = results['root']
            fig.add_trace(
                go.Scatter(
                    x=[root],
                    y=[g_function(root)],
                    mode='markers',
                    name='Punto de convergencia',
                    marker=dict(
                        color='green',
                        size=12,
                        symbol='star',
                        line=dict(color='darkgreen', width=2)
                    )
                )
            )

        # Add iteration points and lines
        for i, iter in enumerate(results['iterations']):
            color = random_color()
            x_n = iter['x_n']
            x_n1 = iter['x_n1']

            # Vertical line from (x_n, x_n) to (x_n, g(x_n))
            fig.add_trace(
                go.Scatter(
                    x=[x_n, x_n],
                    y=[x_n, g_function(x_n)],
                    mode='lines',
                    name=f'Iteración {i + 1}',
                    line=dict(color=color, dash='dot'),
                    showlegend=False
                )
            )

            # Horizontal line from (x_n, g(x_n)) to (x_n1, g(x_n))
            fig.add_trace(
                go.Scatter(
                    x=[x_n, x_n1],
                    y=[g_function(x_n), g_function(x_n)],
                    mode='lines',
                    line=dict(color=color, dash='dot'),
                    showlegend=False
                )
            )

        fig.update_layout(
            title="Método de Iteración de Punto Fijo",
            xaxis_title="x",
            yaxis_title="g(x)",
            showlegend=True,
            xaxis_range=[a, b],
            yaxis_range=[a, b],
            margin=dict(l=20, r=20, t=50, b=50),
            annotations=[
                dict(
                    x=results.get('root', 0),
                    y=g_function(results.get('root', 0)) if results.get('root') else 0,
                    text=f"Convergencia: ({results.get('root', 'No convergió'):.6f})",
                    showarrow=True,
                    arrowhead=1,
                    ax=0,
                    ay=-40,
                    visible=results.get('converged', False)
                )
            ] if results.get('converged', False) else []
        )

        return fig.to_json()

    except Exception as e:
        print(f"Error in generate_graph: {str(e)}")
        raise e
