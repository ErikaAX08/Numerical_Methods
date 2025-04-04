import numpy as np


def gauss_maximum_column_pivoting_method(matrix):
    """
    Implementa el método de eliminación gaussiana con pivoteo máximo de columnas.

    Args:
        matrix: Matriz aumentada del sistema de ecuaciones [A|b]

    Returns:
        tuple: (solución, pasos) donde solución es un vector o mensaje de error,
               y pasos es una lista de diccionarios con los detalles de cada paso.
    """
    try:
        # Convertir a matriz NumPy para facilitar los cálculos
        augmented_matrix = np.array(matrix, dtype=float)
        n = augmented_matrix.shape[0]  # Número de filas (ecuaciones)
        steps = []

        # Guardar el estado inicial
        steps.append({
            "step": "Matriz aumentada inicial",
            "matrix": augmented_matrix.tolist()
        })

        # Verificar si la matriz es singular mediante el cálculo de su determinante
        A = augmented_matrix[:, :-1]  # Matriz de coeficientes
        if A.shape[0] == A.shape[1]:  # Solo si es cuadrada
            try:
                det = np.linalg.det(A)
                if abs(det) < 1e-10:
                    return "El sistema no tiene solución única (matriz singular - determinante ≈ 0)", steps
            except np.linalg.LinAlgError:
                return "Error al calcular el determinante, la matriz podría ser singular", steps

        # Verificar rango para sistemas no cuadrados o sistemas inconsistentes
        rank_A = np.linalg.matrix_rank(A)
        rank_Ab = np.linalg.matrix_rank(augmented_matrix)

        if rank_A < rank_Ab:
            return "El sistema es inconsistente y no tiene solución", steps
        elif rank_A < A.shape[1]:
            return "El sistema tiene infinitas soluciones", steps

        # Eliminación hacia adelante (Gauss)
        for i in range(n):
            # Encontrar el elemento con valor absoluto máximo en la columna actual
            max_index = i + np.argmax(np.abs(augmented_matrix[i:, i]))

            # Intercambiar filas si es necesario
            if max_index != i:
                augmented_matrix[[i, max_index]] = augmented_matrix[[max_index, i]]
                steps.append({
                    "step": f"Intercambio de filas {i + 1} y {max_index + 1}",
                    "matrix": augmented_matrix.tolist()
                })

            # Verificar si el pivote es casi cero
            pivot = augmented_matrix[i, i]
            if abs(pivot) < 1e-10:
                return "El sistema no tiene solución única (encontrado pivote cero)", steps

            # Normalizar la fila del pivote
            augmented_matrix[i] = augmented_matrix[i] / pivot
            steps.append({
                "step": f"Normalización de la fila {i + 1} (dividir por {pivot:.6f})",
                "matrix": augmented_matrix.tolist()
            })

            # Eliminación hacia abajo
            for j in range(i + 1, n):
                factor = augmented_matrix[j, i]
                if abs(factor) > 1e-10:  # Solo eliminar si el factor no es casi cero
                    augmented_matrix[j] -= factor * augmented_matrix[i]

            steps.append({
                "step": f"Eliminación de elementos debajo del pivote en la columna {i + 1}",
                "matrix": augmented_matrix.tolist()
            })

        # Sustitución hacia atrás (Jordan)
        for i in range(n - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                factor = augmented_matrix[j, i]
                if abs(factor) > 1e-10:  # Solo eliminar si el factor no es casi cero
                    augmented_matrix[j] -= factor * augmented_matrix[i]

            if i > 0:  # No registrar un paso para la última iteración
                steps.append({
                    "step": f"Eliminación de elementos encima del pivote en la columna {i + 1}",
                    "matrix": augmented_matrix.tolist()
                })

        # Verificar la validez de la solución
        solution = augmented_matrix[:, -1]
        if np.any(np.isnan(solution)) or np.any(np.isinf(solution)):
            return "Se obtuvieron valores no válidos en la solución (posiblemente sistema inconsistente)", steps

        # Agregar paso final con la solución
        steps.append({
            "step": "Solución final",
            "solution": solution.tolist()
        })

        return solution.tolist(), steps

    except Exception as e:
        # Capturar cualquier excepción y devolver mensaje de error
        return f"Error en el cálculo: {str(e)}", []
