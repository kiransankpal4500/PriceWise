"use client";

import React from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import {
  Scale,
  Sparkles,
  Trophy,
  AlertTriangle,
  X,
  ExternalLink,
  Plus,
  ArrowRight,
} from "lucide-react";
import { useCompareStore } from "@/store/compareStore";
import { compareVariants } from "@/lib/api";
import { formatINR } from "@/lib/utils";

export default function ComparePage() {
  const { selectedVariantIds, removeVariant, clear } = useCompareStore();

  const { data: compareData, isLoading, error } = useQuery({
    queryKey: ["compare", selectedVariantIds],
    queryFn: () => compareVariants(selectedVariantIds),
    enabled: selectedVariantIds.length >= 2,
  });

  if (selectedVariantIds.length < 2) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-20 text-center space-y-6">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-800 text-blue-400">
          <Scale className="h-8 w-8" />
        </div>
        <h1 className="text-3xl font-extrabold text-white">Compare Products</h1>
        <p className="text-sm text-slate-400 max-w-md mx-auto">
          Select at least 2 products (up to 4) to generate a side-by-side specification breakdown,
          price difference evaluation, and algorithmic value verdict.
        </p>
        <Link
          href="/search"
          className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-6 py-3 text-sm font-bold text-white hover:bg-blue-500 transition-colors"
        >
          <span>Explore Catalog & Add Products</span>
          <ArrowRight className="h-4 w-4" />
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">
            Side-by-Side Product Comparison
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Comparing {selectedVariantIds.length} electronics devices with aligned hardware attributes.
          </p>
        </div>

        <button
          onClick={clear}
          className="rounded-xl border border-slate-800 bg-slate-900 px-4 py-2 text-xs font-semibold text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        >
          Clear Comparison
        </button>
      </div>

      {isLoading && (
        <div className="py-12 text-center text-sm text-slate-400">
          Evaluating technical specifications and compiling matrix...
        </div>
      )}

      {compareData && (
        <div className="space-y-10">
          {/* Winner Banner */}
          {compareData.winner_rationale && (
            <div className="rounded-2xl border border-cyan-500/30 bg-gradient-to-r from-blue-950/60 to-slate-900 p-6 space-y-2">
              <div className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-cyan-400">
                <Trophy className="h-4 w-4" />
                <span>Deterministic Value Recommendation</span>
              </div>
              <p className="text-sm sm:text-base text-slate-200 leading-relaxed">
                {compareData.winner_rationale}
              </p>
            </div>
          )}

          {/* Product Header Cards Row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {compareData.products.map((prod) => (
              <div
                key={prod.variant_id}
                className={`relative flex flex-col justify-between rounded-2xl border p-4 transition-all ${
                  compareData.winner_variant_id === prod.variant_id
                    ? "border-cyan-500/50 bg-slate-900/90 shadow-lg shadow-cyan-500/10"
                    : "border-slate-800 bg-slate-900/40"
                }`}
              >
                <button
                  onClick={() => removeVariant(prod.variant_id)}
                  className="absolute top-2 right-2 flex h-6 w-6 items-center justify-center rounded-full bg-slate-800 text-slate-400 hover:text-white"
                  title="Remove"
                >
                  <X className="h-3.5 w-3.5" />
                </button>

                <div className="space-y-3">
                  <div className="h-32 w-full rounded-xl bg-slate-950 flex items-center justify-center p-2">
                    {prod.image_url ? (
                      <img src={prod.image_url} alt={prod.product_name} className="h-full object-contain" />
                    ) : (
                      <span className="text-xs text-slate-600">No Image</span>
                    )}
                  </div>

                  <div>
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-blue-400">
                      {prod.brand_name}
                    </span>
                    <h3 className="text-xs font-bold text-white line-clamp-2 mt-0.5">
                      {prod.product_name}
                    </h3>
                    <p className="text-[11px] text-slate-400">{prod.variant_name}</p>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2">
                  <div className="flex items-baseline justify-between">
                    <span className="text-base font-extrabold text-white">
                      {formatINR(prod.best_price)}
                    </span>
                    <span className="text-[11px] text-slate-500 line-through">
                      {formatINR(prod.mrp)}
                    </span>
                  </div>

                  {compareData.compromises[prod.variant_id]?.length > 0 && (
                    <div className="text-[11px] text-amber-400 flex items-center gap-1">
                      <AlertTriangle className="h-3 w-3 shrink-0" />
                      <span className="line-clamp-1">{compareData.compromises[prod.variant_id][0]}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Side-by-Side Technical Comparison Table */}
          <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900/40">
            <table className="w-full text-left text-xs">
              <tbody className="divide-y divide-slate-800/80">
                {compareData.all_spec_groups.map((group) => (
                  <React.Fragment key={group}>
                    <tr className="bg-slate-950/80">
                      <td
                        colSpan={compareData.products.length + 1}
                        className="px-6 py-2.5 font-bold uppercase tracking-wider text-cyan-400"
                      >
                        {group}
                      </td>
                    </tr>
                    {Object.entries(compareData.specs_matrix[group] || {}).map(([specName, values]) => (
                      <tr key={specName} className="hover:bg-slate-800/20 transition-colors">
                        <td className="px-6 py-3 font-medium text-slate-400 w-1/4">
                          {specName}
                        </td>
                        {values.map((val, idx) => (
                          <td key={idx} className="px-6 py-3 font-semibold text-slate-200">
                            {val || "—"}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
