"use client";

import React, { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Sparkles,
  Search,
  Scale,
  Bookmark,
  Bell,
  Cpu,
  User,
  LogOut,
  Flame,
  Activity,
  X,
  ExternalLink,
} from "lucide-react";
import { useCompareStore } from "@/store/compareStore";
import { useAuthStore } from "@/store/authStore";
import { fetchAlertNotifications, dismissAlertNotification } from "@/lib/api";
import { formatINR } from "@/lib/utils";

export default function Navbar() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [query, setQuery] = useState("");
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const compareCount = useCompareStore((state) => state.selectedVariantIds.length);
  const { isAuthenticated, user, logout } = useAuthStore();

  const { data: notifications = [] } = useQuery({
    queryKey: ["alertNotifications"],
    queryFn: fetchAlertNotifications,
    enabled: isAuthenticated,
    refetchInterval: 30000,
  });

  const dismissMutation = useMutation({
    mutationFn: (alertId: string) => dismissAlertNotification(alertId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["alertNotifications"] });
    },
  });

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setNotificationsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/80 bg-background/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-cyan-400 p-2 shadow-lg shadow-blue-500/20 group-hover:shadow-blue-500/40 transition-all">
            <Cpu className="h-6 w-6 text-white" />
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight text-white group-hover:text-blue-400 transition-colors">
              Price<span className="text-cyan-400">Wise</span>
            </span>
            <span className="block text-[10px] font-medium tracking-wider text-slate-400 -mt-1 uppercase">
              Shopping Intelligence
            </span>
          </div>
        </Link>

        {/* Global Search Bar */}
        <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-md mx-6">
          <div className="relative w-full">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search smartphones, laptops, electronics..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full rounded-full border border-border bg-slate-900/60 py-2 pl-10 pr-4 text-sm text-white placeholder-slate-400 focus:border-blue-500 focus:bg-slate-900 focus:outline-none focus:ring-1 focus:ring-blue-500 transition-all"
            />
          </div>
        </form>

        {/* Main Navigation */}
        <nav className="flex items-center gap-1 sm:gap-2">
          <Link
            href="/search"
            className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 rounded-lg transition-colors"
          >
            <Search className="h-4 w-4 text-slate-400" />
            <span className="hidden sm:inline">Explore</span>
          </Link>

          <Link
            href="/deals"
            className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-amber-400 hover:text-amber-300 hover:bg-slate-800/60 rounded-lg transition-colors"
          >
            <Flame className="h-4 w-4" />
            <span className="hidden sm:inline">Deals</span>
          </Link>

          <Link
            href="/assistant"
            className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-cyan-400 hover:text-cyan-300 hover:bg-slate-800/60 rounded-lg transition-colors"
          >
            <Sparkles className="h-4 w-4 animate-pulse" />
            <span>AI Assistant</span>
          </Link>

          <Link
            href="/compare"
            className="relative flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-300 hover:text-white hover:bg-slate-800/60 rounded-lg transition-colors"
          >
            <Scale className="h-4 w-4 text-slate-400" />
            <span className="hidden sm:inline">Compare</span>
            {compareCount > 0 && (
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-blue-600 text-[11px] font-bold text-white">
                {compareCount}
              </span>
            )}
          </Link>

          <Link
            href="/providers"
            className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800/60 rounded-lg transition-colors"
            title="Marketplace Providers Health"
          >
            <Activity className="h-4 w-4" />
          </Link>

          {/* Price Drop Notifications Bell */}
          {isAuthenticated && (
            <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setNotificationsOpen(!notificationsOpen)}
                className="relative flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/60 transition-colors"
                title="Price Drop Notifications"
              >
                <Bell className="h-4 w-4" />
                {notifications.length > 0 && (
                  <span className="absolute top-1.5 right-1.5 flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                  </span>
                )}
              </button>

              {/* Notifications Dropdown Panel */}
              {notificationsOpen && (
                <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl border border-slate-800 bg-slate-900/95 p-4 shadow-2xl backdrop-blur-xl z-50 animate-in fade-in slide-in-from-top-2">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                    <div className="flex items-center gap-2">
                      <Bell className="h-4 w-4 text-cyan-400" />
                      <span className="text-sm font-bold text-white">Price Drop Alerts</span>
                      {notifications.length > 0 && (
                        <span className="rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20 px-2 py-0.5 text-[10px] font-bold">
                          {notifications.length} new
                        </span>
                      )}
                    </div>
                    <button
                      onClick={() => setNotificationsOpen(false)}
                      className="text-slate-500 hover:text-slate-300"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>

                  <div className="mt-3 max-h-72 overflow-y-auto space-y-2.5">
                    {notifications.length === 0 ? (
                      <div className="py-6 text-center text-xs text-slate-400">
                        No new price drop alerts triggered. You will be notified the instant any saved product drops to or below your target price.
                      </div>
                    ) : (
                      notifications.map((alert: any) => (
                        <div
                          key={alert.id}
                          className="flex items-start justify-between gap-3 rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-3"
                        >
                          <div className="space-y-1">
                            <span className="block text-xs font-semibold text-white line-clamp-1">
                              {alert.product_name}
                            </span>
                            <span className="block text-[11px] text-slate-400">
                              {alert.variant_name}
                            </span>
                            <div className="flex items-center gap-2 text-xs">
                              <span className="font-bold text-emerald-400">
                                Now {formatINR(alert.current_price)}
                              </span>
                              <span className="text-[10px] text-slate-500">
                                (Target: {formatINR(alert.target_price)})
                              </span>
                            </div>
                          </div>
                          <button
                            onClick={() => dismissMutation.mutate(alert.id)}
                            className="text-slate-500 hover:text-slate-300 p-1"
                            title="Dismiss"
                          >
                            <X className="h-3.5 w-3.5" />
                          </button>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Auth */}
          {isAuthenticated ? (
            <div className="flex items-center gap-2 pl-2 border-l border-slate-800">
              <Link
                href="/dashboard"
                className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
              >
                <Bookmark className="h-4 w-4 text-blue-400" />
                <span className="hidden sm:inline">Dashboard</span>
              </Link>
              <button
                onClick={logout}
                className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-800 rounded-lg transition-colors"
                title="Log out"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2 pl-2">
              <Link
                href="/login"
                className="px-3.5 py-1.5 text-sm font-medium text-slate-300 hover:text-white rounded-lg transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/register"
                className="px-3.5 py-1.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-500 rounded-lg transition-colors shadow-sm"
              >
                Sign Up
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}
