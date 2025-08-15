import { Calculator, BookOpen, Github } from "lucide-react"

export function Header() {
    return (
        <header className="bg-white shadow-sm">
            <div className="container mx-auto px-4 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-600 rounded-lg">
                            <Calculator className="h-6 w-6 text-white" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-slate-800">NumMethods</h1>
                            <p className="text-sm text-slate-500">Métodos Numéricos</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        <button className="flex items-center gap-2 px-4 py-2 text-slate-600 hover:text-blue-600 transition-colors">
                            <BookOpen className="h-4 w-4" />
                            <span className="hidden sm:inline">Documentación</span>
                        </button>
                        <button className="flex items-center gap-2 px-4 py-2 text-slate-600 hover:text-blue-600 transition-colors">
                            <Github className="h-4 w-4" />
                            <span className="hidden sm:inline">GitHub</span>
                        </button>
                    </div>
                </div>
            </div>
        </header>
    )
}
