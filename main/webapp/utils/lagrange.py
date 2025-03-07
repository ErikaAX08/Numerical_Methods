import logging
import random
import numpy as np
from sympy import symbols, sympify, lambdify, expand


def lagrange_method(degree=0.0, value=0.0, points=[]):
    try:
        points = [(float(point['x']), float(point['fx'])) for point in points]
        result = 0.0
        n = len(points)
        process_steps = []

        # Paso 1: Definir los puntos
        points_step = {
            'step': r"Dados\ los\ puntos:\ " + ",\ ".join(
                [f"(x_{i}={x},\ y_{i}={y})" for i, (x, y) in enumerate(points)]),
            'intermediate_result': "Definición de puntos"
        }
        process_steps.append(points_step)

        # Paso 2: Calcular los polinomios base
        L_values = []
        L_expressions = []

        x = symbols('x')

        for i in range(n):
            xi, yi = points[i]
            Li = 1.0

            # Construir la expresión para L_i(x)
            numerator_terms = []
            denominator_terms = []

            for j in range(n):
                if j != i:
                    xj, _ = points[j]
                    Li *= (value - xj) / (xi - xj)

                    numerator_terms.append(f"(x - {xj})")
                    denominator_terms.append(f"({xi} - {xj})")

            # Crear la fórmula LaTeX para L_i(x)
            numerator = r" \cdot ".join(numerator_terms)
            denominator = r" \cdot ".join(denominator_terms)

            simplified_denominator = 1
            for j in range(n):
                if j != i:
                    xj, _ = points[j]
                    simplified_denominator *= (xi - xj)

            L_formula = f"L_{i}(x) = \\frac{{{numerator}}}{{{denominator}}} = \\frac{{{numerator}}}{{{simplified_denominator}}}"

            # Guardar valores y expresiones
            L_values.append(Li)
            L_expressions.append(L_formula)

            # Agregar paso
            process_steps.append({
                'step': L_formula,
                'intermediate_result': f"L_{i}({value}) = {Li}"
            })

        # Paso 3: Construir el polinomio interpolador
        interpolation_formula = "P(x) = " + " + ".join([f"{points[i][1]} \\cdot L_{i}(x)" for i in range(n)])
        process_steps.append({
            'step': interpolation_formula,
            'intermediate_result': "Fórmula del polinomio interpolador"
        })

        # Paso 4: Sustituir y simplificar
        substitution_formula = "P(x) = " + " + ".join([
            f"{points[i][1]} \\cdot \\left(\\frac{{{' \\cdot '.join([f'(x - {points[j][0]})' for j in range(n) if j != i])}}}{{{np.prod([xi - points[j][0] for j in range(n) if j != i])}}}" + "\\right)"
            for i, (xi, _) in enumerate(points)])

        # Calcular el resultado
        for i in range(n):
            xi, yi = points[i]
            result += yi * L_values[i]

        process_steps.append({
            'step': substitution_formula,
            'intermediate_result': f"P({value}) = {result}"
        })

        # Paso 5: Desarrollar y simplificar el polinomio final usando sympy
        # Crear la expresión simbólica para P(x)
        P_expr = 0
        for i in range(n):
            xi, yi = points[i]
            L_expr = 1
            for j in range(n):
                if j != i:
                    xj = points[j][0]
                    L_expr *= (x - xj) / (xi - xj)
            P_expr += yi * L_expr

        final_result = f"P({value}) = {result}"

        process_steps.append({
            'step': final_result,
            'intermediate_result': f""
        })

        # Regresar solo los pasos hasta el Paso 6, sin el Paso 7
        return result, process_steps

    except Exception as e:
        print(f"Error: {e}")
        return None, []
