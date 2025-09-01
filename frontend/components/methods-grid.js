import { MethodCard } from "./method-card"

const methods = [
    // Raíces de Ecuaciones
    {
        id: "bisection",
        name: "Método de Bisección",
        category: "roots",
        description: "Encuentra raíces mediante división sucesiva del intervalo",
        complexity: "Básico",
        convergence: "Lineal",
        icon: "📐",
    },
    {
        id: "newton-raphson",
        name: "Newton-Raphson",
        category: "roots",
        description: "Método iterativo usando derivadas para encontrar raíces",
        complexity: "Intermedio",
        convergence: "Cuadrática",
        icon: "🎯",
    },
    {
        id: "secant",
        name: "Método de la Secante",
        category: "roots",
        description: "Aproximación de Newton-Raphson sin calcular derivadas",
        complexity: "Intermedio",
        convergence: "Superlineal",
        icon: "📏",
    },
    {
        id: "false-position",
        name: "Falsa Posición",
        category: "roots",
        description: "Combina bisección con interpolación lineal",
        complexity: "Básico",
        convergence: "Lineal",
        icon: "🎪",
    },
    {
        id: "fixed-point",
        name: "Punto Fijo",
        category: "roots",
        description: "Encuentra puntos donde f(x) = x",
        complexity: "Básico",
        convergence: "Lineal",
        icon: "📍",
    },
    {
        id: "muller",
        name: "Método de Müller",
        category: "roots",
        description: "Usa interpolación cuadrática para encontrar raíces complejas",
        complexity: "Avanzado",
        convergence: "Cuadrática",
        icon: "🌀",
    },

    // Sistemas Lineales
    {
        id: "gaussian",
        name: "Eliminación Gaussiana",
        category: "linear",
        description: "Resuelve sistemas mediante eliminación hacia adelante",
        complexity: "Básico",
        convergence: "Directo",
        icon: "🔢",
    },
    {
        id: "lu-decomposition",
        name: "Descomposición LU",
        category: "linear",
        description: "Factoriza matriz en triangular inferior y superior",
        complexity: "Intermedio",
        convergence: "Directo",
        icon: "🧩",
    },
    {
        id: "gauss-seidel",
        name: "Gauss-Seidel",
        category: "linear",
        description: "Método iterativo para sistemas lineales grandes",
        complexity: "Intermedio",
        convergence: "Iterativo",
        icon: "🔄",
    },
    {
        id: "jacobi",
        name: "Método de Jacobi",
        category: "linear",
        description: "Método iterativo paralelo para sistemas lineales",
        complexity: "Intermedio",
        convergence: "Iterativo",
        icon: "⚡",
    },
    {
        id: "cholesky",
        name: "Descomposición de Cholesky",
        category: "linear",
        description: "Para matrices simétricas definidas positivas",
        complexity: "Avanzado",
        convergence: "Directo",
        icon: "💎",
    },

    // Interpolación
    {
        id: "lagrange",
        name: "Interpolación de Lagrange",
        category: "interpolation",
        description: "Polinomio que pasa por todos los puntos dados",
        complexity: "Intermedio",
        convergence: "Exacto",
        icon: "📈",
    },
    {
        id: "newton-divided",
        name: "Diferencias Divididas de Newton",
        category: "interpolation",
        description: "Construcción eficiente de polinomios interpolantes",
        complexity: "Intermedio",
        convergence: "Exacto",
        icon: "🔺",
    },
    {
        id: "spline",
        name: "Splines Cúbicos",
        category: "interpolation",
        description: "Interpolación suave por tramos con continuidad",
        complexity: "Avanzado",
        convergence: "Suave",
        icon: "🌊",
    },
    {
        id: "least-squares",
        name: "Mínimos Cuadrados",
        category: "interpolation",
        description: "Ajuste de curvas minimizando el error cuadrático",
        complexity: "Intermedio",
        convergence: "Aproximado",
        icon: "📊",
    },

    // Integración Numérica
    {
        id: "trapezoidal",
        name: "Regla del Trapecio",
        category: "integration",
        description: "Aproxima el área usando trapecios",
        complexity: "Básico",
        convergence: "O(h²)",
        icon: "📐",
    },
    {
        id: "simpson",
        name: "Regla de Simpson",
        category: "integration",
        description: "Usa parábolas para mayor precisión",
        complexity: "Intermedio",
        convergence: "O(h⁴)",
        icon: "🎪",
    },
    {
        id: "gaussian-quad",
        name: "Cuadratura Gaussiana",
        category: "integration",
        description: "Puntos y pesos óptimos para integración",
        complexity: "Avanzado",
        convergence: "Exponencial",
        icon: "🎯",
    },
    {
        id: "romberg",
        name: "Integración de Romberg",
        category: "integration",
        description: "Extrapolación de Richardson para alta precisión",
        complexity: "Avanzado",
        convergence: "O(h^2n)",
        icon: "🏛️",
    },

    // Ecuaciones Diferenciales
    {
        id: "euler",
        name: "Método de Euler",
        category: "differential",
        description: "Método más simple para EDOs de primer orden",
        complexity: "Básico",
        convergence: "O(h)",
        icon: "➡️",
    },
    {
        id: "runge-kutta",
        name: "Runge-Kutta 4to Orden",
        category: "differential",
        description: "Método clásico de alta precisión para EDOs",
        complexity: "Intermedio",
        convergence: "O(h⁴)",
        icon: "🚀",
    },
    {
        id: "adams-bashforth",
        name: "Adams-Bashforth",
        category: "differential",
        description: "Método multipaso explícito",
        complexity: "Avanzado",
        convergence: "O(h^k)",
        icon: "🔗",
    },
    {
        id: "predictor-corrector",
        name: "Predictor-Corrector",
        category: "differential",
        description: "Combina métodos explícitos e implícitos",
        complexity: "Avanzado",
        convergence: "Alta",
        icon: "🎪",
    },
    {
        id: "finite-difference",
        name: "Diferencias Finitas",
        category: "differential",
        description: "Para ecuaciones diferenciales parciales",
        complexity: "Avanzado",
        convergence: "O(h²)",
        icon: "🌐",
    },
]

export function MethodsGrid({ activeCategory }) {
    const filteredMethods = methods.filter((method) => method.category === activeCategory)

    return (
        <div>
            <div className="mb-6 text-center">
                <h2 className="text-2xl font-bold text-slate-800 mb-2">{getCategoryTitle(activeCategory)}</h2>
                <p className="text-slate-600">{filteredMethods.length} métodos disponibles en esta categoría</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredMethods.map((method) => (
                    <MethodCard key={method.id} method={method} />
                ))}
            </div>
        </div>
    )
}

function getCategoryTitle(category) {
    const titles = {
        roots: "Raíces de Ecuaciones",
        linear: "Sistemas Lineales",
        interpolation: "Interpolación",
        integration: "Integración Numérica",
        differential: "Ecuaciones Diferenciales",
    }
    return titles[category] || "Métodos"
}
