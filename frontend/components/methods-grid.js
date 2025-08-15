import { MethodCard } from "./method-card";

// Array de todos los métodos
const methods = [
    {
        id: "bisection",
        name: "Método de Bisección",
        description: "Encuentra raíces mediante división sucesiva del intervalo",
        complexity: "Básico",
        convergence: "Lineal",
        icon: "📐"
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
]

export function MethodGrid({ activeCategory }) {
    return (
        <div>
            <div className="mb-6 text-center">
                <h2 className="text-2xl font-bold text-slate-800 mb-2">{activeCategory}</h2>
                <p className="text-slate-600">{methods.length} métodos disponibles en esta categoría</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {methods.map((method) => (
                    <MethodCard key={method.id} method={method} />
                ))}
            </div>
        </div>
    );
}