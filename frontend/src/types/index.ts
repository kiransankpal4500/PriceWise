export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  icon_name?: string;
  product_count: number;
}

export interface Brand {
  id: string;
  name: string;
  slug: string;
  logo_url?: string;
}

export interface Specification {
  spec_group: string;
  name: string;
  value: string;
}

export interface MarketplaceListing {
  id: string;
  marketplace_id: string;
  marketplace_name: string;
  marketplace_slug: string;
  marketplace_logo?: string;
  external_id: string;
  title: string;
  product_url: string;
  image_url?: string;
  current_price: number;
  original_mrp?: number;
  discount_percentage?: number;
  availability: string;
  seller_name?: string;
  rating?: number;
  review_count?: number;
  is_demo: boolean;
  last_scraped_at: string;
}

export interface ProductVariant {
  id: string;
  product_id: string;
  name: string;
  sku: string;
  ram?: string;
  storage?: string;
  color?: string;
  mrp: number;
  best_price?: number;
  specifications: Specification[];
  listings: MarketplaceListing[];
}

export interface ProductSummary {
  id: string;
  name: string;
  slug: string;
  brand_name: string;
  brand_slug: string;
  category_name: string;
  category_slug: string;
  model_number?: string;
  description?: string;
  image_url?: string;
  best_price: number;
  mrp: number;
  discount_percentage?: number;
  marketplace_count: number;
  rating?: number;
  review_count?: number;
  is_demo: boolean;
  primary_variant_id: string;
}

export interface ProductDetail {
  id: string;
  name: string;
  slug: string;
  brand: Brand;
  category: Category;
  model_number?: string;
  description?: string;
  default_image_url?: string;
  variants: ProductVariant[];
  best_offer?: MarketplaceListing;
  lowest_recorded_price?: number;
  highest_recorded_price?: number;
  average_price?: number;
  total_reviews_analyzed: number;
  sentiment_distribution: Record<string, number>;
}

export interface SearchResponse {
  query: string;
  total_results: number;
  page: number;
  page_size: number;
  total_pages: number;
  items: ProductSummary[];
  categories_found: string[];
  brands_found: string[];
  providers_consulted: Record<string, string>;
}

export interface CompareProductColumn {
  variant_id: string;
  product_id: string;
  product_name: string;
  variant_name: string;
  brand_name: string;
  category_name: string;
  image_url?: string;
  best_price: number;
  mrp: number;
  rating: number;
  review_count: number;
  listings: MarketplaceListing[];
  specs: Record<string, Record<string, string>>;
}

export interface CompareResponse {
  products: CompareProductColumn[];
  all_spec_groups: string[];
  specs_matrix: Record<string, Record<string, (string | null)[]>>;
  winner_variant_id?: string;
  winner_rationale?: string;
  compromises: Record<string, string[]>;
}

export interface RecommendationScoreDetail {
  overall_score: number;
  price_score: number;
  spec_score: number;
  rating_score: number;
  review_volume_score: number;
  value_score: number;
  badge?: string;
  key_strengths: string[];
  tradeoffs: string[];
}

export interface RecommendedProductItem {
  product: ProductSummary;
  variant_id: string;
  scores: RecommendationScoreDetail;
  explanation: string;
}

export interface RecommendationResponse {
  category_slug?: string;
  budget_applied?: number;
  algorithm_version: string;
  weights_applied: Record<string, number>;
  recommendations: RecommendedProductItem[];
}

export interface PriceHistoryPoint {
  date: string;
  price: number;
  marketplace: string;
  marketplace_slug: string;
  source: string;
}

export interface PriceHistoryResponse {
  variant_id: string;
  variant_name: string;
  currency: string;
  days_covered: number;
  lowest_price: number;
  highest_price: number;
  average_price: number;
  current_price: number;
  trend: string;
  history: PriceHistoryPoint[];
}

export interface ChatResponse {
  conversation_id: string;
  message: string;
  extracted_requirements?: {
    category_slug?: string;
    budget?: number;
    preferred_brands: string[];
    key_priorities: string[];
  };
  recommended_products: ProductSummary[];
  suggested_follow_ups: string[];
  tokens_used: number;
  model_used: string;
}
