import {
  Category,
  ProductSummary,
  ProductDetail,
  SearchResponse,
  CompareResponse,
  RecommendationResponse,
  PriceHistoryResponse,
  ChatResponse,
} from "@/types";

function getApiBaseUrl(): string {
  const backendUrl =
    process.env.NEXT_PUBLIC_BACKEND_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    process.env.BACKEND_URL;

  if (backendUrl) {
    const clean = backendUrl.trim().replace(/\/+$/, "");
    return clean.endsWith("/api/v1") ? clean : `${clean}/api/v1`;
  }

  if (typeof window !== "undefined") {
    return `${window.location.origin}/api/v1`;
  }

  return "http://127.0.0.1:8000/api/v1";
}

function getAuthHeader(): Record<string, string> {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("pricewise_token");
    if (token) {
      return { Authorization: `Bearer ${token}` };
    }
  }
  return {};
}

export async function fetchCategories(): Promise<Category[]> {
  const res = await fetch(`${getApiBaseUrl()}/categories`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch categories");
  return res.json();
}

export async function fetchProducts(params?: {
  category_slug?: string;
  brand_slug?: string;
  min_price?: number;
  max_price?: number;
  sort_by?: string;
  page?: number;
  page_size?: number;
}): Promise<ProductSummary[]> {
  const url = new URL(`${getApiBaseUrl()}/products`);
  if (params?.category_slug) url.searchParams.set("category_slug", params.category_slug);
  if (params?.brand_slug) url.searchParams.set("brand_slug", params.brand_slug);
  if (params?.min_price) url.searchParams.set("min_price", params.min_price.toString());
  if (params?.max_price) url.searchParams.set("max_price", params.max_price.toString());
  if (params?.sort_by) url.searchParams.set("sort_by", params.sort_by);
  if (params?.page) url.searchParams.set("page", params.page.toString());
  if (params?.page_size) url.searchParams.set("page_size", params.page_size.toString());

  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch products");
  return res.json();
}

export async function fetchProductDetail(idOrSlug: string): Promise<ProductDetail> {
  const res = await fetch(`${getApiBaseUrl()}/products/${idOrSlug}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch product details");
  return res.json();
}

export async function searchProducts(params: {
  q: string;
  category?: string;
  min_price?: number;
  max_price?: number;
  page?: number;
  include_live?: boolean;
}): Promise<SearchResponse> {
  const url = new URL(`${getApiBaseUrl()}/search`);
  url.searchParams.set("q", params.q);
  if (params.category) url.searchParams.set("category", params.category);
  if (params.min_price) url.searchParams.set("min_price", params.min_price.toString());
  if (params.max_price) url.searchParams.set("max_price", params.max_price.toString());
  if (params.page) url.searchParams.set("page", params.page.toString());
  if (params.include_live) url.searchParams.set("include_live_scraping", "true");

  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) throw new Error("Search request failed");
  return res.json();
}

export async function compareVariants(variantIds: string[]): Promise<CompareResponse> {
  const res = await fetch(`${getApiBaseUrl()}/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ variant_ids: variantIds }),
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to generate comparison");
  return res.json();
}

export async function fetchRecommendations(body: {
  category_slug?: string;
  max_budget?: number;
  intent?: string;
  preferred_brands?: string[];
}): Promise<RecommendationResponse> {
  const res = await fetch(`${getApiBaseUrl()}/recommendations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to calculate recommendations");
  return res.json();
}

export async function fetchPriceHistory(variantId: string, days = 90): Promise<PriceHistoryResponse> {
  const res = await fetch(`${getApiBaseUrl()}/products/${variantId}/prices?days=${days}`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to retrieve price history");
  return res.json();
}

export async function chatAssistant(body: {
  message: string;
  conversation_id?: string;
  category_slug?: string;
  max_budget?: number;
}): Promise<ChatResponse> {
  const res = await fetch(`${getApiBaseUrl()}/assistant/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Assistant request failed");
  return res.json();
}

export async function fetchWatchlist(): Promise<ProductSummary[]> {
  const res = await fetch(`${getApiBaseUrl()}/watchlist`, {
    headers: getAuthHeader(),
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch watchlist");
  return res.json();
}

export async function addToWatchlist(variantId: string): Promise<void> {
  const res = await fetch(`${getApiBaseUrl()}/watchlist`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ variant_id: variantId }),
  });
  if (!res.ok) throw new Error("Failed to add to watchlist");
}

export async function removeFromWatchlist(variantId: string): Promise<void> {
  const res = await fetch(`${getApiBaseUrl()}/watchlist/${variantId}`, {
    method: "DELETE",
    headers: getAuthHeader(),
  });
  if (!res.ok) throw new Error("Failed to remove from watchlist");
}

export async function fetchAlerts(): Promise<any[]> {
  const res = await fetch(`${getApiBaseUrl()}/alerts`, {
    headers: getAuthHeader(),
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch alerts");
  return res.json();
}

export async function createAlert(variantId: string, targetPrice: number): Promise<any> {
  const res = await fetch(`${getApiBaseUrl()}/alerts`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeader() },
    body: JSON.stringify({ variant_id: variantId, target_price: targetPrice }),
  });
  if (!res.ok) throw new Error("Failed to create price alert");
  return res.json();
}

export async function fetchAlertNotifications(): Promise<any[]> {
  try {
    const res = await fetch(`${getApiBaseUrl()}/alerts/notifications`, {
      headers: getAuthHeader(),
      cache: "no-store",
    });
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export async function dismissAlertNotification(alertId: string): Promise<void> {
  const res = await fetch(`${getApiBaseUrl()}/alerts/${alertId}/dismiss`, {
    method: "POST",
    headers: getAuthHeader(),
  });
  if (!res.ok) throw new Error("Failed to dismiss alert");
}

export async function fetchProviderHealth(): Promise<any> {
  const res = await fetch(`${getApiBaseUrl()}/health/providers`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch provider health");
  return res.json();
}
