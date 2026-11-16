"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Bookmark,
  Bell,
  Sliders,
  Trash2,
  ExternalLink,
  ShieldCheck,
  AlertCircle,
  CheckCircle2,
} from "lucide-react";
import { useAuthStore } from "@/store/authStore";
import { fetchWatchlist, removeFromWatchlist, fetchAlerts } from "@/lib/api";
import { formatINR } from "@/lib/utils";
import ProductCard from "@/components/ProductCard";

export default function DashboardPage() {
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState<"watchlist" | "alerts" | "preferences">("watchlist");

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, router]);

  const { data: watchlist = [], isLoading: loadingWatchlist } = useQuery({
    queryKey: ["watchlist"],
    queryFn: fetchWatchlist,
    enabled: isAuthenticated,
  });

  const { data: alerts = [], isLoading: loadingAlerts } = useQuery({
    queryKey: ["alerts"],
    queryFn: fetchAlerts,
    enabled: isAuthenticated,
  });

  const removeMutation = useMutation({
    mutationFn: removeFromWatchlist,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["watchlist"] });
    },
  });

  if (!isAuthenticated) return null;

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-extrabold text-white">User Dashboard</h1>
          <p className="text-sm text-slate-400 mt-1">
            Logged in as <strong className="text-white">{user?.email}</strong>
          </p>
        </div>

        {/* Tab Controls */}
        <div className="flex rounded-xl border border-slate-800 bg-slate-900 p-1 text-xs font-semibold">
          <button
            onClick={() => setActiveTab("watchlist")}
            className={`flex items-center gap-1.5 rounded-lg px-4 py-2 transition-colors ${
              activeTab === "watchlist"
                ? "bg-blue-600 text-white shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Bookmark className="h-4 w-4" />
            <span>Watchlist ({watchlist.length})</span>
          </button>
          <button
            onClick={() => setActiveTab("alerts")}
            className={`flex items-center gap-1.5 rounded-lg px-4 py-2 transition-colors ${
              activeTab === "alerts"
                ? "bg-blue-600 text-white shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Bell className="h-4 w-4" />
            <span>Price Alerts ({alerts.length})</span>
          </button>
        </div>
      </div>

      {/* Tab: Watchlist */}
      {activeTab === "watchlist" && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">Your Saved Products</h2>
          {loadingWatchlist ? (
            <div className="text-sm text-slate-400">Loading your saved devices...</div>
          ) : watchlist.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {watchlist.map((p) => (
                <div key={p.id} className="relative group">
                  <ProductCard product={p} />
                  <button
                    onClick={() => removeMutation.mutate(p.primary_variant_id)}
                    className="absolute bottom-4 right-4 z-20 rounded-lg bg-red-600/80 hover:bg-red-600 p-1.5 text-white transition-colors"
                    title="Remove from saved"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-12 text-center text-sm text-slate-400 space-y-3">
              <p>You haven&apos;t saved any products to your watchlist yet.</p>
              <button
                onClick={() => router.push("/search")}
                className="rounded-xl bg-blue-600 px-4 py-2 text-xs font-semibold text-white"
              >
                Browse Electronics
              </button>
            </div>
          )}
        </div>
      )}

      {/* Tab: Alerts */}
      {activeTab === "alerts" && (
        <div className="space-y-6">
          <h2 className="text-xl font-bold text-white">Active Price Drop Alerts</h2>
          {loadingAlerts ? (
            <div className="text-sm text-slate-400">Loading price monitors...</div>
          ) : alerts.length > 0 ? (
            <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900/40">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-slate-800 bg-slate-950/60 text-xs font-semibold uppercase tracking-wider text-slate-400">
                  <tr>
                    <th className="px-6 py-4">Product</th>
                    <th className="px-6 py-4">Current Price</th>
                    <th className="px-6 py-4">Target Alert Price</th>
                    <th className="px-6 py-4">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80">
                  {alerts.map((alt) => (
                    <tr key={alt.id} className="hover:bg-slate-800/30 transition-colors">
                      <td className="px-6 py-4 font-semibold text-white">
                        {alt.product_name} ({alt.variant_name})
                      </td>
                      <td className="px-6 py-4 font-bold text-white">
                        {formatINR(alt.current_price)}
                      </td>
                      <td className="px-6 py-4 font-bold text-cyan-400">
                        {formatINR(alt.target_price)}
                      </td>
                      <td className="px-6 py-4">
                        {alt.is_triggered ? (
                          <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-semibold text-emerald-400 border border-emerald-500/20">
                            <CheckCircle2 className="h-3.5 w-3.5" />
                            Triggered (Target Reached)
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 rounded-full bg-blue-500/10 px-2.5 py-0.5 text-xs font-semibold text-blue-400 border border-blue-500/20">
                            Active Monitor
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-12 text-center text-sm text-slate-400">
              No price alerts set. Open any product page and click &ldquo;Set Target Price Drop Alert&rdquo;.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
