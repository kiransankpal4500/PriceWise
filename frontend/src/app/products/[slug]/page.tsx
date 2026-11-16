"use client";

import React, { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import {
  Star,
  Scale,
  Bookmark,
  Bell,
  ExternalLink,
  ShieldCheck,
  Check,
  ArrowLeft,
  Sparkles,
  TrendingDown,
  Layers,
  Store,
  Info,
} from "lucide-react";
import { fetchProductDetail, fetchPriceHistory, createAlert, addToWatchlist } from "@/lib/api";
import { formatINR } from "@/lib/utils";
import { useCompareStore } from "@/store/compareStore";
import { useAuthStore } from "@/store/authStore";
import PriceChart from "@/components/PriceChart";

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const slug = params.slug as string;

  const { addVariant, hasVariant, removeVariant } = useCompareStore();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const [selectedVariantIndex, setSelectedVariantIndex] = useState(0);
  const [alertTargetPrice, setAlertTargetPrice] = useState<string>("");
  const [alertMessage, setAlertMessage] = useState<string | null>(null);
  const [isSaved, setIsSaved] = useState(false);

  const { data: product, isLoading, error } = useQuery({
    queryKey: ["product", slug],
    queryFn: () => fetchProductDetail(slug),
  });

  const currentVariant = product?.variants?.[selectedVariantIndex];
  const isCompared = currentVariant ? hasVariant(currentVariant.id) : false;

  const { data: priceHistoryData } = useQuery({
    queryKey: ["priceHistory", currentVariant?.id],
    queryFn: () => fetchPriceHistory(currentVariant!.id, 90),
    enabled: !!currentVariant?.id,
  });

  if (isLoading) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-16 text-center">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-500 border-r-transparent"></div>
        <p className="mt-4 text-sm text-slate-400">Loading verified product details...</p>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="mx-auto max-w-7xl px-4 py-16 text-center space-y-4">
        <h2 className="text-xl font-bold text-white">Product Not Found</h2>
        <p className="text-sm text-slate-400">The requested electronics product could not be located in our catalog.</p>
        <button
          onClick={() => router.push("/search")}
          className="rounded-xl bg-blue-600 px-5 py-2 text-xs font-semibold text-white"
        >
          Return to Catalog
        </button>
      </div>
    );
  }

  const handleToggleCompare = () => {
    if (!currentVariant) return;
    if (isCompared) {
      removeVariant(currentVariant.id);
    } else {
      addVariant(currentVariant.id);
    }
  };

  const handleSaveWatchlist = async () => {
    if (!currentVariant) return;
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    try {
      await addToWatchlist(currentVariant.id);
      setIsSaved(true);
    } catch {
      // ignore
    }
  };

  const handleCreateAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentVariant || !alertTargetPrice) return;
    if (!isAuthenticated) {
      router.push("/login");
      return;
    }
    try {
      await createAlert(currentVariant.id, parseFloat(alertTargetPrice));
      setAlertMessage(`Alert saved! We will notify you when price drops below ${formatINR(parseFloat(alertTargetPrice))}`);
      setAlertTargetPrice("");
    } catch (err: any) {
      setAlertMessage("Failed to set alert. Please check value.");
    }
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 space-y-12">
      {/* Back button */}
      <button
        onClick={() => router.back()}
        className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        <span>Back to results</span>
      </button>

      {/* Main Product Hero */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Left: Product Image */}
        <div className="flex flex-col items-center justify-center rounded-3xl border border-slate-800 bg-slate-900/40 p-8">
          <div className="relative h-80 sm:h-96 w-full flex items-center justify-center">
            {product.default_image_url ? (
              <img
                src={product.default_image_url}
                alt={product.name}
                className="max-h-full max-w-full object-contain"
              />
            ) : (
              <span className="text-slate-600">No image available</span>
            )}
          </div>
        </div>

        {/* Right: Product Details & Actions */}
        <div className="space-y-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-400">
              <span>{product.brand.name}</span>
              <span>•</span>
              <span>{product.category.name}</span>
              {product.model_number && (
                <>
                  <span>•</span>
                  <span className="text-slate-400">Model: {product.model_number}</span>
                </>
              )}
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              {product.name}
            </h1>

            <p className="text-sm text-slate-400 leading-relaxed">
              {product.description}
            </p>
          </div>

          {/* Variants Selector */}
          {product.variants && product.variants.length > 1 && (
            <div className="space-y-2 pt-2 border-t border-slate-800">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                Select Hardware Variant
              </label>
              <div className="flex flex-wrap gap-2">
                {product.variants.map((v, idx) => (
                  <button
                    key={v.id}
                    onClick={() => setSelectedVariantIndex(idx)}
                    className={`rounded-xl border px-3.5 py-2 text-xs font-medium transition-all ${
                      selectedVariantIndex === idx
                        ? "border-blue-500 bg-blue-500/10 text-blue-400 shadow-sm"
                        : "border-slate-800 bg-slate-900/60 text-slate-400 hover:border-slate-700 hover:text-white"
                    }`}
                  >
                    <span>{v.name}</span>
                    {v.best_price && (
                      <span className="ml-2 font-bold text-white">
                        {formatINR(v.best_price)}
                      </span>
                    )}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Best Current Offer */}
          <div className="rounded-2xl border border-blue-500/30 bg-gradient-to-r from-blue-950/40 to-slate-900/60 p-5 space-y-3">
            <div className="flex items-baseline justify-between">
              <div>
                <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                  Best Available Price
                </span>
                <div className="flex items-baseline gap-3 mt-1">
                  <span className="text-3xl font-extrabold text-white tracking-tight">
                    {currentVariant?.best_price ? formatINR(currentVariant.best_price) : "Checking..."}
                  </span>
                  {currentVariant?.mrp && (
                    <span className="text-sm text-slate-500 line-through">
                      {formatINR(currentVariant.mrp)}
                    </span>
                  )}
                </div>
              </div>

              {product.best_offer && (
                <div className="text-right">
                  <span className="block text-xs text-slate-400">Sold on</span>
                  <span className="text-sm font-bold text-white">
                    {product.best_offer.marketplace_name}
                  </span>
                </div>
              )}
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              {product.best_offer && (
                <a
                  href={product.best_offer.product_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-bold text-white hover:bg-blue-500 transition-colors shadow-lg shadow-blue-500/20"
                >
                  <span>Buy on {product.best_offer.marketplace_name}</span>
                  <ExternalLink className="h-4 w-4" />
                </a>
              )}

              <button
                onClick={handleToggleCompare}
                className={`flex items-center gap-1.5 rounded-xl border px-4 py-3 text-xs font-semibold transition-colors ${
                  isCompared
                    ? "bg-blue-600 border-blue-500 text-white"
                    : "border-slate-800 bg-slate-900 text-slate-300 hover:text-white hover:bg-slate-800"
                }`}
              >
                <Scale className="h-4 w-4" />
                <span>{isCompared ? "In Comparison" : "Compare"}</span>
              </button>

              <button
                onClick={handleSaveWatchlist}
                disabled={isSaved}
                className={`flex items-center gap-1.5 rounded-xl border px-4 py-3 text-xs font-semibold transition-colors ${
                  isSaved
                    ? "bg-emerald-600 border-emerald-500 text-white"
                    : "border-slate-800 bg-slate-900 text-slate-300 hover:text-white hover:bg-slate-800"
                }`}
              >
                {isSaved ? <Check className="h-4 w-4" /> : <Bookmark className="h-4 w-4" />}
                <span>{isSaved ? "Saved" : "Save"}</span>
              </button>
            </div>
          </div>

          {/* Quick Price Alert Form */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-4 space-y-3">
            <div className="flex items-center gap-2 text-xs font-bold text-white">
              <Bell className="h-4 w-4 text-cyan-400" />
              <span>Set Target Price Drop Alert</span>
            </div>
            <form onSubmit={handleCreateAlert} className="flex gap-2">
              <input
                type="number"
                placeholder="Target Price (₹)"
                value={alertTargetPrice}
                onChange={(e) => setAlertTargetPrice(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
              <button
                type="submit"
                className="rounded-xl bg-cyan-600 px-4 py-2 text-xs font-bold text-white hover:bg-cyan-500 transition-colors shrink-0"
              >
                Notify Me
              </button>
            </form>
            {alertMessage && (
              <p className="text-xs text-emerald-400 font-medium">{alertMessage}</p>
            )}
          </div>
        </div>
      </div>

      {/* 2. MARKETPLACE OFFERS TABLE */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <Store className="h-5 w-5 text-blue-400" />
          <h2 className="text-xl font-bold text-white">Marketplace Offers Comparison</h2>
        </div>

        <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900/40">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-800 bg-slate-950/60 text-xs font-semibold uppercase tracking-wider text-slate-400">
              <tr>
                <th className="px-6 py-4">Marketplace</th>
                <th className="px-6 py-4">Seller</th>
                <th className="px-6 py-4">Rating</th>
                <th className="px-6 py-4">Current Price</th>
                <th className="px-6 py-4">Availability</th>
                <th className="px-6 py-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80">
              {currentVariant?.listings?.map((l) => (
                <tr key={l.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4 font-semibold text-white">
                    {l.marketplace_name}
                  </td>
                  <td className="px-6 py-4 text-slate-400">{l.seller_name || "Verified Merchant"}</td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-1 text-xs">
                      <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
                      <span className="font-semibold text-slate-200">{l.rating?.toFixed(1) || "4.5"}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="font-bold text-white">{formatINR(l.current_price)}</span>
                    {l.original_mrp && l.original_mrp > l.current_price && (
                      <span className="ml-2 text-xs text-slate-500 line-through">
                        {formatINR(l.original_mrp)}
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <span className="inline-flex items-center rounded-full bg-emerald-500/10 px-2 py-0.5 text-xs font-medium text-emerald-400">
                      In Stock
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <a
                      href={l.product_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs font-bold text-blue-400 hover:text-blue-300"
                    >
                      <span>View Deal</span>
                      <ExternalLink className="h-3.5 w-3.5" />
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* 3. HISTORICAL PRICE TRENDS (RECHARTS) */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <TrendingDown className="h-5 w-5 text-cyan-400" />
          <h2 className="text-xl font-bold text-white">90-Day Price Observation History</h2>
        </div>

        <PriceChart
          data={priceHistoryData?.history || []}
          lowestPrice={priceHistoryData?.lowest_price}
          highestPrice={priceHistoryData?.highest_price}
          averagePrice={priceHistoryData?.average_price}
        />
      </section>

      {/* 4. SPECIFICATIONS MATRIX */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <Layers className="h-5 w-5 text-indigo-400" />
          <h2 className="text-xl font-bold text-white">Technical Specifications</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {currentVariant?.specifications?.map((spec, idx) => (
            <div
              key={idx}
              className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900/30 p-3.5 text-sm"
            >
              <span className="text-slate-400 font-medium">{spec.name}</span>
              <span className="font-semibold text-white text-right">{spec.value}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
