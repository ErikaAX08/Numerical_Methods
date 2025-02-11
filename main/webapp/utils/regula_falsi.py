import numpy as np

import plotly.graph_objects as go

from sympy import symbols, sympify, lambdify
import logging

logger = logging.getLogger(__name__)
x = symbols('x')


def regula_falsi_func(equation, tol=1e-6, max_iter=100, p0=1.0, p1=2.5):
    try:
        # Print that calculation is start
        logger.info(f"Starting calculation with equation: {equation}, p0: {p0}, p1: {p1}")

        equation = equation.replace('^', '**')
        try:
            expr = sympify(equation)
            f = lambdify(x, expr)
        except Exception as e:
            logger.error(f"Error parsing equation: {str(e)}")
            return {
                'error': True,
                'message': f'Invalid equation format: {str(e)}'
            }

        # Evaluating p0 y p1 with function
        try:
            fp0 = float(f(float(p0)))
            fp1 = float(f(float(p1)))
        except Exception as e:
            logger.error(f"Error evaluating function: {str(e)}")
            return {
                'error': True,
                'message': 'Error evaluating function at initial points'
            }

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

                # Check if c is less than the tolerance
                if abs(fc) < tol:
                    # If yes, c is the root and indicate that the function converges
                    results['converged'] = True
                    results['root'] = c
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
                return {
                    'error': True,
                    'message': f'Error in iteration {i}: {str(e)}'
                }

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

        equation = equation.replace('^', '**')
        try:
            expr = sympify(equation)
            f = lambdify(x, expr)
        except Exception as e:
            logger.error(f"Error parsing equation: {str(e)}")
            return {
                'error': True,
                'message': f'Invalid equation format: {str(e)}'
            }

        # Evaluating p0 y p1 with function
        try:
            fp0 = float(f(float(p0)))
            fp1 = float(f(float(p1)))
        except Exception as e:
            logger.error(f"Error evaluating function: {str(e)}")
            return {
                'error': True,
                'message': 'Error evaluating function at initial points'
            }

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


"""""
def generate_graph(equation, a, b, results_regula_falsi, results_regula_falsi_modified):
    try:
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
                x=[results_regula_falsi['p0'], results_regula_falsi['p1']],
                y=[original_function(results_regula_falsi['p0']), original_function(results_regula_falsi['p1'])],
                mode='markers',
                name="Puntos iniciales",
                marker=dict(color='blue', size=10)
            )
        )

        # Regula Falsi traces
        rf_c_values_x = []
        rf_c_values_y = []
        rf_lines_x = []
        rf_lines_y = []
        for iteration in results_regula_falsi['iterations']:
            rf_c_values_x.append(iteration['c'])
            rf_c_values_y.append(original_function(iteration['c']))
            rf_lines_x.extend([iteration['p0'], iteration['p1'], None])
            rf_lines_y.extend([original_function(iteration['p0']), original_function(iteration['p1']), None])

        fig.add_trace(
            go.Scatter(
                x=rf_c_values_x,
                y=rf_c_values_y,
                mode='markers+lines',
                name="Puntos c (Regla Falsa)",
                marker=dict(color='red', size=8),
                line=dict(color='red', dash='dash'),
                visible=False
            )
        )

        fig.add_trace(
            go.Scatter(
                x=rf_lines_x,
                y=rf_lines_y,
                mode='lines',
                name="Líneas (Regla Falsa)",
                line=dict(color='orange', width=1),
                visible=False
            )
        )

        # Regula Falsi Modified traces
        rfm_c_values_x = []
        rfm_c_values_y = []
        rfm_lines_x = []
        rfm_lines_y = []
        for iteration in results_regula_falsi_modified['iterations']:
            rfm_c_values_x.append(iteration['c'])
            rfm_c_values_y.append(original_function(iteration['c']))
            rfm_lines_x.extend([iteration['p0'], iteration['p1'], None])
            rfm_lines_y.extend([original_function(iteration['p0']), original_function(iteration['p1']), None])

        fig.add_trace(
            go.Scatter(
                x=rfm_c_values_x,
                y=rfm_c_values_y,
                mode='markers+lines',
                name="Puntos c (Regla Falsa Modificada)",
                marker=dict(color='green', size=8),
                line=dict(color='green', dash='dot'),
                visible=False
            )
        )

        fig.add_trace(
            go.Scatter(
                x=rfm_lines_x,
                y=rfm_lines_y,
                mode='lines',
                name="Líneas (Regla Falsa Modificada)",
                line=dict(color='purple', width=1),
                visible=False
            )
        )

        # Create slider steps
        steps = []
        max_iterations = max(len(results_regula_falsi['iterations']), len(results_regula_falsi_modified['iterations']))
        for i in range(max_iterations + 1):  # +1 to include initial state
            step = dict(
                method="update",
                args=[{"visible": [True, True] +  # Original function and initial points are always visible
                                  [j < i for j in range(2, 4)] +  # RF: points and lines
                                  [j < i for j in range(4, 6)]},  # RFM: points and lines
                      {"title": f"Iteración: {i}"}],
                label=str(i)
            )
            steps.append(step)

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
            margin=dict(l=20, r=20, t=50, b=50),  # Adjust margins here
        )

        return fig.to_json()

    except Exception as e:
        print(f"Error en generate_graph: {str(e)}")
        raise e
"""""


def generate_graph(equation, a, b, results):
    try:
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
                x=[results['p0'], results['p1']],
                y=[original_function(results['p0']), original_function(results['p1'])],
                mode='markers',
                name="Puntos iniciales",
                marker=dict(color='blue', size=10)
            )
        )

        # Regula Falsi traces
        rf_c_values_x = []
        rf_c_values_y = []
        rf_lines_x = []
        rf_lines_y = []
        for iteration in results['iterations']:
            rf_c_values_x.append(iteration['c'])
            rf_c_values_y.append(original_function(iteration['c']))
            rf_lines_x.extend([iteration['p0'], iteration['p1'], None])
            rf_lines_y.extend([original_function(iteration['p0']), original_function(iteration['p1']), None])

        fig.add_trace(
            go.Scatter(
                x=rf_c_values_x,
                y=rf_c_values_y,
                mode='markers+lines',
                name="Puntos c (Regla Falsa)",
                marker=dict(color='red', size=8),
                line=dict(color='red', dash='dash'),
                visible=False
            )
        )

        fig.add_trace(
            go.Scatter(
                x=rf_lines_x,
                y=rf_lines_y,
                mode='lines',
                name="Líneas (Regla Falsa)",
                line=dict(color='orange', width=1),
                visible=False
            )
        )

        # Create slider steps
        steps = []
        max_iterations = len(results['iterations'])
        for i in range(max_iterations + 1):  # +1 to include initial state
            step = dict(
                method="update",
                args=[{"visible": [True, True] +  # Original function and initial points are always visible
                                  [j < i for j in range(2, 4)] +  # RF: points and lines
                                  [j < i for j in range(4, 6)]},  # RFM: points and lines
                      {"title": f"Iteración: {i}"}],
                label=str(i)
            )
            steps.append(step)

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
            margin=dict(l=20, r=20, t=50, b=50),  # Adjust margins here
        )

        return fig.to_json()

    except Exception as e:
        print(f"Error en generate_graph: {str(e)}")
        raise e
