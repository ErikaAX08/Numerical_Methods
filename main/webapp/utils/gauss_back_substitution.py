import numpy as np

def gauss_jordan_elimination(matrix):
    try:
        augmented_matrix = np.array(matrix, dtype=float)
        n = len(augmented_matrix)
        steps = []

        # Guardar el estado inicial
        steps.append({"step": "Initial augmented matrix",
                     "matrix": augmented_matrix.tolist()})

        # Eliminación hacia adelante (Gauss)
        for i in range(n):
            # Pivoteo parcial
            max_row = np.argmax(abs(augmented_matrix[i:, i])) + i
            if max_row != i:
                augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
                steps.append({"step": f"Swap row {i+1} with row {max_row+1}",
                             "matrix": augmented_matrix.tolist()})

            # Normalizar el pivote
            pivot = augmented_matrix[i, i]
            if abs(pivot) < 1e-10:
                return "No unique solution (singular matrix)", []

            augmented_matrix[i] /= pivot
            steps.append({"step": f"Scale row {i+1} by 1/{pivot}",
                         "matrix": augmented_matrix.tolist()})

            # Eliminación solo debajo del pivote primero
            for j in range(i+1, n):
                factor = augmented_matrix[j, i]
                augmented_matrix[j] -= factor * augmented_matrix[i]

            if i < n-1:  # Solo registra pasos si quedan filas debajo
                steps.append({"step": f"Elimination below pivot in column {i+1}",
                             "matrix": augmented_matrix.tolist()})

        # Eliminación hacia atrás (Jordan)
        for i in range(n-1, -1, -1):
            for j in range(i-1, -1, -1):
                factor = augmented_matrix[j, i]
                augmented_matrix[j] -= factor * augmented_matrix[i]

            if i > 0:  # Solo registra pasos si quedan filas arriba
                steps.append({"step": f"Elimination above pivot in column {i+1}",
                             "matrix": augmented_matrix.tolist()})

        # Extraer la solución
        x = augmented_matrix[:, -1]
        steps.append({"step": "Final solution", "solution": x.tolist()})

        return x.tolist(), steps

    except Exception as e:
        return str(e), []
