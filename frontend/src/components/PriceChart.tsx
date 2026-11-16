"use client";

import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { PriceHistoryPoint } from "@/types";
import { formatINR } from "@/lib/utils";

interface PriceChartProps {
  data: PriceHistoryPoint[];
  lowestPrice?: number;
  highestPrice?: number;
  averagePrice?: number;
}

export default function PriceChart({
  data,
  lowestPrice,
  highestPrice,
  averagePrice,
}: PriceChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center rounded-xl border border-slate-800 bg-slate-900/30 text-sm text-slate-500">
        No price history recorded yet for this product.
      </div>
    );
  }

  // Format data for chart
  const chartData = data.map((d) => ({
    date: d.date,
    price: d.price,
    marketplace: d.marketplace,
  }));

  return (
    <div className="space-y-4">
      {/* Summary KPI Badges */}
      <div className="grid grid-cols-3 gap-3">
        <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-3">
          <span className="block text-[11px] font-medium text-emerald-400">Lowest Recorded</span>
          <span className="text-base font-bold text-white">
            {lowestPrice ? formatINR(lowestPrice) : "N/A"}
          </span>
        </div>
        <div className="rounded-xl border border-blue-500/20 bg-blue-500/5 p-3">
          <span className="block text-[11px] font-medium text-blue-400">Average Price</span>
          <span className="text-base font-bold text-white">
            {averagePrice ? formatINR(averagePrice) : "N/A"}
          </span>
        </div>
        <div className="rounded-xl border border-rose-500/20 bg-rose-500/5 p-3">
          <span className="block text-[11px] font-medium text-rose-400">Highest Recorded</span>
          <span className="text-base font-bold text-white">
            {highestPrice ? formatINR(highestPrice) : "N/A"}
          </span>
        </div>
      </div>

      {/* Chart Canvas */}
      <div className="h-64 w-full rounded-xl border border-slate-800 bg-slate-950/60 p-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 20, left: 20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis
              dataKey="date"
              stroke="#64748b"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: "#334155" }}
            />
            <YAxis
              stroke="#64748b"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: "#334155" }}
              tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
            />
            <Tooltip
              content={({ active, payload, label }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="rounded-lg border border-slate-700 bg-slate-900/95 p-3 shadow-xl backdrop-blur-md">
                      <p className="text-xs font-semibold text-slate-300">{label}</p>
                      <p className="text-sm font-bold text-cyan-400 mt-1">
                        {formatINR(Number(payload[0].value))}
                      </p>
                      <p className="text-[11px] text-slate-400">
                        {payload[0].payload.marketplace}
                      </p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#06b6d4"
              strokeWidth={3}
              dot={{ r: 4, fill: "#06b6d4", stroke: "#090d16", strokeWidth: 2 }}
              activeDot={{ r: 6, fill: "#38bdf8" }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
