import { cn } from "@/lib/utils";

// Array objetos categorías
const categories = [
    { id: "roots", name: "Raíces de Ecuaciones", count: 6, color: "from-red-500 to-pink-500" },
    { id: "linear", name: "Sistemas Lineales", count: 5, color: "from-blue-500 to-indigo-500" },
    { id: "interpolation", name: "Interpolación", count: 4, color: "from-green-500 to-emerald-500" },
    { id: "integration", name: "Integración Numérica", count: 4, color: "from-purple-500 to-violet-500" },
    { id: "differential", name: "Ecuaciones Diferenciales", count: 5, color: "from-orange-500 to-amber-500" },
]

export function CategoryNav({ activeCategory, onCategoryChange }) {
    return (
        <div className="mb-8">
            <div className="flex flex-wrap gap-2 justify-center">
                <button
                    onClick={() => onCategoryChange(null)}
                    className={cn(
                        "px-8 py-4 rounded-2xl text-sm font-bold transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 border-2",
                        activeCategory === null
                            ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white border-transparent shadow-purple-500/30"
                            : "bg-white text-gray-700 border-gray-200 hover:border-purple-300 hover:shadow-purple-500/20",
                    )}
                >
                    Inicio
                </button>

                {categories.map((category) => (
                    <button
                        key={category.id}
                        onClick={() => onCategoryChange(category.id)}
                        className={cn(
                            "px-8 py-4 rounded-2xl text-sm font-bold transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 border-2 relative overflow-hidden",
                            activeCategory === category.id
                                ? `bg-gradient-to-r ${category.color} text-white border-transparent`
                                : "bg-white text-gray-700 border-gray-200 hover:border-gray-300",
                        )}
                    >
                        {activeCategory !== category.id && (
                            <div
                                className={`absolute inset-0 bg-gradient-to-r ${category.color} opacity-0 hover:opacity-10 transition-opacity duration-300`}
                            ></div>
                        )}
                        <span className="relative z-10">
                            {category.name}
                            <span className="ml-2 text-xs opacity-75 font-normal">({category.count})</span>
                        </span>
                    </button>
                ))}
            </div>
        </div>
    );
}