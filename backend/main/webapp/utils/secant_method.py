import numpy as np
from sympy import symbols, sympify, lambdify
import plotly.graph_objects as go

from .equation_handler import EquationHandler
from .random_color import random_color

eq_handler = EquationHandler()


def secant_method_func(equation, tol, p0, p1, max_iter):
    try:
        print("Starting secant_method_fun")

        eq_result = eq_handler.prepare_equation(equation)
        print("eq_result: ", eq_result)

        if not eq_result['success']:
            return {
                "error": True,
                "message": eq_result['message']
            }

        f = eq_result['function']

        p0_result = eq_handler.evaluate_at_point(f, p0)
        p1_result = eq_handler.evaluate_at_point(f, p1)

        print("p0_result: ", p0_result)
        print("p1_result: ", p1_result)

        if not p0_result['success'] and not p1_result['success']:
            return {
                "error": True,
                "message": "Error evaluating function at initial points"
            }

        fp0 = float(p0_result['value'])
        fp1 = float(p1_result['value'])

        print("fp0: ", fp0)
        print("fp1: ", fp1)

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

        # Current points
        current_p0 = float(p0)
        current_p1 = float(p1)
        current_fp0 = fp0
        current_fp1 = fp1

        for i in range(max_iter):
            try:
                # Print that calculation is start
                x2 = current_p1 - current_fp1 * (current_p1 - current_p0) / (current_fp1 - current_fp0)
                print("x2: ", x2)

                fx2 = float(f(x2))
                print("fx2: ", fx2)

                results['iterations'].append({
                    'iteration': i + 1,
                    'p0': current_p0,
                    'f(p0)': current_fp0,
                    'f(p1)': current_fp1,
                    'p1': current_p1,
                    'c': x2,
                    'f(c)': fx2
                })

                if abs(current_p0 - current_p1) < tol:
                    results['converged'] = True
                    results['root'] = x2
                    print("La funcion si converge")
                    break

                current_p0 = current_p1
                current_p1 = x2
                current_fp0 = current_fp1
                current_fp1 = fx2

            except Exception as e:
                print(f"Error in iteration {i}: {str(e)}")
                return {
                    'error': True,
                    'message': f'Unexpected error in iteration {i}: {str(e)}'
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
        print(e)
        return {
            'error': True,
            'message': f'Unexpected error: {str(e)}'
        }


def generate_graph(equation, a, b, results):
    print("generate_graph_fun")
    try:
        equation = equation.replace('^', '**')

        # Render original function
        x = symbols('x')
        original_function = lambdify(x, sympify(equation), "numpy")
        original_x_values = np.linspace(a, b, 1000)
        original_y_values = original_function(original_x_values)

        fig = go.Figure()
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
                marker=dict(color='red', size=10)
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

            # Line for current iteration
            fig.add_trace(
                go.Scatter(
                    x=[iteration['p0'], iteration['p1']],
                    y=[original_function(iteration['p0']), original_function(iteration['p1'])],
                    mode='lines',
                    name=f"Línea - Iteración {i + 1}",
                    line=dict(color=iteration_colors[i], width=1),
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
        print(e)
        return {
            'error': True,
            'message': f'Unexpected error: {str(e)}'
        }
