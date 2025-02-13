import numpy as np

from .equation_handler import EquationHandler
from .random_color import random_color

import plotly.graph_objects as go
from sympy import symbols, sympify, lambdify

eq_handler = EquationHandler()


def bisection_method_func(equation, tol=1e-6, p0=1.0, p1=2.5, max_iter=100):
    print(equation, p0, p1, tol, max_iter)
    try:
        print(f"Starting bisection method equation: ${equation}, a = {p0}, b = {p1}")
        eq_result = eq_handler.prepare_equation(equation)

        print(f"Equation result: {eq_result}")

        if not eq_result['success']:
            return {
                'error': True,
                'message': eq_result['message']
            }

        f = eq_result['function']

        # Evaluate initial points
        p0_result = eq_handler.evaluate_at_point(f, p0)
        p1_result = eq_handler.evaluate_at_point(f, p1)

        print(f"p0_result: {p0_result}")
        print(f"p1_result: {p1_result}")

        if not p0_result['success'] and not p1_result['success']:
            return {
                "error": True,
                "message": "Error evaluating function at initial points"
            }

        fp0 = float(p0_result['value'])
        fp1 = float(p1_result['value'])

        print(f"fp0: {fp0}")
        print(f"fp1: {fp1}")

        # Check if fp0 and fp1 >= 0
        if fp0 * fp1 >= 0:
            print("Los puntos iniciales no tienen una raiz")
            return {
                'error': True,
                'message': 'Initial points do not bracket a root'
            }

        results = {
            'iterations': [],
            'p0': float(p0),
            'p1': float(p1),
            'root': None,
            'converged': False
        }

        current_p0 = float(p0)
        current_p1 = float(p1)
        current_fp0 = fp0
        current_fp1 = fp1

        for i in range(max_iter):
            try:
                # Calculate c
                c = (current_p0 + current_p1) / 2

                # Evaluate c
                fc_result = eq_handler.evaluate_at_point(f, c)
                if not fc_result['success']:
                    return {
                        'error': True,
                        'message': 'Error evaluating function at c'
                    }

                fc = float(fc_result['value'])

                # Save results
                results['iterations'].append({
                    'iteration': i + 1,
                    'p0': current_p0,
                    'f(p0)': current_fp0,
                    'p1': current_p1,
                    'f(p1)': current_fp1,
                    'c': c,
                    'f(c)': fc
                })

                # Check if c is less than the tolerance
                if abs(fc) < tol or abs(current_p0 - current_p1) < tol:
                    results['converged'] = True
                    results['root'] = c
                    print(f"La función converge en {c}")
                    break

                # Establish new points
                if current_fp0 * fc < 0:
                    current_p1 = c
                    current_fp1 = fc
                else:
                    current_p0 = c
                    current_fp0 = fc


            except Exception as e:
                print(f"Error in iteration {i}: {str(e)}")
                return {
                    'error': True,
                    'message': f'Error in iteration {i}: {str(e)}'
                }

        if not results['converged']:
            results['message'] = 'Method did not converge within the maximum number of iterations'

        print(f"Calculation completed. Converged: {results['converged']}")

        return {
            'error': False,
            'message': 'Calculation completed successfully',
            'results': results
        }

    except Exception as e:
        print(f"Unexpected error in bisection_method_func: {str(e)}")
        return {
            'error': True,
            'message': f'Error processing request: {str(e)}'
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

        fig.add_trace(
            go.Scatter(
                x=[results['p1']],
                y=[original_function(results['p1'])],
                mode='markers',
                name='Punto inicial p1',
                marker=dict(color=random_color(), size=10)
            )
        )
        print("Punto inicial p1 agregado")

        iteration_colors = [random_color() for _ in range(len(results['iterations']))]

        print(iteration_colors)

        for i, iteration in enumerate(results['iterations']):
            # Point c
            fig.add_trace(
                go.Scatter(
                    x=[iteration['c']],
                    y=[original_function(iteration['c'])],
                    mode='markers',
                    name=f"Punto c - Iteración {i + 1}",
                    marker=dict(color=iteration_colors[i], size=8),
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
            visible_array = [True] * 3  # Original function and initial points always visible
            for j in range(2 * max_iterations):  # Two traces per iteration (point and line)
                visible_array.append(j <= (2 * i + 1))  # Show traces up to current iteration

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
