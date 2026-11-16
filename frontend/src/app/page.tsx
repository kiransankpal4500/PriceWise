"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import {
  Search,
  Sparkles,
  Flame,
  ArrowRight,
  ShieldCheck,
  Scale,
  Zap,
  TrendingDown,
  Smartphone,
  Laptop,
  Headphones,
  Watch,
  Tv,
  Camera,
  Cpu,
  Monitor,
} from "lucide-react";
import { fetchCategories, fetchProducts } from "@/lib/api";
import ProductCard from "@/components/ProductCard";

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  smartphones: <Smartphone className="h-6 w-6" />,
  laptops: <Laptop className="h-6 w-6" />,
  headphones: <Headphones className="h-6 w-6" />,
  earbuds: <Headphones className="h-6 w-6" />,
  smartwatches: <Watch className="h-6 w-6" />,
  televisions: <Tv className="h-6 w-6" />,
  cameras: <Camera className="h-6 w-6" />,
  "computer-components": <Cpu className="h-6 w-6" />,
  monitors: <Monitor className="h-6 w-6" />,
};

export default function HomePage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");

  const { data: categories = [] } = useQuery({
    queryKey: ["categories"],
    queryFn: fetchCategories,
  });

  const { data: trendingProducts = [] } = useQuery({
    queryKey: ["products-trending"],
    queryFn: () => fetchProducts({ sort_by: "rating", page_size: 6 }),
  });

  const { data: dealProducts = [] } = useQuery({
    queryKey: ["products-deals"],
    queryFn: () => fetchProducts({ sort_by: "price_asc", page_size: 4 }),
  });

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <div className="space-y-16 pb-16">
      {/* 1. HERO SECTION */}
      <section className="relative overflow-hidden pt-12 pb-20 md:pt-20 md:pb-28">
        {/* Ambient Glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-b from-blue-600/15 via-cyan-500/10 to-transparent blur-3xl pointer-events-none -z-10" />

        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-400 backdrop-blur-md">
            <Sparkles className="h-3.5 w-3.5 text-cyan-400 animate-pulse" />
            <span>AI-Driven Electronics Intelligence • India Market</span>
          </div>

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
            Stop Overpaying for <span className="bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 bg-clip-text text-transparent">Electronics</span>.
          </h1>

          <p className="text-base sm:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Real-time price comparison across Amazon and Flipkart, technical specification analysis,
            and honest Gemini AI shopping advice in Indian Rupees.
          </p>

          {/* Search Hero Box */}
          <form onSubmit={handleSearchSubmit} className="max-w-2xl mx-auto relative mt-6">
            <div className="flex items-center rounded-2xl border border-slate-700 bg-slate-900/90 p-2 shadow-2xl shadow-blue-500/10 backdrop-blur-xl focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20 transition-all">
              <Search className="ml-3 h-5 w-5 text-slate-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search Samsung Galaxy S25, MacBook Air M3, Sony XM5..."
                className="w-full bg-transparent px-3 py-2 text-sm sm:text-base text-white placeholder-slate-500 focus:outline-none"
              />
              <button
                type="submit"
                className="flex items-center gap-1.5 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-500 transition-colors shadow-md"
              >
                <span>Compare</span>
                <ArrowRight className="h-4 w-4" />
              </button>
            </div>
          </form>

          {/* Quick AI Prompts */}
          <div className="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs text-slate-400">
            <span className="font-medium text-slate-500">Ask Gemini AI:</span>
            <Link
              href="/assistant?prompt=Best%20smartphone%20under%2050000%20with%20great%20camera"
              className="rounded-full border border-slate-800 bg-slate-900/60 px-3 py-1 hover:border-cyan-500 hover:text-cyan-300 transition-colors"
            >
              &ldquo;Best phone under ₹50,000 for camera&rdquo;
            </Link>
            <Link
              href="/assistant?prompt=Laptop%20for%20programming%20and%20AI%20development%20under%201%20lakh"
              className="rounded-full border border-slate-800 bg-slate-900/60 px-3 py-1 hover:border-cyan-500 hover:text-cyan-300 transition-colors"
            >
              &ldquo;Laptop for coding & AI under ₹1 Lakh&rdquo;
            </Link>
          </div>
        </div>
      </section>

      {/* 2. CATEGORIES GRID */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-white">Browse Categories</h2>
            <p className="text-sm text-slate-400 mt-1">Explore verified electronics across India</p>
          </div>
          <Link href="/search" className="text-sm font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1">
            <span>View All</span>
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
          {categories.map((cat) => (
            <Link
              key={cat.id}
              href={`/search?category=${cat.slug}`}
              className="group flex flex-col items-center justify-center rounded-2xl border border-slate-800 bg-slate-900/40 p-5 text-center transition-all duration-300 hover:border-blue-500/50 hover:bg-slate-900 hover:shadow-lg hover:shadow-blue-500/10"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-800 text-slate-300 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                {CATEGORY_ICONS[cat.slug] || <Cpu className="h-6 w-6" />}
              </div>
              <span className="mt-3 text-sm font-semibold text-slate-200 group-hover:text-white transition-colors">
                {cat.name}
              </span>
              <span className="mt-1 text-xs text-slate-500">
                {cat.product_count} {cat.product_count === 1 ? "device" : "devices"}
              </span>
            </Link>
          ))}
        </div>
      </section>

      {/* 3. TRENDING PRODUCTS */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-blue-400 mb-1">
              <Zap className="h-3.5 w-3.5" />
              <span>Verified Market Prices</span>
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-white">Trending in India</h2>
          </div>
          <Link href="/search" className="text-sm font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1">
            <span>Explore Catalog</span>
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {trendingProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      {/* 4. AI SHOPPING ASSISTANT BANNER */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-3xl border border-cyan-500/30 bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/80 p-8 sm:p-12">
          <div className="max-w-2xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full bg-cyan-500/10 px-3 py-1 text-xs font-semibold text-cyan-400 border border-cyan-500/20">
              <Sparkles className="h-3.5 w-3.5" />
              <span>Powered by Google Gemini AI</span>
            </div>
            <h3 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
              Meet Your Personal Electronics Advisor
            </h3>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              Tell PriceWise your budget, workflow needs (gaming, video editing, photography, battery endurance),
              and let our deterministic scoring engine and Gemini synthesize the ideal recommendations with zero fake data.
            </p>
            <div className="pt-2">
              <Link
                href="/assistant"
                className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-cyan-500/20 hover:from-cyan-400 hover:to-blue-500 transition-all"
              >
                <span>Start AI Consultation</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 5. TOP VALUE DEALS */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-amber-400 mb-1">
              <Flame className="h-3.5 w-3.5" />
              <span>Biggest Reductions</span>
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-white">Top Deals & Price Drops</h2>
          </div>
          <Link href="/deals" className="text-sm font-semibold text-amber-400 hover:text-amber-300 flex items-center gap-1">
            <span>View All Deals</span>
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {dealProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      {/* 6. PLATFORM TRUST GUARANTEES */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-8">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 border-t border-slate-900 pt-10">
          <div className="flex items-start gap-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">₹0 Cost Policy</h4>
              <p className="mt-1 text-xs text-slate-400 leading-relaxed">
                Operating strictly with free services, ethical scrapers, and official free Gemini tier without subscription costs.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Scale className="h-5 w-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">Strict Variant Isolation</h4>
              <p className="mt-1 text-xs text-slate-400 leading-relaxed">
                Never conflates 128GB vs 256GB storage or RAM configurations. RapidFuzz token matching guarantees precision.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <TrendingDown className="h-5 w-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">Append-Only Price History</h4>
              <p className="mt-1 text-xs text-slate-400 leading-relaxed">
                Observations are never modified or fabricated. Real chronological trends across Amazon and Flipkart.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
