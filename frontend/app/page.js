"use client"

import { useState } from "react"
import { MethodsGrid } from "@/components/methods-grid"
import { CategoryNav } from "@/components/category-nav"
import { Header } from "@/components/header"
import { Introduction } from "@/components/introduction"

export default function HomePage() {
  const [activeCategory, setActiveCategory] = useState(null)

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="max-w-6xl mx-auto px-6 py-16">
        <div className="mb-16 text-center">
          <h1 className="text-5xl font-light text-gray-900 mb-6 tracking-tight">Métodos Numéricos</h1>
          <p className="text-xl text-gray-500 max-w-3xl mx-auto font-light leading-relaxed">
            Colección de métodos numéricos para resolver problemas matemáticos y de ingeniería
          </p>
        </div>

        <CategoryNav activeCategory={activeCategory} onCategoryChange={setActiveCategory} />

        {activeCategory ? <MethodsGrid activeCategory={activeCategory} /> : <Introduction />}
      </main>
    </div>
  )
}
