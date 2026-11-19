import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatINR(amount: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(amount);
}

export function getSafeMarketplaceUrl(
  rawUrl?: string,
  productName?: string,
  marketplaceName?: string
): string {
  if (!rawUrl) {
    const q = encodeURIComponent(productName || "electronics");
    return `https://www.amazon.in/s?k=${q}`;
  }

  // Preserve all direct, exact product links (Amazon /dp/, Flipkart /p/ or ?pid=)
  return rawUrl;
}
