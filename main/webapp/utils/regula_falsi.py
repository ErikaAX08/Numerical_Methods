from sympy import symbols, sympify, lambdify
import logging

logger = logging.getLogger(__name__)

def regula_falsi_func(equation, a, b, tol=1e-6, max_iter=100, p0=1.0, p1=2.5):
    try:
        logger.info(f"Starting calculation with equation: {equation}, p0: {p0}, p1: {p1}")

        equation = equation.replace('^', '**')
        x = symbols('x')
        try:
            expr = sympify(equation)
            f = lambdify(x, expr)
        except Exception as e:
            logger.error(f"Error parsing equation: {str(e)}")
            return {
                'error': True,
                'message': f'Invalid equation format: {str(e)}'
            }

        try:
            fp0 = float(f(float(p0)))
            fp1 = float(f(float(p1)))
        except Exception as e:
            logger.error(f"Error evaluating function: {str(e)}")
            return {
                'error': True,
                'message': 'Error evaluating function at initial points'
            }

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
                p = current_p1 - current_fp1 * (current_p1 - current_p0) / (current_fp1 - current_fp0)
                fp = float(f(float(p)))

                results['iterations'].append({
                    'iteration': i + 1,
                    'p0': current_p0,
                    'p1': current_p1,
                    'p': p,
                    'f(p)': fp
                })

                if abs(fp) < tol:
                    results['converged'] = True
                    results['root'] = p
                    break

                if fp * current_fp0 < 0:
                    current_p1 = p
                    current_fp1 = fp
                else:
                    current_p0 = p
                    current_fp0 = fp

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