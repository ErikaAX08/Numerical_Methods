from django.shortcuts import render
from django.http import JsonResponse
import json
import copy


def lu_factorization(request):
    return render(request, 'lu_factorization.html')


def calculate_lu_factorization(request):
    if request.method == "POST":
        try:
            print("Start calculating LU decomposition...")

            data = json.loads(request.body.decode("utf-8"))
            print("Received data:", data)

            if "matrix" not in data or "vector" not in data:
                return JsonResponse({'error': 'Missing required fields: matrix and vector'}, status=400)

            matrix = data["matrix"]
            vector = data["vector"]

            if len(matrix) != len(vector):
                return JsonResponse({'error': 'Matrix and vector dimensions do not match'}, status=400)

            for row in matrix:
                if len(row) != len(matrix):
                    return JsonResponse({'error': 'Matrix must be square'}, status=400)

            result = lu_decomposition_method(matrix, vector)
            return JsonResponse(result)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as error:
            print("Error:", error)
            return JsonResponse({'error': str(error)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def eliminacion_gaussiana(A):
    n = len(A)
    U = copy.deepcopy(A)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    steps = []

    for i in range(n):
        for j in range(i+1, n):
            if abs(U[i][i]) < 1e-10:
                raise ZeroDivisionError(
                    f"División por cero detectada al procesar fila {i+1}")

            m = U[j][i] / U[i][i]
            L[j][i] = m

            for k in range(n):
                U[j][k] -= m * U[i][k]

            steps.append({
                "step": f"Eliminación en fila {j+1}, columna {i+1}",
                "description": f"Se hace cero U[{j+1}][{i+1}] usando la fila {i+1}. Multiplicador m = {m}",
                "matrix_U": copy.deepcopy(U),
                "matrix_L": copy.deepcopy(L)
            })

    return L, U, steps


def resolver_ly_b(L, b):
    n = len(L)
    y = [0.0] * n
    steps = []
    # Extendido por si hay más variables
    variables = ['a', 'b', 'c', 'd', 'e', 'f']

    for i in range(n):
        suma = sum(L[i][j] * y[j] for j in range(i))
        sum_terms = " + ".join(
            [f"L[{i+1}][{j+1}]*{variables[j]}" for j in range(i)]) if i > 0 else "0"
        y[i] = b[i] - suma

        steps.append({
            "step": f"Cálculo de {variables[i]}",
            "description": f"{variables[i]} = b[{i+1}] - ({sum_terms})",
            "calculation": f"{variables[i]} = {b[i]} - {suma} = {y[i]}"
        })

    return y, steps


def resolver_ux_y(U, y):
    n = len(U)
    x = [0.0] * n
    steps = []
    # Cambiamos a variables x1, x2, x3 para mayor claridad
    variables = [f'x{i+1}' for i in range(n)]

    for i in range(n-1, -1, -1):  # Iniciamos desde la última fila hacia la primera
        suma = sum(U[i][j] * x[j] for j in range(i+1, n))
        x[i] = (y[i] - suma) / U[i][i]

        sum_terms = " + ".join(
            [f"U[{i+1}][{j+1}]*{variables[j]}" for j in range(i+1, n)]) if i < n-1 else "0"

        steps.append({
            "step": f"Cálculo de {variables[i]}",
            "description": f"Resolviendo para {variables[i]} usando sustitución hacia atrás",
            "calculation": f"{variables[i]} = (y[{i+1}] - {sum_terms}) / U[{i+1}][{i+1}] = ({y[i]} - {suma}) / {U[i][i]} = {x[i]:.4f}"
        })

    return x, steps


def lu_decomposition_method(matrix, vector):
    A = copy.deepcopy(matrix)
    b = copy.deepcopy(vector)
    steps = []

    steps.append({
        "step": "Sistema inicial Ax = b",
        "description": "Matriz A y vector b originales",
        "matrix_A": copy.deepcopy(A),
        "vector_b": copy.deepcopy(b)
    })

    # Paso de eliminación gaussiana
    L, U, gauss_steps = eliminacion_gaussiana(A)
    steps.extend(gauss_steps)

    # Resolución de Ly = b
    y, ly_steps = resolver_ly_b(L, b)
    steps.append({
        "step": "Resolución de Ly = b",
        "description": "Se resuelve el sistema Ly = b usando sustitución hacia adelante"
    })
    steps.extend(ly_steps)

    # Resolución de Ux = y
    x, ux_steps = resolver_ux_y(U, y)
    steps.append({
        "step": "Resolución de Ux = y",
        "description": "Se resuelve el sistema Ux = y usando sustitución hacia atrás",
        "matrix_U": copy.deepcopy(U),
        "vector_y": copy.deepcopy(y)
    })
    steps.extend(ux_steps)

    return {
        "status": "success",
        "message": "Descomposición LU y resolución de Ly = b y Ux = y completadas",
        "matrices": {
            "A": A,
            "L": L,
            "U": U
        },
        "vectors": {
            "b": b,
            "y": y,
            "x": x
        },
        "process_steps": steps
    }
