import { MethodDetail } from "@/components/method-detail"
import { notFound } from "next/navigation"

const methods = [
    // Raíces de Ecuaciones
    {
        id: "bisection",
        name: "Método de Bisección",
        category: "roots",
        description:
            "El método de bisección es un algoritmo de búsqueda de raíces que funciona dividiendo repetidamente un intervalo por la mitad y seleccionando el subintervalo que contiene la raíz.",
        complexity: "Básico",
        convergence: "Lineal",
        timeComplexity: "O(log n)",
        spaceComplexity: "O(1)",
        formula: "x_c = (a + b) / 2",
        detailedFormula: [
            "Sea f(x) una función continua en [a,b] con f(a)·f(b) < 0",
            "x_c = (a + b) / 2",
            "Si f(a)·f(x_c) < 0, entonces b = x_c",
            "Si f(a)·f(x_c) > 0, entonces a = x_c",
            "Repetir hasta |b - a| < tolerancia",
        ],
        inputs: [
            { name: "función", type: "text", placeholder: "x^2 - 4", description: "Función f(x)" },
            { name: "a", type: "number", placeholder: "0", description: "Límite inferior del intervalo" },
            { name: "b", type: "number", placeholder: "3", description: "Límite superior del intervalo" },
            { name: "tolerancia", type: "number", placeholder: "0.001", description: "Error máximo permitido" },
            { name: "maxIteraciones", type: "number", placeholder: "100", description: "Número máximo de iteraciones" },
        ],
    },
    {
        id: "newton-raphson",
        name: "Newton-Raphson",
        category: "roots",
        description:
            "Método iterativo que utiliza la derivada de la función para encontrar raíces con convergencia cuadrática.",
        complexity: "Intermedio",
        convergence: "Cuadrática",
        timeComplexity: "O(log log n)",
        spaceComplexity: "O(1)",
        formula: "x_{n+1} = x_n - f(x_n)/f'(x_n)",
        detailedFormula: [
            "x_{n+1} = x_n - f(x_n)/f'(x_n)",
            "Donde f'(x_n) es la derivada de f evaluada en x_n",
            "Requiere un valor inicial x_0 cercano a la raíz",
            "Converge cuadráticamente si f'(x) ≠ 0 en la raíz",
        ],
        inputs: [
            { name: "función", type: "text", placeholder: "x^2 - 4", description: "Función f(x)" },
            { name: "derivada", type: "text", placeholder: "2*x", description: "Derivada f'(x)" },
            { name: "x0", type: "number", placeholder: "1", description: "Valor inicial" },
            { name: "tolerancia", type: "number", placeholder: "0.001", description: "Error máximo permitido" },
            { name: "maxIteraciones", type: "number", placeholder: "100", description: "Número máximo de iteraciones" },
        ],
    },
    // Métodos adicionales
    {
        id: "gaussian",
        name: "Eliminación Gaussiana",
        category: "linear",
        description:
            "Algoritmo para resolver sistemas de ecuaciones lineales mediante eliminación hacia adelante y sustitución hacia atrás.",
        complexity: "Básico",
        convergence: "Directo",
        timeComplexity: "O(n³)",
        spaceComplexity: "O(n²)",
        formula: "Ax = b → [A|b] → [U|c] → x",
        detailedFormula: [
            "Formar la matriz aumentada [A|b]",
            "Eliminación hacia adelante: convertir A en matriz triangular superior U",
            "Para i = 1 hasta n-1:",
            "  Para j = i+1 hasta n:",
            "    factor = a[j][i] / a[i][i]",
            "    Fila[j] = Fila[j] - factor × Fila[i]",
            "Sustitución hacia atrás para encontrar x",
        ],
        inputs: [
            {
                name: "matriz",
                type: "text",
                placeholder: "[[2,1,-1],[1,3,2],[-1,2,1]]",
                description: "Matriz de coeficientes A",
            },
            { name: "vector", type: "text", placeholder: "[8,13,5]", description: "Vector de términos independientes b" },
        ],
    },
    {
        id: "lagrange",
        name: "Interpolación de Lagrange",
        category: "interpolation",
        description:
            "Método para encontrar un polinomio que pase exactamente por todos los puntos dados usando la fórmula de Lagrange.",
        complexity: "Intermedio",
        convergence: "Exacto",
        timeComplexity: "O(n²)",
        spaceComplexity: "O(n)",
        formula: "P(x) = Σ y_i × L_i(x)",
        detailedFormula: [
            "P(x) = Σ(i=0 hasta n) y_i × L_i(x)",
            "Donde L_i(x) = Π(j=0 hasta n, j≠i) (x - x_j)/(x_i - x_j)",
            "L_i(x) son los polinomios base de Lagrange",
            "P(x_i) = y_i para todos los puntos dados",
        ],
        inputs: [
            { name: "puntos", type: "text", placeholder: "[(0,1),(1,4),(2,9)]", description: "Puntos (x,y) para interpolar" },
            { name: "valorX", type: "number", placeholder: "1.5", description: "Valor de x para evaluar P(x)" },
        ],
    },
    {
        id: "trapezoidal",
        name: "Regla del Trapecio",
        category: "integration",
        description: "Método de integración numérica que aproxima el área bajo la curva usando trapecios.",
        complexity: "Básico",
        convergence: "O(h²)",
        timeComplexity: "O(n)",
        spaceComplexity: "O(1)",
        formula: "∫f(x)dx ≈ (h/2)[f(a) + 2Σf(x_i) + f(b)]",
        detailedFormula: [
            "Dividir [a,b] en n subintervalos de ancho h = (b-a)/n",
            "x_i = a + i×h para i = 0,1,...,n",
            "Área ≈ (h/2)[f(x_0) + 2f(x_1) + 2f(x_2) + ... + 2f(x_{n-1}) + f(x_n)]",
            "Error = -(b-a)h²/12 × f''(ξ) para algún ξ ∈ [a,b]",
        ],
        inputs: [
            { name: "función", type: "text", placeholder: "x^2", description: "Función f(x) a integrar" },
            { name: "a", type: "number", placeholder: "0", description: "Límite inferior de integración" },
            { name: "b", type: "number", placeholder: "2", description: "Límite superior de integración" },
            { name: "n", type: "number", placeholder: "10", description: "Número de subintervalos" },
        ],
    },
    {
        id: "euler",
        name: "Método de Euler",
        category: "differential",
        description: "Método numérico más simple para resolver ecuaciones diferenciales ordinarias de primer orden.",
        complexity: "Básico",
        convergence: "O(h)",
        timeComplexity: "O(n)",
        spaceComplexity: "O(1)",
        formula: "y_{n+1} = y_n + h × f(x_n, y_n)",
        detailedFormula: [
            "Para resolver y' = f(x,y) con y(x_0) = y_0",
            "Dividir [x_0, x_f] en n pasos de tamaño h = (x_f - x_0)/n",
            "x_{n+1} = x_n + h",
            "y_{n+1} = y_n + h × f(x_n, y_n)",
            "Repetir hasta alcanzar x_f",
        ],
        inputs: [
            { name: "ecuacion", type: "text", placeholder: "x + y", description: "f(x,y) en y' = f(x,y)" },
            { name: "x0", type: "number", placeholder: "0", description: "Valor inicial de x" },
            { name: "y0", type: "number", placeholder: "1", description: "Valor inicial de y" },
            { name: "xf", type: "number", placeholder: "2", description: "Valor final de x" },
            { name: "h", type: "number", placeholder: "0.1", description: "Tamaño del paso" },
        ],
    },
]

export default function MethodPage({ params }) {
    const method = methods.find((m) => m.id === params.id)

    if (!method) {
        notFound()
    }

    return <MethodDetail method={method} />
}

export function generateStaticParams() {
    return methods.map((method) => ({
        id: method.id,
    }))
}
