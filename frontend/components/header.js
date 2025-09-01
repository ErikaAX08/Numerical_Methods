import { Calculator } from "lucide-react"

export function Header() {
    return (
        <header className="bg-white">
            <div className="max-w-6xl mx-auto px-6 py-6">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center border border-white/30 shadow-lg hover:scale-110 transition-transform duration-300">
                            <Calculator className="h-6 w-6 text-black" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-black drop-shadow-sm">NumMethods</h1>
                            <p className="text-black text-sm">Métodos Numéricos Interactivos</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-6">
                        <button className="px-4 py-2 bg-white/20 backdrop-blur-sm text-black rounded-xl border border-white/30 hover:bg-white/30 hover:scale-105 transition-all duration-300 font-medium shadow-lg">
                            Docs
                        </button>
                        <button className="px-4 py-2 bg-white/20 backdrop-blur-sm text-black rounded-xl border border-white/30 hover:bg-white/30 hover:scale-105 transition-all duration-300 font-medium shadow-lg">
                            GitHub
                        </button>
                    </div>
                </div>
            </div>
        </header>
    )
}
