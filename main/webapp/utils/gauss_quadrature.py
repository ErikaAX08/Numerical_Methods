import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import io
from sympy import symbols, lambdify, sympify

# Definir la variable simbólica
x = symbols('x')


def gauss_quadrature(func, a, b, n=2):
    """
    Implementa la cuadratura de Gauss-Legendre.
    
    Args:
        func: función a integrar (expresión de sympy)
        a: límite inferior
        b: límite superior
        n: número de puntos de Gauss (2 por defecto)
    
    Returns:
        Aproximación de la integral, puntos x, pesos w
    """
    # Puntos y pesos de Gauss-Legendre para diferentes valores de n
    gauss_points = {
        2: ([-0.5773502692, 0.5773502692], [1.0000000000, 1.0000000000]),
        3: ([-0.7745966692, 0.0000000000, 0.7745966692], 
            [0.5555555556, 0.8888888889, 0.5555555556]),
        4: ([-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116],
            [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]),
        5: ([-0.9061798459, -0.5384693101, 0.0000000000, 0.5384693101, 0.9061798459],
            [0.2369268851, 0.4786286705, 0.5688888889, 0.4786286705, 0.2369268851])
    }
    
    if n not in gauss_points:
        raise ValueError(f"Número de puntos no soportado. Use 2, 3, 4 o 5.")
    
    x_i, w_i = gauss_points[n]
    
    # Transformación al intervalo [a,b]
    transform = lambda xi: (b-a)/2 * xi + (b+a)/2
    x_points = [transform(xi) for xi in x_i]
    
    # Convertir la función simbólica a una función numérica
    f = lambdify(x, func, "numpy")
    
    # Calcular la integral
    integral = (b-a)/2 * sum(w * f(x_p) for w, x_p in zip(w_i, x_points))
    
    # Evaluar la función en más puntos para el gráfico
    plot_x = np.linspace(a, b, 1000)
    plot_y = f(plot_x)
    y_points = [f(x_p) for x_p in x_points]
    
    return integral, x_points, y_points, plot_x, plot_y, w_i

def generate_gauss_graph(func, a, b, n, integral_value):
    """
    Genera una visualización estática del método de Gauss.
    """
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Obtener datos con pesos
        _, x_points, y_points, plot_x, plot_y, weights = gauss_quadrature(func, a, b, n)
        
        # Graficar la función
        ax.plot(plot_x, plot_y, 'b-', label=f"f(x) = {func}", zorder=3)
        
        # Sombrear el área de integración
        ax.fill_between(plot_x, plot_y, alpha=0.2, color='lightblue', 
                       where=(plot_x >= a) & (plot_x <= b),
                       label='Área de integración', zorder=1)
        
        # Añadir líneas verticales para delimitar el intervalo
        ax.axvline(x=a, color='green', linestyle='--', alpha=0.5, 
                   label='Límites de integración', zorder=2)
        ax.axvline(x=b, color='green', linestyle='--', alpha=0.5)
        
        # Graficar puntos de Gauss con un borde negro para mejor visibilidad
        ax.scatter(x_points, y_points, color='red', s=100, 
                  label='Puntos de Gauss', zorder=5,
                  edgecolor='black', linewidth=1)
        
        # Líneas verticales en los puntos de Gauss
        for x_p, y_p in zip(x_points, y_points):
            ax.vlines(x_p, 0, y_p, colors='red', linestyles='--', 
                     alpha=0.5, zorder=4)
        
        # Añadir información de los pesos en las etiquetas con fondo blanco
        for i, (x_p, y_p, w) in enumerate(zip(x_points, y_points, weights)):
            ax.annotate(f'w={w:.4f}', (x_p, y_p), 
                       xytext=(0, 10), textcoords='offset points', 
                       ha='center', bbox=dict(facecolor='white', 
                       alpha=0.8, edgecolor='none'))
        
        # Configuración del gráfico con borde
        ax.grid(True, zorder=0)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3, zorder=2)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3, zorder=2)
        
        # Añadir un borde al área del gráfico
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['top'].set_linewidth(1.5)
        ax.spines['right'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        
        title = f"Cuadratura de Gauss-Legendre con {n} puntos\n"
        title += f"∫({a},{b}) = {integral_value:.6f}"
        ax.set_title(title)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=300, bbox_inches='tight')
        plt.close()
        buffer.seek(0)
        
        return buffer
    except Exception as e:
        print(f"Error en generate_gauss_graph: {str(e)}")
        raise e

def generate_interactive_gauss_graph(func, a, b, n, integral_value):
    """
    Genera una visualización interactiva del método de Gauss.
    """
    try:
        # Obtener datos con pesos
        _, x_points, y_points, plot_x, plot_y, weights = gauss_quadrature(func, a, b, n)
        
        # Crear figura
        fig = go.Figure()
        
        # Añadir el área de integración como un relleno
        fig.add_trace(go.Scatter(
            x=plot_x,
            y=plot_y,
            fill='tozeroy',
            fillcolor='rgba(173, 216, 230, 0.3)',
            line=dict(width=0),
            name='Área de integración',
            showlegend=True
        ))
        
        # Añadir la función original
        fig.add_trace(go.Scatter(
            x=plot_x, 
            y=plot_y,
            name=f"f(x) = {func}",
            line=dict(color='blue', width=2)
        ))
        
        # Añadir líneas verticales para los límites de integración
        for x_val, name in [(a, 'a'), (b, 'b')]:
            fig.add_trace(go.Scatter(
                x=[x_val, x_val],
                y=[0, max(plot_y)],
                mode='lines',
                line=dict(color='green', width=2, dash='dash'),
                name=f'x = {name}',
                showlegend=True
            ))
        
        # Añadir puntos de Gauss con etiquetas de peso
        fig.add_trace(go.Scatter(
            x=x_points, 
            y=y_points,
            mode='markers+text',
            name='Puntos de Gauss',
            marker=dict(
                size=12, 
                color='red',
                line=dict(color='black', width=1)
            ),
            text=[f'w={w:.4f}' for w in weights],
            textposition='top center',
            textfont=dict(size=10),
            hovertemplate='x: %{x:.4f}<br>f(x): %{y:.4f}<br>w: %{text}<extra></extra>'
        ))
        
        # Configurar layout con borde
        title = f"Cuadratura de Gauss-Legendre con {n} puntos<br>"
        title += f"Valor aproximado: {integral_value:.6f}"
        
        fig.update_layout(
            title=title,
            xaxis_title="x",
            yaxis_title="f(x)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='white',
            xaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True
            ),
            yaxis=dict(
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True
            )
        )
        
        return fig.to_json()
    except Exception as e:
        print(f"Error en generate_interactive_gauss_graph: {str(e)}")
        raise e


# Ejemplo de uso:
if __name__ == "__main__":
    from sympy import sympify
    print("Ejemplo de integración numérica usando el método de cuadratura de Gauss-Legendre")
    a = float(input("Ingrese el valor de a: "))
    b = float(input("Ingrese el valor de b: "))
    n = int(input("Ingrese el número de puntos de Gauss (2, 3, 4 o 5): "))
    
    # Función por defecto: x^2 + 1
    func_str = "x**2 + 1"
    func = sympify(func_str)
    
    resultado, _, _, _, _, _ = gauss_quadrature(func, a, b, n)
    print(f"Resultado de la integral: {resultado}")