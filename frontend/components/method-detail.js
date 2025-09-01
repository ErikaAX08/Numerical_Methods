"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Calculator, BookOpen, Zap, Clock } from "lucide-react"
import Link from "next/link"

export function MethodDetail({ method }) {
    const [inputValues, setInputValues] = useState({})
    const [results, setResults] = useState(null)
    const [isCalculating, setIsCalculating] = useState(false)

    const handleInputChange = (name, value) => {
        setInputValues((prev) => ({ ...prev, [name]: value }))
    }

    const handleCalculate = async () => {
        setIsCalculating(true)
        // Simular cálculo
        setTimeout(() => {
            setResults({
                result: "Raíz encontrada: x = 2.000",
                iterations: 7,
                error: 0.0001,
                steps: [
                    "Iteración 1: x = 1.500, f(x) = -1.750",
                    "Iteración 2: x = 2.250, f(x) = 1.063",
                    "Iteración 3: x = 1.875, f(x) = -0.484",
                    "Iteración 4: x = 2.063, f(x) = 0.256",
                    "Iteración 5: x = 1.969, f(x) = -0.123",
                    "Iteración 6: x = 2.016, f(x) = 0.064",
                    "Iteración 7: x = 1.992, f(x) = -0.032",
                ],
            })
            setIsCalculating(false)
        }, 2000)
    }

    const getComplexityColor = (complexity) => {
        switch (complexity) {
            case "Básico":
                return "bg-green-100 text-green-800 border-green-200"
            case "Intermedio":
                return "bg-yellow-100 text-yellow-800 border-yellow-200"
            case "Avanzado":
                return "bg-red-100 text-red-800 border-red-200"
            default:
                return "bg-gray-100 text-gray-800 border-gray-200"
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
            <div className="container mx-auto px-4 py-8">
                {/* Header */}
                <div className="mb-8">
                    <Link href="/">
                        <Button variant="ghost" className="mb-4 hover:bg-white/50 transition-all duration-300">
                            <ArrowLeft className="w-4 h-4 mr-2" />
                            Volver al inicio
                        </Button>
                    </Link>

                    <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 border border-white/20 shadow-xl">
                        <div className="flex flex-wrap items-center gap-4 mb-4">
                            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                                {method.name}
                            </h1>
                            <Badge className={`${getComplexityColor(method.complexity)} border`}>{method.complexity}</Badge>
                        </div>
                        <p className="text-lg text-slate-600 leading-relaxed">{method.description}</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Información del Método */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Características */}
                        <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2 text-slate-800">
                                    <BookOpen className="w-5 h-5 text-blue-500" />
                                    Características del Método
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-xl border border-blue-100">
                                        <div className="flex items-center gap-2 mb-2">
                                            <Zap className="w-4 h-4 text-blue-500" />
                                            <span className="font-semibold text-slate-700">Convergencia</span>
                                        </div>
                                        <span className="text-slate-600">{method.convergence}</span>
                                    </div>
                                    <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl border border-purple-100">
                                        <div className="flex items-center gap-2 mb-2">
                                            <Clock className="w-4 h-4 text-purple-500" />
                                            <span className="font-semibold text-slate-700">Complejidad Temporal</span>
                                        </div>
                                        <span className="text-slate-600">{method.timeComplexity}</span>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        {/* Fórmulas */}
                        <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300">
                            <CardHeader>
                                <CardTitle className="text-slate-800">Fórmulas Matemáticas</CardTitle>
                                <CardDescription>Ecuaciones fundamentales del método</CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="bg-gradient-to-r from-slate-50 to-slate-100 p-6 rounded-xl border border-slate-200 mb-4">
                                    <h4 className="font-semibold text-slate-700 mb-2">Fórmula Principal:</h4>
                                    <code className="text-lg font-mono text-blue-600 bg-white px-3 py-1 rounded border">
                                        {method.formula}
                                    </code>
                                </div>

                                <div className="space-y-3">
                                    <h4 className="font-semibold text-slate-700">Algoritmo Detallado:</h4>
                                    {method.detailedFormula.map((step, index) => (
                                        <div
                                            key={index}
                                            className="flex items-start gap-3 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100"
                                        >
                                            <span className="bg-blue-500 text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-0.5">
                                                {index + 1}
                                            </span>
                                            <code className="text-slate-700 font-mono text-sm">{step}</code>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    {/* Calculadora Interactiva */}
                    <div className="space-y-6">
                        <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2 text-slate-800">
                                    <Calculator className="w-5 h-5 text-green-500" />
                                    Calculadora Interactiva
                                </CardTitle>
                                <CardDescription>Ingresa los parámetros para resolver</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {method.inputs.map((input) => (
                                    <div key={input.name} className="space-y-2">
                                        <label className="text-sm font-semibold text-slate-700 capitalize">{input.name}</label>
                                        <Input
                                            type={input.type}
                                            placeholder={input.placeholder}
                                            value={inputValues[input.name] || ""}
                                            onChange={(e) => handleInputChange(input.name, e.target.value)}
                                            className="bg-white/50 border-white/30 focus:bg-white focus:border-blue-300 transition-all duration-300"
                                        />
                                        <p className="text-xs text-slate-500">{input.description}</p>
                                    </div>
                                ))}

                                <Button
                                    onClick={handleCalculate}
                                    disabled={isCalculating}
                                    className="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                                >
                                    {isCalculating ? "Calculando..." : "Calcular"}
                                </Button>
                            </CardContent>
                        </Card>

                        {/* Resultados */}
                        {results && (
                            <Card className="bg-white/70 backdrop-blur-sm border-white/20 shadow-xl">
                                <CardHeader>
                                    <CardTitle className="text-slate-800">Resultados</CardTitle>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-4 rounded-xl border border-green-200">
                                        <h4 className="font-semibold text-green-800 mb-2">Resultado:</h4>
                                        <p className="text-green-700 font-mono">{results.result}</p>
                                    </div>

                                    <div className="grid grid-cols-2 gap-3">
                                        <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                                            <span className="text-xs text-blue-600 font-semibold">Iteraciones</span>
                                            <p className="text-blue-800 font-bold">{results.iterations}</p>
                                        </div>
                                        <div className="bg-purple-50 p-3 rounded-lg border border-purple-200">
                                            <span className="text-xs text-purple-600 font-semibold">Error</span>
                                            <p className="text-purple-800 font-bold">{results.error}</p>
                                        </div>
                                    </div>

                                    <div className="space-y-2">
                                        <h4 className="font-semibold text-slate-700">Pasos del Algoritmo:</h4>
                                        <div className="max-h-40 overflow-y-auto space-y-1">
                                            {results.steps.map((step, index) => (
                                                <div key={index} className="text-xs font-mono bg-slate-50 p-2 rounded border">
                                                    {step}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
