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


def cubic_spline_method(points_raw, x_interp, boundary="natural", deriv_start=0, deriv_end=0, periodic_check=False):
    process_steps = []

    # Convertir los valores de x y f(x) a float
    points = [{'x': float(p['x']), 'y': float(p['fx'])} for p in points_raw]
    process_steps.append({
        "step": r"\(\textbf{Paso 1:}\) Convertir cada punto de entrada a número flotante.",
        "explanation": r"Convertimos todos los datos de entrada a formato numérico para realizar los cálculos matemáticos con precisión. Este paso es fundamental para asegurar que todas las operaciones aritméticas se realicen correctamente.",
        "intermediate_result": fr"\(\text{{puntos}} = [" + ", ".join([f"({p['x']}, {p['y']})" for p in points]) + r"]\)"
    })

    n = len(points)
    if n < 3:
        raise ValueError("Se necesitan al menos 3 puntos para calcular un trazador cúbico.")

    # Para spline periódico, verificar si el primer y último punto tienen el mismo valor
    if boundary == "periodic":
        if periodic_check and abs(points[0]['y'] - points[-1]['y']) > 1e-10:
            raise ValueError("Para el spline periódico, el valor de f(x) en el primer y último punto debe ser igual.")
        # Si no se verificó antes, asegurarse de que el valor de y sea igual
        points[-1]['y'] = points[0]['y']
        process_steps.append({
            "step": r"\(\textbf{Verificación para spline periódico:}\) Comprobar la igualdad de valores en los extremos.",
            "explanation": r"En un spline periódico, es necesario que \(f(x_0) = f(x_n)\) para garantizar la continuidad cíclica. Verificamos esta condición y, si es necesario, ajustamos el valor final para que coincida con el inicial.",
            "intermediate_result": fr"\(f(x_0) = {points[0]['y']},\ f(x_n) = {points[-1]['y']}\)"
        })

    # Paso 2: Calcular h[i] = x[i+1] - x[i]
    h = [points[i + 1]['x'] - points[i]['x'] for i in range(n - 1)]
    process_steps.append({
        "step": r"\(\textbf{Paso 2:}\) Calcular las distancias entre nodos consecutivos.",
        "explanation": r"Calculamos la diferencia entre cada par de nodos consecutivos \(h_i = x_{i+1} - x_i\). Estas distancias son fundamentales para construir el sistema de ecuaciones y calcular los coeficientes del spline.",
        "intermediate_result": r"\( h = [" + ", ".join([f"{hi}" for hi in h]) + r"] \)"
    })

    # Paso 3: Construir el sistema para las segundas derivadas M[i]
    A = [[0] * n for _ in range(n)]
    b = [0] * n

    # Explicación general del sistema
    system_explanation = r"""Para determinar los trazadores cúbicos, necesitamos encontrar las segundas derivadas \(M_i = S_i''(x_i)\) en cada nodo. 
    Para esto, construimos un sistema de ecuaciones lineales que relaciona estas segundas derivadas, considerando las condiciones de continuidad de la primera y segunda derivada en los puntos internos.

    La forma general del sistema es:
    \[h_{i-1}M_{i-1} + 2(h_{i-1} + h_i)M_i + h_iM_{i+1} = 6\left(\frac{y_{i+1} - y_i}{h_i} - \frac{y_i - y_{i-1}}{h_{i-1}}\right)\]

    Para los nodos de los extremos, necesitamos aplicar condiciones de frontera específicas según el tipo de spline seleccionado."""

    # Aplicar condiciones de frontera según el tipo de spline
    if boundary == "natural":
        # Condiciones de frontera Natural: segunda derivada = 0 en los extremos
        A[0][0] = 1
        A[-1][-1] = 1
        boundary_explanation = r"""En un spline natural, establecemos que la segunda derivada sea cero en los extremos:
        \[S''(x_0) = S''(x_n) = 0\]

        Esto significa que \(M_0 = M_{n-1} = 0\), lo que simplifica las ecuaciones en los extremos. Esta condición es ideal cuando no tenemos información adicional sobre el comportamiento de la función en los límites del intervalo.
        """
        process_steps.append({
            "step": r"\(\textbf{Paso 3:}\) Aplicar condiciones de frontera: Spline Natural.",
            "explanation": boundary_explanation,
            "intermediate_result": r"\(A_{0,0}=1,\ A_{n-1,n-1}=1,\ b_0=b_{n-1}=0\)"
        })
    elif boundary == "clamped":
        # Condiciones de frontera Clamped: se especifica la primera derivada en los extremos
        A[0][0] = 2 * h[0]
        A[0][1] = h[0]
        b[0] = 6 * (((points[1]['y'] - points[0]['y']) / h[0]) - deriv_start)
        A[-1][-2] = h[-1]
        A[-1][-1] = 2 * h[-1]
        b[-1] = 6 * (deriv_end - ((points[-1]['y'] - points[-2]['y']) / h[-1]))
        boundary_explanation = r"""En un spline clamped (o sujeto), especificamos el valor de la primera derivada en ambos extremos:
        \[S'(x_0) = f'_0 = """ + str(deriv_start) + r"""\]
        \[S'(x_n) = f'_n = """ + str(deriv_end) + r"""\]

        Esta condición es particularmente útil cuando conocemos la pendiente de la función en los extremos, proporcionando una interpolación más precisa en estos puntos. Por ejemplo, si estamos modelando una curva física y conocemos su velocidad o tasa de cambio en los extremos.
        """
        process_steps.append({
            "step": r"\(\textbf{Paso 3:}\) Aplicar condiciones de frontera: Spline Clamped.",
            "explanation": boundary_explanation,
            "intermediate_result": r"\(A_0 = [" + ", ".join(
                [f"{a}" for a in A[0][:3]]) + r"...],\ A_{n-1} = [..." + ", ".join(
                [f"{a}" for a in A[-1][-3:]]) + r"],\ b_0 = " + f"{b[0]}" + r",\ b_{n-1} = " + f"{b[-1]}" + r"\)"
        })
    elif boundary == "not-a-knot":
        # Condiciones de frontera Not-a-Knot: tercera derivada continua en x₁ y x_{n-1}
        # Primera condición en x₁
        A[0][0] = h[1]
        A[0][1] = -(h[0] + h[1])
        A[0][2] = h[0]
        b[0] = 0  # Continuidad de la tercera derivada implica que el lado derecho es 0

        # Segunda condición en x_{n-1}
        A[-1][-3] = h[-1]
        A[-1][-2] = -(h[-2] + h[-1])
        A[-1][-1] = h[-2]
        b[-1] = 0

        boundary_explanation = r"""En un spline not-a-knot (no-a-nudo), imponemos que la tercera derivada sea continua en los puntos \(x_1\) y \(x_{n-1}\):
        \[S_0'''(x_1) = S_1'''(x_1)\]
        \[S_{n-3}'''(x_{n-1}) = S_{n-2}'''(x_{n-1})\]

        Esta condición elimina efectivamente los "nudos" (o puntos de unión) en \(x_1\) y \(x_{n-1}\), haciendo que el spline actúe como un único polinomio cúbico en los intervalos \([x_0, x_2]\) y \([x_{n-2}, x_n]\). Este enfoque suele proporcionar mejor precisión en los extremos del intervalo que el spline natural.
        """
        process_steps.append({
            "step": r"\(\textbf{Paso 3:}\) Aplicar condiciones de frontera: Spline Not-a-Knot.",
            "explanation": boundary_explanation,
            "intermediate_result": r"\(A_0 = [" + ", ".join(
                [f"{a}" for a in A[0][:3]]) + r"...],\ A_{n-1} = [..." + ", ".join(
                [f"{a}" for a in A[-1][-3:]]) + r"],\ b_0 = " + f"{b[0]}" + r",\ b_{n-1} = " + f"{b[-1]}" + r"\)"
        })
    elif boundary == "periodic":
        # Condiciones de frontera periódicas: f(x₀) = f(xₙ) y derivadas iguales
        # Ecuaciones internas (1 a n-2)
        for i in range(1, n - 1):
            A[i][i - 1] = h[i - 1]
            A[i][i] = 2 * (h[i - 1] + h[i])
            A[i][i + 1] = h[i]
            b[i] = 6 * (((points[i + 1]['y'] - points[i]['y']) / h[i]) -
                        ((points[i]['y'] - points[i - 1]['y']) / h[i - 1]))

        # Para la periodicidad, M₀ = Mₙ
        A[0][0] = 2 * (h[0] + h[-1])
        A[0][1] = h[0]
        A[0][-1] = h[-1]
        b[0] = 6 * (((points[1]['y'] - points[0]['y']) / h[0]) -
                    ((points[0]['y'] - points[-2]['y']) / h[-1]))

        A[-1][0] = h[-1]
        A[-1][-2] = h[-2]
        A[-1][-1] = 2 * (h[-2] + h[-1])
        b[-1] = 6 * (((points[0]['y'] - points[-1]['y']) / h[-1]) -
                     ((points[-1]['y'] - points[-2]['y']) / h[-2]))

        boundary_explanation = r"""En un spline periódico, establecemos que tanto la función como sus derivadas primera y segunda coincidan en los extremos:
        \[f(x_0) = f(x_n)\]
        \[S'_0(x_0) = S'_{n-1}(x_n)\]
        \[S''_0(x_0) = S''_{n-1}(x_n)\]

        Esta condición es ideal para modelar fenómenos cíclicos como ondas, órbitas planetarias o cualquier proceso que se repita periódicamente. El spline periódico garantiza una transición perfectamente suave al "cerrar el ciclo" entre el primer y último punto.
        """
        process_steps.append({
            "step": r"\(\textbf{Paso 3:}\) Aplicar condiciones de frontera: Spline Periódico.",
            "explanation": boundary_explanation,
            "intermediate_result": r"\(A_0 = [" + ", ".join(
                [f"{A[0][0]:.2f}, {A[0][1]:.2f},..., {A[0][-1]:.2f}"]) + r"],\ A_{n-1} = [" + ", ".join(
                [f"{A[-1][0]:.2f},..., {A[-1][-2]:.2f}, {A[-1][-1]:.2f}"]) + r"]\)"
        })
    else:
        # Por defecto, usar spline natural
        A[0][0] = 1
        A[-1][-1] = 1
        process_steps.append({
            "step": r"\(\textbf{Paso 3:}\) Aplicar condiciones de frontera (por defecto): Spline Natural.",
            "explanation": r"Como no se especificó un tipo de spline válido, se utiliza el spline natural como opción predeterminada.",
            "intermediate_result": r"\(A_{0,0}=1,\ A_{n-1,n-1}=1,\ b_0=b_{n-1}=0\)"
        })
    # Agregar ecuaciones internas para todas las condiciones excepto periódico (ya se hizo)
    if boundary != "periodic":
        for i in range(1, n - 1):
            A[i][i - 1] = h[i - 1]
            A[i][i] = 2 * (h[i - 1] + h[i])
            A[i][i + 1] = h[i]
            b[i] = 6 * (((points[i + 1]['y'] - points[i]['y']) / h[i]) -
                        ((points[i]['y'] - points[i - 1]['y']) / h[i - 1]))

    process_steps.append({
        "step": r"\(\textbf{Paso 3 (cont.):}\) Construir las ecuaciones internas para \(M_i\).",
        "explanation": r"Para cada punto interno \(x_i\) (con \(i = 1, 2, ..., n-2\)), imponemos la continuidad de la primera y segunda derivada, resultando en ecuaciones de la forma \(h_{i-1}M_{i-1} + 2(h_{i-1}+h_i)M_i + h_iM_{i+1} = 6(\frac{y_{i+1}-y_i}{h_i} - \frac{y_i-y_{i-1}}{h_{i-1}})\).",
        "intermediate_result": fr"\[ A = {A},\quad b = {b} \]"
    })

    # Paso 4: Resolver el sistema tridiagonal (o general para periódico)
    M = thomas_algorithm(A, b)
    process_steps.append({
        "step": r"\(\textbf{Paso 4:}\) Resolver el sistema para obtener los valores de \(M_i\) (segundas derivadas en los nodos).",
        "explanation": r"Utilizamos el algoritmo de Thomas para resolver el sistema tridiagonal de forma eficiente. Para el caso periódico, se adapta el sistema para mantener la periodicidad.",
        "intermediate_result": fr"\( M = {M} \)"
    })

    # Paso 5: Calcular los coeficientes de cada segmento
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
        "step": r"\(\textbf{Paso 5:}\) Calcular los coeficientes del spline para cada intervalo.",
        "explanation": r"""Para cada intervalo $[x_i, x_{i+1}]$, calculamos los coeficientes del polinomio cúbico $S_i(x) = a_i + b_i(x - x_i) + c_i(x - x_i)^2 + d_i(x - x_i)^3$ donde:
        $a_i = y_i$
        $b_i = \frac{y_{i+1} - y_i}{h_i} - \frac{h_i}{6}(2M_i + M_{i+1})$
        $c_i = \frac{M_i}{2}$
        $d_i = \frac{M_{i+1} - M_i}{6h_i}$""",
        "intermediate_result": (
                r"\[ S_i(x) = a_i + b_i(x - x_i) + c_i(x - x_i)^2 + d_i(x - x_i)^3 \]"
                + fr"\( \text{{Coeficientes}} = {coefficients} \)"
        )
    })

    # Paso 6: Determinar el tramo donde se encuentra x_interp
    segment = 0
    for i in range(n - 1):
        if points[i]['x'] <= x_interp <= points[i + 1]['x']:
            segment = i
            break
    else:
        # Si x_interp está fuera del rango
        if x_interp < points[0]['x']:
            segment = 0
        else:
            segment = n - 2  # Último segmento

    process_steps.append({
        "step": r"\(\textbf{Paso 6:}\) Determinar el segmento donde se ubica \(x_{\text{interp}}\).",
        "explanation": r"Identificamos en qué intervalo $[x_i, x_{i+1}]$ se encuentra el valor a interpolar $x_{\text{interp}} = " + str(
            x_interp) + r"$ para utilizar el polinomio correspondiente.",
        "intermediate_result": fr"\( \text{{Segmento}} = {segment},\ \text{{Intervalo}} = [{points[segment]['x']}, {points[segment + 1]['x']}] \)"
    })

    # Paso 7: Calcular el valor interpolado en x_interp
    coef = coefficients[segment]
    dx = x_interp - coef["x_i"]
    value_interp = coef["a"] + coef["b"] * dx + coef["c"] * dx ** 2 + coef["d"] * dx ** 3
    process_steps.append({
        "step": r"\(\textbf{Paso 7:}\) Calcular el valor interpolado usando el polinomio del segmento determinado.",
        "explanation": r"Evaluamos el polinomio $S_" + str(segment) + r"(x)$ en $x = " + str(
            x_interp) + r"$ sustituyendo los coeficientes y calculando $S(" + str(x_interp) + r") = a_" + str(
            segment) + r" + b_" + str(segment) + r"(x - x_" + str(segment) + r") + c_" + str(
            segment) + r"(x - x_" + str(segment) + r")^2 + d_" + str(segment) + r"(x - x_" + str(segment) + r")^3$",
        "intermediate_result": (
                r"\[ S_" + str(
            segment) + r"(x) = " + f"{coef['a']:.6f} + {coef['b']:.6f}(x - {coef['x_i']}) + {coef['c']:.6f}(x - {coef['x_i']})^2 + {coef['d']:.6f}(x - {coef['x_i']})^3 \]"
                + fr"\( x_{{\text{{interp}}}} = {x_interp},\ dx = {dx},\ S({x_interp}) = {value_interp:.6f} \)"
        )
    })

    return {
        "points": points,
        "h": h,
        "M": M,
        "coefficients": coefficients,
        "segment": segment,
        "value_interp": value_interp,
        "process_steps": process_steps,
        "boundary_type": boundary
    }
