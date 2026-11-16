"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Flame, TrendingDown, Tag, Sparkles } from "lucide-react";
import { fetchProducts } from "@/lib/api";
import ProductCard from "@/components/ProductCard";

export default function DealsPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>("");

  const { data: products = [], isLoading } = useQuery({
    queryKey: ["deals", selectedCategory],
    queryFn: () => fetchProducts({ category_slug: selectedCategory || undefined, sort_by: "price_asc", page_size: 20 }),
  });

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header Banner */}
      <div className="rounded-3xl border border-amber-500/20 bg-gradient-to-r from-amber-950/40 via-slate-900 to-slate-950 p-8 space-y-3">
        <div className="inline-flex items-center gap-1.5 rounded-full bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-400 border border-amber-500/20">
          <Flame className="h-4 w-4" />
          <span>Real Discount Intelligence</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white sm:text-4xl">
          Top Verified Electronics Deals
        </h1>
        <p className="text-sm text-slate-300 max-w-2xl leading-relaxed">
          Every deal listed here is verified against historical price observations. We distinguish between true price drops and artificial MRP inflation.
        </p>
      </div>

      {/* Category Pills */}
      <div className="flex flex-wrap gap-2 text-xs font-medium">
        <button
          onClick={() => setSelectedCategory("")}
          className={`rounded-xl px-4 py-2 transition-all ${
            selectedCategory === ""
              ? "bg-amber-500 text-black font-bold shadow-md shadow-amber-500/20"
              : "border border-slate-800 bg-slate-900/60 text-slate-300 hover:bg-slate-800 hover:text-white"
          }`}
        >
          All Deals
        </button>
        {["smartphones", "laptops", "headphones", "smartwatches", "televisions"].map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`rounded-xl px-4 py-2 capitalize transition-all ${
              selectedCategory === cat
                ? "bg-amber-500 text-black font-bold shadow-md shadow-amber-500/20"
                : "border border-slate-800 bg-slate-900/60 text-slate-300 hover:bg-slate-800 hover:text-white"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Deals Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-80 rounded-2xl border border-slate-800 bg-slate-900/40 animate-pulse" />
          ))}
        </div>
      ) : products.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      ) : (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-12 text-center text-sm text-slate-400">
          No deals currently available in this category.
        </div>
      )}
    </div>
  );
}
