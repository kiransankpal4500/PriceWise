"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import {
  Compass,
  ArrowRight,
  Sparkles,
  Smartphone,
  Laptop,
  Headphones,
  Watch,
  Monitor,
  Check,
  ChevronRight,
  RotateCcw,
} from "lucide-react";
import { fetchRecommendations } from "@/lib/api";
import ProductCard from "./ProductCard";

interface StepOption {
  id: string;
  label: string;
  icon?: any;
  subtext?: string;
}

const CATEGORIES: StepOption[] = [
  { id: "smartphones", label: "Smartphone", icon: Smartphone, subtext: "iPhones, Samsung Galaxy, Flagships" },
  { id: "laptops", label: "Laptop", icon: Laptop, subtext: "MacBooks, Ultrabooks, Gaming Rigs" },
  { id: "earbuds", label: "Earbuds / Audio", icon: Headphones, subtext: "TWS Earbuds & ANC Cans" },
  { id: "smartwatches", label: "Smartwatch", icon: Watch, subtext: "Apple Watch, Galaxy, Fitness" },
  { id: "monitors", label: "Monitor / TV", icon: Monitor, subtext: "4K Displays, High-refresh panels" },
];

const BUDGETS: StepOption[] = [
  { id: "25000", label: "Under ₹25,000", subtext: "Budget Champions & Maximum Value" },
  { id: "50000", label: "₹25,000 – ₹50,000", subtext: "Mid-Range Sweet Spot" },
  { id: "100000", label: "₹50,000 – ₹1,00,000", subtext: "Premium & High Performance" },
  { id: "250000", label: "₹1,00,000+", subtext: "No-Compromise Flagships" },
];

const PRIORITIES: StepOption[] = [
  { id: "value", label: "Best Value for Money", subtext: "Maximize hardware per rupee spent" },
  { id: "camera", label: "Superior Camera & Display", subtext: "OLED/AMOLED screens & computational photography" },
  { id: "battery", label: "All-Day Battery & Longevity", subtext: "Efficient silicon & fast charging support" },
  { id: "performance", label: "Maximum Sustained Performance", subtext: "Latest Apple Silicon / Snapdragon / Core i7+" },
];

