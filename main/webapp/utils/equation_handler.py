from sympy import symbols, sympify, lambdify, parse_expr, exp
import logging
from typing import Dict, Union, Callable
import re

logger = logging.getLogger(__name__)


class EquationHandler:
    def __init__(self):
        self.x = symbols('x')

    def prepare_equation(self, equation: str) -> Dict[str, Union[bool, str, Callable]]:
        """
        Prepares and validates a mathematical equation for computation.
        Handles a wide variety of mathematical expressions including decimals.

        Args:
            equation (str): The mathematical equation to process

        Returns:
            Dict containing:
                - success (bool): Whether the equation was successfully processed
                - message (str): Status message or error description
                - function (Callable, optional): Lambda function of the processed equation
                - expression (sympy.Expr, optional): Sympy expression of the equation
        """
        try:
            # Remove whitespace and validate basic structure
            equation = equation.strip()
            if not equation:
                return {
                    'success': False,
                    'message': 'Equation cannot be empty'
                }

            # Replace common mathematical notations
            replacements = {
                '^': '**',  # Power operator
                '÷': '/',  # Division
                '×': '*',  # Multiplication
                '−': '-',  # Minus sign
                '√': 'sqrt',  # Square root
                ',': '.',  # Replace comma with decimal point
                ' ': '',  # Remove spaces
            }

            for old, new in replacements.items():
                equation = equation.replace(old, new)

            # Reemplazar e^x por exp(x)
            equation = re.sub(r'e\*\*(\w+)', r'exp(\1)', equation)

            # Pre-process special functions
            special_functions = {
                'sen': 'sin',  # Spanish trigonometric functions
                'tg': 'tan',
                'arctg': 'atan',
                'arcsen': 'asin',
                'arccos': 'acos',
                'ln': 'log'
            }

            for old, new in special_functions.items():
                equation = re.sub(r'\b' + old + r'\b', new, equation)

            # Asegurar que los números decimales estén bien formateados
            equation = re.sub(r'(\d+)\.(\d+)', r'\1.\2', equation)

            try:
                # Intentar parsear la ecuación con parse_expr para mayor flexibilidad
                expr = parse_expr(equation, evaluate=True)

                # Verificar variables
                variables = expr.free_symbols
                if not variables.issubset({self.x}):
                    other_vars = variables - {self.x}
                    return {
                        'success': False,
                        'message': f'Equation contains invalid variables: {", ".join(str(v) for v in other_vars)}. Only "x" is allowed.'
                    }

                # Crear función lambda con módulos matemáticos adicionales
                f = lambdify(self.x, expr, modules=['numpy', 'sympy'])

                return {
                    'success': True,
                    'message': 'Equation processed successfully',
                    'function': f,
                    'expression': expr
                }

            except Exception as e:
                logger.error(f"Error parsing equation '{equation}': {str(e)}")
                return {
                    'success': False,
                    'message': f'Invalid equation format: {str(e)}'
                }

        except Exception as e:
            logger.error(f"Unexpected error in prepare_equation: {str(e)}")
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}'
            }

    def evaluate_at_point(self, func: Callable, x_value: float) -> Dict[str, Union[bool, str, float]]:
        """
        Safely evaluates a function at a given point.

        Args:
            func (Callable): The function to evaluate
            x_value (float): The point at which to evaluate the function

        Returns:
            Dict containing:
                - success (bool): Whether the evaluation was successful
                - message (str): Status message or error description
                - value (float, optional): The computed value
        """
        try:
            # Convertir el valor x a float y evaluar
            x_float = float(x_value)
            result = float(func(x_float))

            return {
                'success': True,
                'message': 'Evaluation successful',
                'value': result
            }
        except Exception as e:
            logger.error(f"Error evaluating function at x={x_value}: {str(e)}")
            return {
                'success': False,
                'message': f'Error evaluating function at x={x_value}: {str(e)}'
            }