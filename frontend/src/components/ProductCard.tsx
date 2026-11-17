"use client";

import React, { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Star, Scale, Bookmark, Check, ShieldAlert, ExternalLink } from "lucide-react";
import { ProductSummary } from "@/types";
import { formatINR, getSafeMarketplaceUrl } from "@/lib/utils";
import { useCompareStore } from "@/store/compareStore";
import { useAuthStore } from "@/store/authStore";
import { addToWatchlist } from "@/lib/api";

interface ProductCardProps {
  product: ProductSummary;
}

export default function ProductCard({ product }: ProductCardProps) {
  const { hasVariant, addVariant, removeVariant } = useCompareStore();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const isCompared = hasVariant(product.primary_variant_id);

  const [isSaved, setIsSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleToggleCompare = (e: React.MouseEvent) => {
    e.preventDefault();
    if (isCompared) {
      removeVariant(product.primary_variant_id);
    } else {
      addVariant(product.primary_variant_id);
    }
  };

  const handleSaveWatchlist = async (e: React.MouseEvent) => {
    e.preventDefault();
    if (!isAuthenticated) {
      window.location.href = "/login";
      return;
    }
    try {
      setSaving(true);
      await addToWatchlist(product.primary_variant_id);
      setIsSaved(true);
    } catch {
      // already saved or failed
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="group relative flex flex-col overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/40 p-4 transition-all duration-300 hover:border-slate-700 hover:bg-slate-900/80 hover:shadow-xl hover:shadow-blue-500/5">
      {/* Demo Badge */}
      {product.is_demo && (
        <div className="absolute top-3 left-3 z-10 flex items-center gap-1 rounded-full bg-amber-500/10 px-2.5 py-1 text-[11px] font-semibold text-amber-400 border border-amber-500/20 backdrop-blur-md">
          <ShieldAlert className="h-3 w-3" />
          <span>DEMO DATA</span>
        </div>
      )}

      {/* Discount Badge */}
      {product.discount_percentage && product.discount_percentage > 0 && !product.is_demo ? (
        <div className="absolute top-3 left-3 z-10 rounded-full bg-emerald-500/10 px-2.5 py-1 text-[11px] font-semibold text-emerald-400 border border-emerald-500/20 backdrop-blur-md">
          {Math.round(product.discount_percentage)}% OFF
        </div>
      ) : null}

      {/* Compare & Watchlist Quick Actions */}
      <div className="absolute top-3 right-3 z-10 flex items-center gap-1.5 opacity-90 sm:opacity-0 group-hover:opacity-100 transition-opacity">
        <button
          onClick={handleToggleCompare}
          title={isCompared ? "Remove from comparison" : "Add to comparison"}
          className={`flex h-8 w-8 items-center justify-center rounded-full border backdrop-blur-md transition-colors ${
            isCompared
              ? "bg-blue-600 border-blue-500 text-white"
              : "bg-slate-800/80 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700"
          }`}
        >
          <Scale className="h-4 w-4" />
        </button>

        <button
          onClick={handleSaveWatchlist}
          disabled={saving || isSaved}
          title={isSaved ? "Saved to watchlist" : "Save product"}
          className={`flex h-8 w-8 items-center justify-center rounded-full border backdrop-blur-md transition-colors ${
            isSaved
              ? "bg-emerald-600 border-emerald-500 text-white"
              : "bg-slate-800/80 border-slate-700 text-slate-300 hover:text-white hover:bg-slate-700"
          }`}
        >
          {isSaved ? <Check className="h-4 w-4" /> : <Bookmark className="h-4 w-4" />}
        </button>
      </div>

      {/* Product Image */}
      <Link href={`/products/${product.slug}`} className="relative h-48 w-full overflow-hidden rounded-xl bg-slate-950 flex items-center justify-center p-4">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="h-full w-full object-contain object-center transition-transform duration-300 group-hover:scale-105"
          />
        ) : (
          <div className="text-slate-600 text-xs">No Image Available</div>
        )}
      </Link>

      {/* Meta & Title */}
      <div className="mt-4 flex flex-1 flex-col">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span className="font-medium text-blue-400">{product.brand_name}</span>
          <span className="capitalize">{product.category_name}</span>
        </div>

        <Link href={`/products/${product.slug}`} className="mt-1 flex-1">
          <h3 className="text-sm font-semibold text-white line-clamp-2 group-hover:text-blue-400 transition-colors">
            {product.name}
          </h3>
        </Link>

        {/* Rating & Marketplace count */}
        <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-1">
            <Star className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
            <span className="font-medium text-slate-200">{product.rating ? product.rating.toFixed(1) : "4.5"}</span>
            {product.review_count ? (
              <span className="text-slate-500">({product.review_count.toLocaleString()})</span>
            ) : null}
          </div>
          <span className="text-[11px] text-slate-400">
            {product.marketplace_count} {product.marketplace_count === 1 ? "store" : "stores"}
          </span>
        </div>

        {/* AI Deal Prediction Badge */}
        {product.price_prediction && (
          <div className="mt-2 flex items-center">
            <span
              className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-semibold border ${
                product.price_prediction.verdict === "STRONG_BUY"
                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                  : product.price_prediction.verdict === "BUY"
                  ? "bg-blue-500/10 text-blue-400 border-blue-500/30"
                  : product.price_prediction.verdict === "FAIR_PRICE"
                  ? "bg-amber-500/10 text-amber-400 border-amber-500/30"
                  : "bg-rose-500/10 text-rose-400 border-rose-500/30"
              }`}
            >
              <span
                className={`h-1.5 w-1.5 rounded-full ${
                  product.price_prediction.verdict === "STRONG_BUY"
                    ? "bg-emerald-400 animate-pulse"
                    : product.price_prediction.verdict === "BUY"
                    ? "bg-blue-400"
                    : product.price_prediction.verdict === "FAIR_PRICE"
                    ? "bg-amber-400"
                    : "bg-rose-400"
                }`}
              />
              {product.price_prediction.badge_label} • {product.price_prediction.deal_score}/100
            </span>
          </div>
        )}

        {/* Pricing & Direct Best Price Redirect */}
        <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2.5">
          <div className="flex items-baseline justify-between">
            <div>
              <span className="text-lg font-bold text-white tracking-tight">
                {formatINR(product.best_price)}
              </span>
              {product.mrp && product.mrp > product.best_price && (
                <span className="ml-2 text-xs text-slate-500 line-through">
                  {formatINR(product.mrp)}
                </span>
              )}
            </div>
            {product.best_offer_marketplace && (
              <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded-md">
                Best on {product.best_offer_marketplace}
              </span>
            )}
          </div>

          <div className="flex items-center gap-2 pt-1">
            <a
              href={getSafeMarketplaceUrl(product.best_offer_url, product.name, product.best_offer_marketplace)}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 flex items-center justify-center gap-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 px-3 py-2 text-xs font-bold text-white transition-all shadow-md shadow-blue-500/20"
              title={`Redirect to ${product.best_offer_marketplace || 'store'} with lowest price`}
            >
              <span>Buy at Best Price</span>
              <ExternalLink className="h-3 w-3" />
            </a>

            <Link
              href={`/products/${product.slug}`}
              className="flex items-center justify-center rounded-xl border border-slate-800 bg-slate-900/80 hover:bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-300 hover:text-white transition-colors"
              title="Compare all marketplace offers and technical specs"
            >
              Details
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
