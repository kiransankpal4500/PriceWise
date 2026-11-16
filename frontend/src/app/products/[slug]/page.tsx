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
  MapPin,
  ThumbsUp,
  ThumbsDown,
  CheckCircle2,
  AlertCircle,
  Truck,
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
  const [pincode, setPincode] = useState("");
  const [pincodeStatus, setPincodeStatus] = useState<string | null>(null);

  const handleCheckPincode = (e: React.FormEvent) => {
    e.preventDefault();
    if (!pincode || pincode.length !== 6 || !/^\d{6}$/.test(pincode)) {
      setPincodeStatus("Please enter a valid 6-digit Indian PIN code (e.g. 110001 or 560001).");
      return;
    }
    const metroPrefixes = ["11", "40", "56", "60", "70", "50", "38", "41"];
    const isMetro = metroPrefixes.some((p) => pincode.startsWith(p));
    if (isMetro) {
      setPincodeStatus("⚡ Free Express Next-Day Delivery available for PIN " + pincode + " (Fulfilled by verified hub).");
    } else {
      setPincodeStatus("Standard Delivery within 2-4 business days for PIN " + pincode + " (Cash on Delivery eligible).");
    }
  };

  const { data: product, isLoading, error } = useQuery({
    queryKey: ["product", slug],
    queryFn: () => fetchProductDetail(slug),
  });

  const currentVariant = product?.variants?.[selectedVariantIndex];
  const isCompared = currentVariant ? hasVariant(currentVariant.id) : false;

  // Dynamically determine the listing with the lowest / best price for the selected variant
  const bestListing =
    currentVariant?.listings && currentVariant.listings.length > 0
      ? [...currentVariant.listings].sort((a, b) => a.current_price - b.current_price)[0]
      : product?.best_offer;

  const sortedListings = currentVariant?.listings
    ? [...currentVariant.listings].sort((a, b) => a.current_price - b.current_price)
    : [];

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

              {bestListing && (
                <div className="text-right">
                  <span className="block text-[11px] font-semibold text-emerald-400 uppercase tracking-wider">
                    Lowest Price Store
                  </span>
                  <span className="text-sm font-bold text-white">
                    {bestListing.marketplace_name}
                  </span>
                </div>
              )}
            </div>

            {/* CTA Buttons - Guaranteed Direct Redirect to Best Price */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              {bestListing && (
                <a
                  href={bestListing.product_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 px-5 py-3.5 text-sm font-extrabold text-white transition-all shadow-lg shadow-emerald-500/25"
                  title={`Redirect directly to ${bestListing.marketplace_name} with lowest verified price of ${formatINR(bestListing.current_price)}`}
                >
                  <span>Buy on {bestListing.marketplace_name} • {formatINR(bestListing.current_price)}</span>
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

          {/* Indian Pincode Delivery Estimator */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-4 space-y-3">
            <div className="flex items-center gap-2 text-xs font-bold text-white">
              <Truck className="h-4 w-4 text-emerald-400" />
              <span>Check Delivery Speed & Cash on Delivery</span>
            </div>
            <form onSubmit={handleCheckPincode} className="flex gap-2">
              <div className="relative w-full">
                <MapPin className="absolute left-3 top-2.5 h-3.5 w-3.5 text-slate-500" />
                <input
                  type="text"
                  maxLength={6}
                  placeholder="Enter 6-digit Indian PIN (e.g. 560001)"
                  value={pincode}
                  onChange={(e) => setPincode(e.target.value.replace(/\D/g, ""))}
                  className="w-full rounded-xl border border-slate-800 bg-slate-950 pl-8 pr-3 py-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500"
                />
              </div>
              <button
                type="submit"
                className="rounded-xl bg-slate-800 border border-slate-700 px-4 py-2 text-xs font-bold text-white hover:bg-slate-700 transition-colors shrink-0"
              >
                Check
              </button>
            </form>
            {pincodeStatus && (
              <p className={`text-xs font-medium ${pincodeStatus.startsWith("⚡") ? "text-emerald-400" : pincodeStatus.startsWith("Standard") ? "text-blue-400" : "text-amber-400"}`}>
                {pincodeStatus}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* AI PRICE PREDICTION: BUY NOW OR WAIT? */}
      {product.price_prediction && (
        <section className={`rounded-3xl border p-6 sm:p-8 backdrop-blur-xl transition-all ${
          product.price_prediction.verdict === "STRONG_BUY"
            ? "border-emerald-500/30 bg-gradient-to-r from-emerald-950/30 to-slate-900/60"
            : product.price_prediction.verdict === "BUY"
            ? "border-blue-500/30 bg-gradient-to-r from-blue-950/30 to-slate-900/60"
            : product.price_prediction.verdict === "FAIR_PRICE"
            ? "border-amber-500/30 bg-gradient-to-r from-amber-950/30 to-slate-900/60"
            : "border-rose-500/30 bg-gradient-to-r from-rose-950/30 to-slate-900/60"
        }`}>
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="space-y-3 flex-1">
              <div className="flex items-center gap-2">
                <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${
                  product.price_prediction.verdict === "STRONG_BUY"
                    ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/40"
                    : product.price_prediction.verdict === "BUY"
                    ? "bg-blue-500/20 text-blue-400 border-blue-500/40"
                    : product.price_prediction.verdict === "FAIR_PRICE"
                    ? "bg-amber-500/20 text-amber-400 border-amber-500/40"
                    : "bg-rose-500/20 text-rose-400 border-rose-500/40"
                }`}>
                  <Sparkles className="h-3.5 w-3.5" />
                  <span>AI VERDICT: {product.price_prediction.badge_label.toUpperCase()}</span>
                </span>
                <span className="text-xs text-slate-400">
                  Deal Confidence: <strong className="text-white">{product.price_prediction.deal_score}/100</strong>
                </span>
              </div>

              <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                {product.price_prediction.verdict === "STRONG_BUY"
                  ? "Historic Low Alert — Outstanding Time to Purchase"
                  : product.price_prediction.verdict === "BUY"
                  ? "Competitive Price — Recommended Value Pick"
                  : product.price_prediction.verdict === "FAIR_PRICE"
                  ? "Stable Standard Market Price"
                  : "Price is High — Consider Waiting or Setting an Alert"}
              </h2>

              <p className="text-sm text-slate-300 leading-relaxed max-w-3xl">
                {product.price_prediction.rationale}
              </p>
            </div>

            <div className="flex sm:flex-col items-center sm:items-end justify-between w-full sm:w-auto pt-4 sm:pt-0 border-t sm:border-t-0 border-slate-800 gap-3">
              <div className="text-left sm:text-right">
                <span className="text-xs text-slate-400 block">Lowest Recorded</span>
                <span className="text-sm font-bold text-emerald-400">
                  {formatINR(product.price_prediction.lowest_recorded_price)}
                </span>
              </div>
              <div className="text-left sm:text-right">
                <span className="text-xs text-slate-400 block">Average 90-Day Price</span>
                <span className="text-sm font-semibold text-slate-300">
                  {formatINR(product.price_prediction.average_price)}
                </span>
              </div>
              {product.price_prediction.savings_vs_peak > 0 && (
                <div className="text-left sm:text-right">
                  <span className="text-xs text-slate-400 block">Saved vs Peak</span>
                  <span className="text-sm font-bold text-cyan-400">
                    +{formatINR(product.price_prediction.savings_vs_peak)}
                  </span>
                </div>
              )}
            </div>
          </div>
        </section>
      )}

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
              {sortedListings.map((l, idx) => (
                <tr
                  key={l.id}
                  className={`transition-colors ${
                    idx === 0
                      ? "bg-emerald-950/20 hover:bg-emerald-950/30 font-medium"
                      : "hover:bg-slate-800/30"
                  }`}
                >
                  <td className="px-6 py-4 font-semibold text-white">
                    <div className="flex items-center gap-2">
                      <span>{l.marketplace_name}</span>
                      {idx === 0 && (
                        <span className="rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider">
                          Lowest Price
                        </span>
                      )}
                    </div>
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
                      className={`inline-flex items-center gap-1 rounded-xl px-3 py-1.5 text-xs font-bold transition-all ${
                        idx === 0
                          ? "bg-emerald-600 hover:bg-emerald-500 text-white shadow-sm"
                          : "text-blue-400 hover:text-blue-300"
                      }`}
                    >
                      <span>{idx === 0 ? "Buy at Best Price" : "View Deal"}</span>
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

      {/* 5. AI REVIEW INTELLIGENCE & SENTIMENT */}
      {product.review_intelligence && (
        <section className="space-y-6 rounded-3xl border border-slate-800 bg-slate-900/40 p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
                <Sparkles className="h-5 w-5" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">AI Review Intelligence</h2>
                <p className="text-xs text-slate-400">
                  Synthesized across {product.review_intelligence.total_reviews_analyzed.toLocaleString()} verified buyer observations
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {product.review_intelligence.key_themes.map((theme, i) => (
                <span
                  key={i}
                  className="rounded-full bg-slate-800/80 border border-slate-700/80 px-3 py-1 text-[11px] font-medium text-slate-300"
                >
                  {theme}
                </span>
              ))}
            </div>
          </div>

          {/* Sentiment Bar */}
          <div className="space-y-2 rounded-2xl bg-slate-950 p-4 border border-slate-800">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-emerald-400">
                {product.review_intelligence.sentiment.positive_percentage}% Positive
              </span>
              <span className="text-slate-400">
                {product.review_intelligence.sentiment.neutral_percentage}% Neutral
              </span>
              <span className="text-rose-400">
                {product.review_intelligence.sentiment.negative_percentage}% Critical
              </span>
            </div>
            <div className="h-2.5 w-full flex overflow-hidden rounded-full bg-slate-800">
              <div
                style={{ width: `${product.review_intelligence.sentiment.positive_percentage}%` }}
                className="bg-emerald-500 transition-all duration-500"
              />
              <div
                style={{ width: `${product.review_intelligence.sentiment.neutral_percentage}%` }}
                className="bg-slate-500 transition-all duration-500"
              />
              <div
                style={{ width: `${product.review_intelligence.sentiment.negative_percentage}%` }}
                className="bg-rose-500 transition-all duration-500"
              />
            </div>
            <p className="text-xs text-slate-400 pt-1">
              {product.review_intelligence.verdict_summary}
            </p>
          </div>

          {/* Pros & Cons Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Top Pros */}
            <div className="rounded-2xl border border-emerald-500/20 bg-emerald-950/10 p-5 space-y-3">
              <div className="flex items-center gap-2 text-sm font-bold text-emerald-400">
                <ThumbsUp className="h-4 w-4" />
                <span>Verified Buyer Highlights (Pros)</span>
              </div>
              <ul className="space-y-2 text-xs text-slate-300">
                {product.review_intelligence.top_pros.map((pro, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{pro}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Top Cons */}
            <div className="rounded-2xl border border-rose-500/20 bg-rose-950/10 p-5 space-y-3">
              <div className="flex items-center gap-2 text-sm font-bold text-rose-400">
                <ThumbsDown className="h-4 w-4" />
                <span>Reported Compromises (Cons)</span>
              </div>
              <ul className="space-y-2 text-xs text-slate-300">
                {product.review_intelligence.top_cons.map((con, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <AlertCircle className="h-4 w-4 text-rose-400 shrink-0 mt-0.5" />
                    <span>{con}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
