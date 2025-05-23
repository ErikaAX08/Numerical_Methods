import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import io
from sympy import symbols, lambdify, sympify

x = symbols('x')

def romberg_method_integration(func, a, b, max_level=4):
    f = lambdify(x, func, "numpy")
    tabla_romberg = []
    for i in range(max_level):
        n = 2 ** i
        h = (b - a) / n
        x_points = np.linspace(a, b, n + 1)
        y_points = f(x_points)
        T = h * (0.5 * y_points[0] + np.sum(y_points[1:-1]) + 0.5 * y_points[-1])
        tabla_romberg.append([T])
    for j in range(1, max_level):
        for i in range(j, max_level):
            prev = tabla_romberg[i][j-1]
            prev2 = tabla_romberg[i-1][j-1]
            val = prev + (prev - prev2) / (4**j - 1)
            tabla_romberg[i].append(val)
    return tabla_romberg

def generate_romberg_method_graph(func, a, b):
    f = lambdify(x, func, "numpy")
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_vals, label=f"f(x) = {func}", color="blue")
    ax.fill_between(x_vals, y_vals, alpha=0.2, color="orange")
    ax.set_title("Área bajo la curva para Romberg")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True)
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=300)
    plt.close()
    buffer.seek(0)
    return buffer

def generate_romberg_method_interactive_graph(func, a, b):
    f = lambdify(x, func, "numpy")
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode="lines", name=f"f(x) = {func}", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, fill='tozeroy', fillcolor='rgba(255,165,0,0.2)', line=dict(color='rgba(255,255,255,0)'), name="Área"))
    fig.update_layout(
        title="Área bajo la curva para Romberg",
        xaxis_title="x",
        yaxis_title="f(x)",
        showlegend=True
    )
    return fig.to_json()

# Ejemplo de uso
if __name__ == "__main__":
    print("Ejemplo de integración numérica usando el método de Romberg")
    a = float(input("Ingrese el valor de a: "))
    b = float(input("Ingrese el valor de b: "))
    max_level = int(input("Ingrese el número de niveles de Romberg (ej. 4): "))
    func_str = "x**2 + 1"
    func = sympify(func_str)
    tabla = romberg_method_integration(func, a, b, max_level)
    print("Tabla de Romberg:")
    for i, row in enumerate(tabla):
        print([f"{val:.8f}" for val in row])
    buffer = generate_romberg_method_graph(func, a, b)
    with open("romberg_area.png", "wb") as f:
        f.write(buffer.getvalue())
    interactive_graph = generate_romberg_method_interactive_graph(func, a, b)
    with open("romberg_area_interactive.json", "w") as f:
        f.write(interactive_graph)
    print("¡Gráficos generados!")
