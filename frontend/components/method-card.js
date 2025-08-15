import { Card, CardHeader, CardContent } from "./ui/card";

// Colores dificultad de cada método
const complexityColors = {
    Basic: { text: "text-green-700", bg: "from-green-400 to-emerald-500" },
    Intermediate: { text: "text-yellow-700", bg: "from-yellow-400 to-orange-500" },
    Avanced: { text: "text-red-700", bg: "from-red-400 to-pink-500" },
}

export function MethodCard({method}) {
    return (
        <Card className="group relative hover:shadow-2xl hover:shadow-purple-500/20 transition-all duration-500 cursor-pointer border-2 border-gray-100 hover:border-transparent bg-white rounded-3xl overflow-hidden hover:-translate-y-2">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-blue-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

            <CardHeader className="pb-4 relative z-10">
                <div className="flex items-start justify-between mb-4">
                    <div className="text-4xl group-hover:scale-110 transition-transform duration-300">{method.icon}</div>
                    <span className={`px-3 py-1 bg-red-800 text-white rounded-full text-xs font-bold shadow-lg`}>{method.complexity}</span>
                </div>
                <h3 className="font-bold text-xl text-gray-900 group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-blue-600 group-hover:bg-clip-text group-hover:text-transparent transition-all duration-300">{method.name}</h3>
            </CardHeader>

            <CardContent className="pt-0 relative z-10">
                <p className="text-gray-600 mb-6 leading-relaxed font-medium">{method.description}</p>

                <div className="space-y-4">
                    <div className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"></span>
                        <span className="text-sm text-gray-600 font-medium">Convergencia: {method.convergence}</span>
                    </div>

                    <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                        <button className="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-xl font-bold text-sm hover:from-purple-600 hover:to-blue-600 hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl">
                            Ver detalles
                        </button>
                        <button className="px-4 py-2 bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 rounded-xl font-bold text-sm hover:from-gray-200 hover:to-gray-300 hover:scale-105 transition-all duration-300 shadow-md hover:shadow-lg">
                            Implementar
                        </button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}