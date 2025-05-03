import numpy as np
from sympy import symbols, lambdify, sympify

x = symbols('x')


def simpson_1_3_compuesta(func_expr, a, b, n):
    """
    Implementa la regla de Simpson 1/3 compuesta.

    Args:
        func_expr: expresión de SymPy representando la función f(x)
        a: límite inferior del intervalo
        b: límite superior del intervalo
        n: número de subintervalos (debe ser par)

    Returns:
        Aproximación de la integral definida
    """
    if n % 2 != 0:
        raise ValueError(
            "Simpson 1/3 requiere que el número de subintervalos n sea par.")

    f = lambdify(x, func_expr, 'numpy')
    h = (b - a) / n
    x_vals = np.linspace(a, b, n + 1)
    y_vals = f(x_vals)

    sum_odd = np.sum(y_vals[1:-1:2])
    sum_even = np.sum(y_vals[2:-1:2])

    integral = (h / 3) * (y_vals[0] + 4 * sum_odd + 2 * sum_even + y_vals[-1])
    return integral


# Ejemplo de uso
if __name__ == "__main__":
    func_str = "x / (x**2 + 4)"
    func_expr = sympify(func_str)
    a = 0
    b = 2
    n = 6  # Debe ser par

    result = simpson_1_3_compuesta(func_expr, a, b, n)
    print(
        f"Resultado de la integral de {func_str} en [{a}, {b}] con n={n}: {result:.6f}")
