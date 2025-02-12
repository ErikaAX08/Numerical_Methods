import logging
import random

import numpy as np
import plotly.graph_objects as go
from sympy import symbols, sympify, lambdify

from .equation_handler import EquationHandler

eq_handler = EquationHandler()
logger = logging.getLogger(__name__)
x = symbols('x')


def regula_falsi_func(equation, tol=1e-6, max_iter=100, p0=1.0, p1=2.5):
    try:
        # Print that calculation is start
        logger.info(f"Starting calculation with equation: {equation}, p0: {p0}, p1: {p1}")

        eq_result = eq_handler.prepare_equation(equation)
        print(eq_result)

        if not eq_result['success']:
            return {
                'error': True,
                'message': eq_result['message']
            }

        f = eq_result['function']

        # Evaluate initial points
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
                c = (current_p0 * current_fp1 - current_p1 * current_fp0) / (current_fp1 - current_fp0)
                # Evaluate c
                fc = float(f(float(c)))

                # Save results
                results['iterations'].append({
                    'iteration': i + 1,
                    'p0': current_p0,
                    'f(p0)': current_fp0,
                    'f(p1)': current_fp1,
                    'p1': current_p1,
                    'c': c,
                    'f(c)': fc
                })

                # Check if c is less than the tolerance
                if abs(fc) < tol:
                    # If yes, c is the root and indicate that the function converges
                    results['converged'] = True
                    results['root'] = c
                    print("La funcion si converge")
                    break

                # Establish new points
                if fc * current_fp0 < 0:
                    current_p1 = c
                    current_fp1 = fc
                else:
                    # When f(b) * f(c) < 0
                    current_p0 = c
                    current_fp0 = fc

            except Exception as e:
                logger.error(f"Error in iteration {i}: {str(e)}")
                print("Error in iteration {i}: {str(e)}")
                return {
                    'error': True,
                    'message': f'Error in iteration {i}: {str(e)}'
                }

        if not results['converged']:
            results['message'] = 'Method did not converge within the maximum number of iterations'

        logger.info(f"Calculation completed. Converged: {results['converged']}")
        return {
            'error': False,
            'message': 'Calculation completed successfully',
            'results': results
        }

    except Exception as e:
        logger.error(f"Unexpected error in regula_falsi_func: {str(e)}")
        return {
            'error': True,
            'message': f'Unexpected error: {str(e)}'
        }


def regula_falsi_modified_func(equation, tol=1e-6, max_iter=100, p0=1.0, p1=2.5):
    try:
        # Print that calculation is start
        logger.info(f"Starting calculation with equation: {equation}, p0: {p0}, p1: {p1}")

        eq_result = eq_handler.prepare_equation(equation)
        if not eq_result['success']:
            return {
                'error': True,
                'message': eq_result['message']
            }

        f = eq_result['function']

        p0_result = eq_handler.evaluate_at_point(f, p0)
        p1_result = eq_handler.evaluate_at_point(f, p1)

        if not p0_result['success'] and p1_result['success']:
            return {
                "error": True,
                "message": "Error evaluating function at initial points"
            }

        fp0 = p0_result['value']
        fp1 = p1_result['value']

        # Check if fp0 and fp1 >= 0
        if fp0 * fp1 >= 0:
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
                c = (current_p0 * current_fp1 - current_p1 * current_fp0) / (current_fp1 - current_fp0)
                # Evaluate c
                fc = float(f(float(c)))

                # Save results
                results['iterations'].append({
                    'iteration': i + 1,
                    'p0': current_p0,
                    'f(p0)': current_fp0,
                    'f(p1)': current_fp1,
                    'p1': current_p1,
                    'c': c,
                    'f(c)': fc
                })

                # Check if c is equal to 0
                if abs(fc) < tol:
                    # If yes, c is the root and indicate that the function converges
                    results['converged'] = True
                    results['root'] = c
                    break

                # Establish new points
                if fc * current_fp0 < 0:
                    # When f(a) * f(c) < 0
                    current_p1 = c
                    current_fp0 = current_fp0 / 2
                else:
                    # When f(b) * f(c) < 0
                    current_p0 = c
                    current_fp1 = current_fp1 / 2

            except Exception as e:
                logger.error(f"Error in iteration {i}: {str(e)}")
                return {
                    'error': True,
                    'message': f'Error in iteration {i}: {str(e)}'
                }

        if not results['converged']:
            results['message'] = 'Method did not converge within the maximum number of iterations'

        logger.info(f"Calculation completed. Converged: {results['converged']}")
        return {
            'error': False,
            'message': 'Calculation completed successfully',
            'results': results
        }

    except Exception as e:
        logger.error(f"Unexpected error in regula_falsi__modified_func: {str(e)}")
        return {
            'error': True,
            'message': f'Unexpected error: {str(e)}'
        }


def generate_graph(equation, a, b, results):
    try:

        # Function to generate random colors
        def random_color():
            return f'rgb({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)})'

        equation = equation.replace('^', '**')

        # Convert equation to numeric function
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
                name="Función original",
                line=dict(color='black')
            )
        )

        # Add initial points
        fig.add_trace(
            go.Scatter(
                x=[results['p0']],
                y=[original_function(results['p0'])],
                mode='markers',
                name="Punto inicial p0",
                marker=dict(color=random_color(), size=10)
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[results['p1']],
                y=[original_function(results['p1'])],
                mode='markers',
                name="Punto inicial p1",
                marker=dict(color=random_color(), size=10)
            )
        )

        # Generate random colors for iterations
        iteration_colors = [random_color() for _ in range(len(results['iterations']))]

        # Add a trace for each iteration point and line
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

        # Initial state (only original function and initial points)
        visible_array = [True] * 3  # Original function and two initial points
        visible_array.extend([False] * (2 * max_iterations))  # Hide all iteration traces

        steps.append(dict(
            method="update",
            args=[{"visible": visible_array},
                  {"title": "Estado inicial"}],
            label="Inicio"
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
        print(f"Error en generate_graph: {str(e)}")
        raise e
