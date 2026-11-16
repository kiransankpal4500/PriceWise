"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Activity,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ShieldCheck,
  Server,
  RefreshCw,
} from "lucide-react";
import { fetchProviderHealth } from "@/lib/api";

export default function ProvidersPage() {
  const { data, isLoading, refetch, isFetching } = useQuery({
    queryKey: ["providerHealth"],
    queryFn: fetchProviderHealth,
    refetchInterval: 15000,
  });

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-800">
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-blue-400 mb-1">
            <Activity className="h-4 w-4" />
            <span>Marketplace Integrations</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">Provider Monitoring Dashboard</h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time status, rate limit cooldowns, and error telemetry for external marketplace adapters.
          </p>
        </div>

        <button
          onClick={() => refetch()}
          disabled={isFetching}
          className="flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-900 px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${isFetching ? "animate-spin" : ""}`} />
          <span>Refresh Status</span>
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-sm text-slate-400">Checking adapter telemetry...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {data?.providers?.map((p: any) => {
            const isAvail = p.status === "AVAILABLE";
            const isRate = p.status === "RATE_LIMITED";
            return (
              <div
                key={p.slug}
                className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 space-y-4"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Server className="h-5 w-5 text-blue-400" />
                    <h3 className="text-base font-bold text-white">{p.name}</h3>
                  </div>
                  <span
                    className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold border ${
                      isAvail
                        ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                        : isRate
                        ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                        : "bg-red-500/10 text-red-400 border-red-500/20"
                    }`}
                  >
                    {isAvail ? (
                      <CheckCircle2 className="h-3.5 w-3.5" />
                    ) : (
                      <AlertTriangle className="h-3.5 w-3.5" />
                    )}
                    <span>{p.status}</span>
                  </span>
                </div>

                <div className="space-y-2 text-xs text-slate-400 pt-2 border-t border-slate-800/80">
                  <div className="flex justify-between">
                    <span>Classification:</span>
                    <strong className="text-slate-200">
                      {p.is_demo ? "Synthetic Demo Data" : "Live Marketplace Scraper"}
                    </strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Capabilities:</span>
                    <span className="text-slate-300 capitalize">{p.capabilities.join(", ")}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Last Successful Request:</span>
                    <span className="text-slate-300">
                      {p.last_successful_request
                        ? new Date(p.last_successful_request).toLocaleTimeString()
                        : "Ready"}
                    </span>
                  </div>
                </div>

                {p.last_error && (
                  <div className="rounded-xl border border-slate-800 bg-slate-950 p-3 text-[11px] text-slate-400">
                    <span className="block font-semibold text-red-400">Telemetry Info:</span>
                    <p className="mt-0.5 truncate">{p.last_error}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Compliance Information */}
      <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-6 space-y-3">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
          <ShieldCheck className="h-4 w-4" />
          <span>Operational Compliance & Resilience Guarantees</span>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          PriceWise respects marketplace availability. In accordance with ethical scraping standards and platform guidelines,
          PriceWise does not execute anti-bot bypasses or CAPTCHA solvers. When an external provider responds with rate-limits,
          the adapter automatically enters a timed cooldown while search falls back transparently to canonical and demo databases.
        </p>
      </div>
    </div>
  );
}
