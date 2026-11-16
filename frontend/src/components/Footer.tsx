import React from "react";
import Link from "next/link";
import { Cpu, ShieldCheck, Zap, Scale, Heart } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-border bg-slate-950/80 text-slate-400">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white">
                <Cpu className="h-5 w-5" />
              </div>
              <span className="text-lg font-bold text-white">PriceWise</span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              India&apos;s intelligent electronics price comparison platform. Powered by Google Gemini AI,
              real-time market parsing, and deterministic specification scoring.
            </p>
            <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
              <ShieldCheck className="h-4 w-4" />
              <span>₹0 External API Policy & 100% Data Grounding</span>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-200">Categories</h3>
            <ul className="mt-4 space-y-2 text-sm">
              <li><Link href="/search?category=smartphones" className="hover:text-blue-400 transition-colors">Smartphones</Link></li>
              <li><Link href="/search?category=laptops" className="hover:text-blue-400 transition-colors">Laptops & Workstations</Link></li>
              <li><Link href="/search?category=headphones" className="hover:text-blue-400 transition-colors">Headphones & ANC</Link></li>
              <li><Link href="/search?category=smartwatches" className="hover:text-blue-400 transition-colors">Smartwatches</Link></li>
              <li><Link href="/search?category=televisions" className="hover:text-blue-400 transition-colors">4K OLED TVs</Link></li>
              <li><Link href="/search?category=computer-components" className="hover:text-blue-400 transition-colors">GPUs & Components</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-200">Intelligence</h3>
            <ul className="mt-4 space-y-2 text-sm">
              <li><Link href="/assistant" className="hover:text-cyan-400 transition-colors">AI Shopping Assistant</Link></li>
              <li><Link href="/compare" className="hover:text-blue-400 transition-colors">Side-by-Side Comparison</Link></li>
              <li><Link href="/deals" className="hover:text-amber-400 transition-colors">Price Drops & Top Deals</Link></li>
              <li><Link href="/providers" className="hover:text-blue-400 transition-colors">Marketplace Health Status</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-200">Platform Invariants</h3>
            <div className="mt-4 space-y-3 text-xs leading-relaxed text-slate-400">
              <p>• Prices tracked in Indian Rupees (₹) with append-only observation history.</p>
              <p>• Variant isolation: 128GB vs 256GB storage tiers are never merged.</p>
              <p>• Synthetic data is strictly labeled <span className="text-amber-400 font-semibold">DEMO DATA</span>.</p>
            </div>
          </div>
        </div>

        <div className="mt-8 border-t border-slate-900 pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© {new Date().getFullYear()} PriceWise India. Built for commercial-grade shopping intelligence.</p>
          <p className="flex items-center gap-1 mt-2 sm:mt-0">
            Engineered with <Heart className="h-3.5 w-3.5 text-rose-500 fill-rose-500" /> for Indian electronics buyers.
          </p>
        </div>
      </div>
    </footer>
  );
}
