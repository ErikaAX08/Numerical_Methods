import numpy as np


def gauss_back_substitution_method(matrix):
    try:
        import numpy as np
        A = np.array([row[:-1] for row in matrix], dtype=float)  # Coeficientes
        # Términos independientes
        b = np.array([row[-1] for row in matrix], dtype=float)

        steps = []  # Guardar los pasos de la eliminación
        augmented_matrix = np.hstack([A, b.reshape(-1, 1)])  # Matriz aumentada

        # Guardar el estado inicial
        steps.append(augmented_matrix.tolist())

        # Aplicar eliminación de Gauss
        n = len(A)
        for i in range(n):
            for j in range(i + 1, n):
                factor = augmented_matrix[j, i] / augmented_matrix[i, i]
                augmented_matrix[j] -= factor * augmented_matrix[i]

            steps.append(augmented_matrix.tolist())  # Guardar cada paso

        # Resolver con sustitución hacia atrás
        x = np.linalg.solve(A, b)

        print("Pasos enviados:", steps)  # 👀 Verificar salida en el servidor

        return x.tolist(), steps  # Asegurar que los pasos sean listas

    except Exception as e:
        return str(e), []
