def thomas_algorithm(A, b):
    n = len(b)
    c_prime = [0] * n
    d_prime = [0] * n

    # Inicialización del algoritmo
    c_prime[0] = A[0][1] / A[0][0] if n > 1 else 0
    d_prime[0] = b[0] / A[0][0]

    for i in range(1, n):
        denom = A[i][i] - A[i][i - 1] * c_prime[i - 1]
        if i < n - 1:
            c_prime[i] = A[i][i + 1] / denom
        d_prime[i] = (b[i] - A[i][i - 1] * d_prime[i - 1]) / denom

    x = [0] * n
    x[-1] = d_prime[-1]
    for i in reversed(range(n - 1)):
        x[i] = d_prime[i] - c_prime[i] * x[i + 1]
    return x


def cubic_spline_method(points_raw, x_interp, boundary="natural", deriv_start=0, deriv_end=0):
    process_steps = []

    # Convertir los valores de x y f(x) a float
    points = [{'x': float(p['x']), 'y': float(p['fx'])} for p in points_raw]
    process_steps.append({
        "step": r"\(\textbf{Convert Input Points:}\) Convertir cada punto de entrada a número flotante.",
        "intermediate_result": fr"\(\text{{points}} = {points}\)"
    })

    n = len(points)
    if n < 3:
        raise ValueError("Se necesitan al menos 3 puntos para calcular un trazador cúbico.")

    # Paso 1: Calcular h[i] = x[i+1] - x[i]
    h = [points[i + 1]['x'] - points[i]['x'] for i in range(n - 1)]
    process_steps.append({
        "step": r"\(\textbf{Step 1:}\) Calcular las diferencias \(\,h_i = x_{i+1} - x_i\).",
        "intermediate_result": fr"\( h = {h} \)"
    })

    # Paso 2: Construir el sistema para las segundas derivadas M[i]
    A = [[0] * n for _ in range(n)]
    b = [0] * n

    if boundary == "natural":
        A[0][0] = 1
        A[-1][-1] = 1
        process_steps.append({
            "step": r"\(\textbf{Step 2:}\) Condiciones de frontera Natural.",
            "intermediate_result": r"\(A_{0,0}=1,\ A_{n-1,n-1}=1,\ b_0=b_{n-1}=0\)"
        })
    elif boundary == "clamped":
        A[0][0] = 2 * h[0]
        A[0][1] = h[0]
        b[0] = 6 * (((points[1]['y'] - points[0]['y']) / h[0]) - deriv_start)
        A[-1][-2] = h[-1]
        A[-1][-1] = 2 * h[-1]
        b[-1] = 6 * (deriv_end - ((points[-1]['y'] - points[-2]['y']) / h[-1]))
        process_steps.append({
            "step": r"\(\textbf{Step 2:}\) Condiciones de frontera Clamped.",
            "intermediate_result": fr"\(A_0 = {A[0]},\ A_{{n-1}} = {A[-1]},\ b_0 = {b[0]},\ b_{{n-1}} = {b[-1]}\)"
        })

    for i in range(1, n - 1):
        A[i][i - 1] = h[i - 1]
        A[i][i] = 2 * (h[i - 1] + h[i])
        A[i][i + 1] = h[i]
        b[i] = 6 * (((points[i + 1]['y'] - points[i]['y']) / h[i]) -
                    ((points[i]['y'] - points[i - 1]['y']) / h[i - 1]))
    process_steps.append({
        "step": r"\(\textbf{Step 2 (cont.):}\) Construir las ecuaciones internas para \(M_i\).",
        "intermediate_result": fr"\[ A = {A},\quad b = {b} \]"
    })

    # Paso 3: Resolver el sistema tridiagonal
    M = thomas_algorithm(A, b)
    process_steps.append({
        "step": r"\(\textbf{Step 3:}\) Resolver el sistema tridiagonal con el algoritmo de Thomas.",
        "intermediate_result": fr"\( M = {M} \)"
    })

    # Paso 4: Calcular los coeficientes de cada segmento
    coefficients = []
    for i in range(n - 1):
        a_i = points[i]['y']
        b_i = ((points[i + 1]['y'] - points[i]['y']) / h[i]) - h[i] * (2 * M[i] + M[i + 1]) / 6
        c_i = M[i] / 2
        d_i = (M[i + 1] - M[i]) / (6 * h[i])
        coefficients.append({
            "a": a_i,
            "b": b_i,
            "c": c_i,
            "d": d_i,
            "x_i": points[i]['x'],
            "x_i1": points[i + 1]['x']
        })
    process_steps.append({
        "step": r"\(\textbf{Step 4:}\) Calcular los coeficientes del spline para cada intervalo.",
        "intermediate_result": (
            r"\[ S_i(x) = a_i + b_i(x - x_i) + c_i(x - x_i)^2 + d_i(x - x_i)^3 \]"
            + fr"\( \text{{Coeficientes}} = {coefficients} \)"
        )
    })

    # Paso 5: Determinar el tramo donde se encuentra x_interp
    segment = 0
    for i in range(n - 1):
        if points[i]['x'] <= x_interp <= points[i + 1]['x']:
            segment = i
            break
    else:
        segment = n - 2  # Si x_interp es igual al último punto, usar el último tramo
    process_steps.append({
        "step": r"\(\textbf{Step 5:}\) Determinar el segmento donde se ubica \(x_{\text{interp}}\).",
        "intermediate_result": fr"\( \text{{Segment}} = {segment},\ \text{{Interval}} = [{points[segment]['x']}, {points[segment+1]['x']}] \)"
    })

    # Paso 6: Calcular el valor interpolado en x_interp
    coef = coefficients[segment]
    dx = x_interp - coef["x_i"]
    value_interp = coef["a"] + coef["b"] * dx + coef["c"] * dx**2 + coef["d"] * dx**3
    process_steps.append({
        "step": r"\(\textbf{Step 6:}\) Calcular el valor interpolado usando el tramo determinado.",
        "intermediate_result": (
            r"\[ S(x) = a_i + b_i(x - x_i) + c_i(x - x_i)^2 + d_i(x - x_i)^3 \]"
            + fr"\( x_{{\text{{interp}}}} = {x_interp},\ dx = {dx},\ S(x) = {value_interp} \)"
        )
    })

    return {
        "points": points,
        "h": h,
        "M": M,
        "coefficients": coefficients,
        "segment": segment,
        "value_interp": value_interp,
        "process_steps": process_steps
    }
