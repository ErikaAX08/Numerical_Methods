def bisection(f, a, b, tol=1e-5, max_iter=100):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("No hay raíz en el intervalo dado")

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        if abs(fc) < tol or (b - a) / 2 < tol:
            return {"root": c, "iterations": i+1}

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

    raise ValueError(
        "No se encontró solución en el número máximo de iteraciones")
