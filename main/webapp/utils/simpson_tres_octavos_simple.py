import numpy as np
from sympy import symbols, lambdify, sympify, Expr

x = symbols('x')

def simpson_tres_octavos_simple(func_expr, a, b):
    """
    Implementa la regla de Simpson 3/8 simple.

    Args:
        func_expr: expresión de SymPy o cadena representando la función f(x)
        a: límite inferior del intervalo (float)
        b: límite superior del intervalo (float)

    Returns:
        Aproximación de la integral definida en [a, b] (float)
    """
    # Permitir que func_expr sea cadena o expresión sympy
    if isinstance(func_expr, str):
        func_expr = sympify(func_expr)
    elif not isinstance(func_expr, Expr):
        raise ValueError("func_expr debe ser una cadena o una expresión SymPy.")

    # Validar límites
    a = float(a)
    b = float(b)
    if a == b:
        return 0.0

    f = lambdify(x, func_expr, 'numpy')
    h = (b - a) / 3

    x0 = a
    x1 = a + h
    x2 = a + 2*h
    x3 = b

    integral = (3 * h / 8) * (f(x0) + 3*f(x1) + 3*f(x2) + f(x3))
    return float(integral)

# Ejemplo de uso
if __name__ == "__main__":
    func_str = "x / (x**2 + 4)"
    func_expr = func_str  # Ahora puede ser cadena directamente
    a = 0
    b = 2

    result = simpson_tres_octavos_simple(func_expr, a, b)
    print(f"Resultado de la integral de {func_str} en [{a}, {b}] con Simpson 3/8 simple: {result:.6f}")
