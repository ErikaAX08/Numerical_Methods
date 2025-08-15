"use client";

import { CategoryNav } from "@/components/category-nav";
import { Header } from "@/components/header";
import { Introduction } from "@/components/introduction";
import { MethodCard } from "@/components/method-card";
import { MethodGrid } from "@/components/methods-grid";
import { useState } from "react";

export default function Home() {

  // 
  const [activeCategory, setActiveCategory] = useState(null);

  return (
    <>
      <div className="min-h-screen bg-white-60">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <div className="mb-8 text-center">
            <h1 className="text-4xl font-bold text-slate-800 mb-4">Métodos Numéricos</h1>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Explora una colección completa de métodos numéricos organizados por categorías para resolver problemas
              matemáticos y de ingeniería.
            </p>
          </div>

          <CategoryNav 
            activeCategory={activeCategory}
            onCategoryChange={setActiveCategory}
          />
          {activeCategory ? <MethodGrid activeCategory={activeCategory} /> : <Introduction />}
        </main>
      </div>
    </>
  );
}
