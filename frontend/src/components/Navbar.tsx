"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
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
} from "lucide-react";
import { useCompareStore } from "@/store/compareStore";
import { useAuthStore } from "@/store/authStore";

export default function Navbar() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const compareCount = useCompareStore((state) => state.selectedVariantIds.length);
  const { isAuthenticated, user, logout } = useAuthStore();

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
