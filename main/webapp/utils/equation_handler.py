from sympy import symbols, sympify, lambdify
import logging
from typing import Dict, Union, Callable

logger = logging.getLogger(__name__)


class EquationHandler:
    def __init__(self):
        self.x = symbols('x')

    def prepare_equation(self, equation: str) -> Dict[str, Union[bool, str, Callable]]:
        """
        Prepares and validates a mathematical equation for computation.

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
                '√': 'sqrt'  # Square root
            }

            for old, new in replacements.items():
                equation = equation.replace(old, new)

            # Try to parse the equation with sympy
            try:
                expr = sympify(equation)

                # Check if the equation only uses x as variable
                variables = expr.free_symbols
                if not variables.issubset({self.x}):
                    other_vars = variables - {self.x}
                    return {
                        'success': False,
                        'message': f'Equation contains invalid variables: {", ".join(str(v) for v in other_vars)}. Only "x" is allowed.'
                    }

                # Create a lambda function for numerical evaluation
                f = lambdify(self.x, expr)

                return {
                    'success': True,
                    'message': 'Equation processed successfully',
                    'function': f,
                    'expression': expr
                }

            except Exception as e:
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
            result = float(func(float(x_value)))
            return {
                'success': True,
                'message': 'Evaluation successful',
                'value': result
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error evaluating function at x={x_value}: {str(e)}'
            }
