import numpy as np


def cholesky_factorization_method(matrix):
    """
    Implementa el método de factorización de Cholesky para resolver sistemas de ecuaciones lineales.

    La factorización de Cholesky descompone una matriz simétrica y definida positiva A 
    en el producto de una matriz triangular inferior L y su transpuesta L^T, tal que A = L * L^T.

    Args:
        matrix: Matriz aumentada del sistema de ecuaciones [A|b]

    Returns:
        tuple: (solución, pasos) donde solución es un vector o mensaje de error,
               y pasos es una lista de diccionarios con los detalles de cada paso.
    """
    try:
        # Convertir a matriz NumPy para facilitar los cálculos
        augmented_matrix = np.array(matrix, dtype=float)

        # Extraer la matriz A y el vector b
        A = augmented_matrix[:, :-1]
        b = augmented_matrix[:, -1]

        # Verificar si la matriz es cuadrada
        n = A.shape[0]
        if A.shape[1] != n:
            return "La matriz de coeficientes debe ser cuadrada para aplicar Cholesky", []

        steps = []

        # Guardar el estado inicial
        steps.append({
            "step": "Matriz aumentada inicial",
            "matrix": augmented_matrix.tolist()
        })

        # Verificar si la matriz es simétrica
        if not np.allclose(A, A.T, rtol=1e-5, atol=1e-8):
            return "La matriz no es simétrica. La factorización de Cholesky requiere una matriz simétrica", steps

        # Verificar rango
        rank_A = np.linalg.matrix_rank(A)
        rank_Ab = np.linalg.matrix_rank(augmented_matrix)

        if rank_A < rank_Ab:
            return "El sistema es inconsistente y no tiene solución", steps
        elif rank_A < n:
            # Determinar variables libres
            free_variables = []
            for i in range(n):
                col = A[:, i]
                # Si la columna es linealmente dependiente de las anteriores
                if np.linalg.matrix_rank(A[:, :i + 1]) == np.linalg.matrix_rank(A[:, :i]):
                    free_variables.append(f"x_{i + 1}")

            steps.append({
                "step": "Análisis de rango",
                "rank": rank_A,
                "variables": n,
                "free_variables": free_variables,
                "description": "El sistema tiene infinitas soluciones"
            })

            return {
                "status": "infinite_solutions",
                "message": "El sistema tiene infinitas soluciones",
                "details": {
                    "rank": rank_A,
                    "variables": n,
                    "free_variables": free_variables,
                    "description": "Hay variables libres en el sistema, lo que resulta en infinitas soluciones"
                }
            }, steps

        try:
            # Intentar calcular los eigenvalores para verificar si es definida positiva
            eigenvalues = np.linalg.eigvals(A)
            if np.any(eigenvalues <= 0):
                return "La matriz no es definida positiva. Todos los eigenvalores deben ser positivos para Cholesky", steps
        except np.linalg.LinAlgError:
            return "Error al calcular eigenvalores, la matriz puede ser singular", steps

        # Inicializar matriz L con ceros
        L = np.zeros((n, n))

        # Factorización de Cholesky
        for i in range(n):
            for j in range(i + 1):
                if i == j:  # Elementos diagonales
                    sum_term = sum(L[i, k] ** 2 for k in range(j))
                    if A[i, i] - sum_term <= 0:
                        return "La matriz no es definida positiva durante la factorización (valor diagonal no positivo)", steps
                    L[i, j] = np.sqrt(A[i, i] - sum_term)
                else:  # Elementos debajo de la diagonal
                    sum_term = sum(L[i, k] * L[j, k] for k in range(j))
                    if abs(L[j, j]) < 1e-10:
                        return "División por cero durante la factorización. La matriz puede no ser definida positiva", steps
                    L[i, j] = (A[i, j] - sum_term) / L[j, j]

            steps.append({
                "step": f"Factorización: cálculo de elementos de L para fila {i + 1}",
                "L": L.tolist(),
                "LT": L.T.tolist()
            })

        # Verificación A = L*L^T
        LLT = np.dot(L, L.T)
        is_decomposition_valid = np.allclose(A, LLT, rtol=1e-5, atol=1e-8)

        steps.append({
            "step": "Verificación de factorización: A = L*L^T",
            "A": A.tolist(),
            "LLT": LLT.tolist(),
            "is_valid": is_decomposition_valid
        })

        if not is_decomposition_valid:
            return "La factorización no es válida para esta matriz. Puede que no sea definida positiva", steps

        # Resolver Ly = b (sustitución hacia adelante)
        y = np.zeros(n)
        for i in range(n):
            sum_term = sum(L[i, j] * y[j] for j in range(i))
            if abs(L[i, i]) < 1e-10:
                return "División por cero al resolver Ly = b. La matriz L es singular", steps
            y[i] = (b[i] - sum_term) / L[i, i]

        steps.append({
            "step": "Solución del sistema Ly = b (sustitución hacia adelante)",
            "L": L.tolist(),
            "b": b.tolist(),
            "y": y.tolist()
        })

        # Resolver L^T x = y (sustitución hacia atrás)
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            sum_term = sum(L.T[i, j] * x[j] for j in range(i + 1, n))
            if abs(L.T[i, i]) < 1e-10:
                return "División por cero al resolver L^T x = y. La matriz L^T es singular", steps
            x[i] = (y[i] - sum_term) / L.T[i, i]

        steps.append({
            "step": "Solución del sistema L^T x = y (sustitución hacia atrás)",
            "LT": L.T.tolist(),
            "y": y.tolist(),
            "x": x.tolist()
        })

        # Verificar la solución
        residual = np.linalg.norm(np.dot(A, x) - b)
        if residual > 1e-8:
            steps.append({
                "step": "Advertencia: La solución tiene un residual alto",
                "residual": residual,
                "Ax": np.dot(A, x).tolist(),
                "b": b.tolist()
            })

        # Agregar solución final al historial de pasos
        steps.append({
            "step": "Solución final",
            "solution": x.tolist()
        })

        return x.tolist(), steps

    except Exception as e:
        # Capturar cualquier excepción y devolver mensaje de error
        return f"Error en el cálculo: {str(e)}", []
