import numpy as np
import sympy as sp


def diferencias_divididas(x, y):
    """ Calcula la tabla de diferencias divididas """
    n = len(x)
    coef = np.zeros((n, n))  # Matriz de ceros
    coef[:, 0] = y  # Primera columna es f(x)

    for j in range(1, n):
        for i in range(n - j):
            coef[i][j] = (coef[i + 1][j - 1] - coef[i]
                          [j - 1]) / (x[i + j] - x[i])

    return coef


def evaluar_polinomio(coef, x, x_eval):
    """ Evalúa el polinomio de diferencias divididas en x_eval """
    n = len(coef)
    resultado = coef[0, -1]

    for i in range(n - 2, -1, -1):
        resultado = resultado * (x_eval - x[i]) + coef[0, i]

    return resultado


def divided_differences_method(x_values, y_values, x_eval):
    try:
        x = np.array(x_values, dtype=float)
        y = np.array(y_values, dtype=float)

        if len(x) != len(y):
            return {'error': True, 'message': 'Las listas de X y F(X) deben tener la misma longitud.'}

        coef = diferencias_divididas(x, y)
        resultado = evaluar_polinomio(coef, x, x_eval)

        # Construir tabla de salida
        table = []
        for i in range(len(x)):
            row = {"x": x[i], "f(x)": y[i]}
            for j in range(i):
                row[f"Δ^{j+1}"] = coef[i - j - 1, j + 1]
            table.append(row)

        return {
            'error': False,
            'message': 'Cálculo completado exitosamente.',
            'result': resultado,
            'table': table
        }

    except Exception as e:
        return {'error': True, 'message': f'Error: {str(e)}'}