export default function ProductMatchmaker() {
  const router = useRouter();
  const [step, setStep] = useState<1 | 2 | 3 | 4>(1);
  const [selectedCategory, setSelectedCategory] = useState<string>("smartphones");
  const [selectedBudget, setSelectedBudget] = useState<string>("50000");
  const [selectedPriority, setSelectedPriority] = useState<string>("value");

  const { data: recData, isLoading } = useQuery({
    queryKey: ["matchmakerRecs", selectedCategory, selectedBudget, selectedPriority],
    queryFn: () =>
      fetchRecommendations({
        category_slug: selectedCategory,
        max_budget: parseFloat(selectedBudget),
        intent: selectedPriority,
      }),
    enabled: step === 4,
  });

  const handleReset = () => {
    setStep(1);
    setSelectedCategory("smartphones");
    setSelectedBudget("50000");
    setSelectedPriority("value");
  };

  return (
    <div className="rounded-3xl border border-slate-800 bg-gradient-to-b from-slate-900/80 via-slate-900/40 to-slate-950 p-6 sm:p-10 backdrop-blur-xl relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-0 right-1/4 -z-10 h-64 w-64 rounded-full bg-blue-600/10 blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-1/4 -z-10 h-64 w-64 rounded-full bg-cyan-600/10 blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-800/80">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20">
            <Compass className="h-6 w-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                Interactive Decision Engine
              </span>
              <span className="rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 text-[10px] font-semibold">
                3-Step Wizard
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
              AI Electronics Matchmaker
            </h2>
          </div>
        </div>

        {/* Progress pills */}
        <div className="flex items-center gap-2">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`h-2 rounded-full transition-all duration-300 ${
                step === s
                  ? "w-8 bg-cyan-400"
                  : step > s
                  ? "w-3 bg-emerald-400"
                  : "w-3 bg-slate-800"
              }`}
            />
          ))}
          {step === 4 && (
            <button
              onClick={handleReset}
              className="ml-3 flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              <span>Start Over</span>
            </button>
          )}
        </div>
      </div>

      {/* WIZARD CONTENT */}
      <div className="mt-8">
        {/* STEP 1: CATEGORY */}
        {step === 1 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <h3 className="text-lg font-bold text-white">Step 1: What device are you shopping for?</h3>
              <p className="text-xs text-slate-400 mt-1">
                Select your primary electronics category to calibrate hardware specifications.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {CATEGORIES.map((cat) => {
                const Icon = cat.icon;
                const isSelected = selectedCategory === cat.id;
                return (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedCategory(cat.id)}
                    className={`flex items-start gap-4 rounded-2xl border p-4 text-left transition-all ${
                      isSelected
                        ? "border-cyan-500 bg-cyan-950/30 shadow-lg shadow-cyan-500/10"
                        : "border-slate-800 bg-slate-900/40 hover:border-slate-700 hover:bg-slate-900/80"
                    }`}
                  >
                    <div
                      className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${
                        isSelected ? "bg-cyan-500 text-white" : "bg-slate-800 text-slate-400"
                      }`}
                    >
                      <Icon className="h-5 w-5" />
                    </div>
                    <div>
                      <span className="block text-sm font-bold text-white">{cat.label}</span>
                      <span className="block text-xs text-slate-400 mt-0.5">{cat.subtext}</span>
                    </div>
                  </button>
                );
              })}
            </div>

            <div className="flex justify-end pt-4">
              <button
                onClick={() => setStep(2)}
                className="flex items-center gap-2 rounded-xl bg-cyan-600 px-6 py-3 text-xs font-bold text-white hover:bg-cyan-500 transition-colors shadow-lg shadow-cyan-500/20"
              >
                <span>Continue to Budget</span>
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: BUDGET */}
        {step === 2 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <h3 className="text-lg font-bold text-white">Step 2: What is your target budget?</h3>
              <p className="text-xs text-slate-400 mt-1">
                Prices are calibrated in Indian Rupees (₹) with real-time marketplace offers.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {BUDGETS.map((b) => {
                const isSelected = selectedBudget === b.id;
                return (
                  <button
                    key={b.id}
                    onClick={() => setSelectedBudget(b.id)}
                    className={`flex items-start gap-4 rounded-2xl border p-4 text-left transition-all ${
                      isSelected
                        ? "border-cyan-500 bg-cyan-950/30 shadow-lg shadow-cyan-500/10"
                        : "border-slate-800 bg-slate-900/40 hover:border-slate-700 hover:bg-slate-900/80"
                    }`}
                  >
                    <div
                      className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border ${
                        isSelected
                          ? "border-cyan-400 bg-cyan-500 text-white"
                          : "border-slate-700 bg-slate-800"
                      }`}
                    >
                      {isSelected && <Check className="h-3.5 w-3.5" />}
                    </div>
                    <div>
                      <span className="block text-sm font-bold text-white">{b.label}</span>
                      <span className="block text-xs text-slate-400 mt-0.5">{b.subtext}</span>
                    </div>
                  </button>
                );
              })}
            </div>

            <div className="flex items-center justify-between pt-4">
              <button
                onClick={() => setStep(1)}
                className="text-xs font-semibold text-slate-400 hover:text-white"
              >
                ← Back
              </button>
              <button
                onClick={() => setStep(3)}
                className="flex items-center gap-2 rounded-xl bg-cyan-600 px-6 py-3 text-xs font-bold text-white hover:bg-cyan-500 transition-colors shadow-lg shadow-cyan-500/20"
              >
                <span>Continue to Priorities</span>
                <ChevronRight className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: PRIORITIES */}
        {step === 3 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            <div>
              <h3 className="text-lg font-bold text-white">Step 3: What attribute matters most to you?</h3>
              <p className="text-xs text-slate-400 mt-1">
                The recommendation engine dynamically reweights scoring parameters to favor your choice.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {PRIORITIES.map((p) => {
                const isSelected = selectedPriority === p.id;
                return (
                  <button
                    key={p.id}
                    onClick={() => setSelectedPriority(p.id)}
                    className={`flex items-start gap-4 rounded-2xl border p-4 text-left transition-all ${
                      isSelected
                        ? "border-cyan-500 bg-cyan-950/30 shadow-lg shadow-cyan-500/10"
                        : "border-slate-800 bg-slate-900/40 hover:border-slate-700 hover:bg-slate-900/80"
                    }`}
                  >
                    <div
                      className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border ${
                        isSelected
                          ? "border-cyan-400 bg-cyan-500 text-white"
                          : "border-slate-700 bg-slate-800"
                      }`}
                    >
                      {isSelected && <Check className="h-3.5 w-3.5" />}
                    </div>
                    <div>
                      <span className="block text-sm font-bold text-white">{p.label}</span>
                      <span className="block text-xs text-slate-400 mt-0.5">{p.subtext}</span>
                    </div>
                  </button>
                );
              })}
            </div>

            <div className="flex items-center justify-between pt-4">
              <button
                onClick={() => setStep(2)}
                className="text-xs font-semibold text-slate-400 hover:text-white"
              >
                ← Back
              </button>
              <button
                onClick={() => setStep(4)}
                className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-6 py-3 text-xs font-bold text-white hover:opacity-95 transition-opacity shadow-lg shadow-cyan-500/25"
              >
                <Sparkles className="h-4 w-4" />
                <span>Calculate My Matches</span>
              </button>
            </div>
          </div>
        )}

        {/* STEP 4: RECOMMENDATION RESULTS */}
        {step === 4 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-400">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
                  <Sparkles className="h-3.5 w-3.5" />
                  <span>Matches Calculated Successfully</span>
                </div>
                <h3 className="text-lg font-bold text-white mt-0.5">
                  Top Recommended Products for Your Profile
                </h3>
              </div>

              <button
                onClick={() => router.push(`/search?category_slug=${selectedCategory}&max_price=${selectedBudget}`)}
                className="text-xs font-semibold text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
              >
                <span>Browse All Matches in Catalog</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </button>
            </div>

            {isLoading ? (
              <div className="py-12 text-center space-y-3">
                <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-cyan-500 border-r-transparent"></div>
                <p className="text-xs text-slate-400">Synthesizing specifications and finding optimal deals...</p>
              </div>
            ) : recData?.recommendations && recData.recommendations.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {recData.recommendations.slice(0, 3).map((item) => (
                  <div key={item.product.id} className="flex flex-col">
                    <ProductCard product={item.product} />
                    <div className="mt-2 rounded-xl border border-cyan-500/20 bg-cyan-950/20 p-3 text-xs text-slate-300">
                      <span className="font-semibold text-cyan-400 block mb-1">
                        Why PriceWise Selected This:
                      </span>
                      <p className="line-clamp-2 text-[11px] leading-relaxed">{item.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-10 text-center text-xs text-slate-400">
                No exact match found within that budget threshold. Try selecting a slightly higher budget tier.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
