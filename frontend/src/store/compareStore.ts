import { create } from "zustand";

interface CompareStore {
  selectedVariantIds: string[];
  addVariant: (id: string) => boolean;
  setVariants: (ids: string[]) => void;
  removeVariant: (id: string) => void;
  clear: () => void;
  hasVariant: (id: string) => boolean;
}

export const useCompareStore = create<CompareStore>((set, get) => ({
  selectedVariantIds: [],
  addVariant: (id: string) => {
    const current = get().selectedVariantIds;
    if (current.includes(id)) return true;
    if (current.length >= 4) return false;
    set({ selectedVariantIds: [...current, id] });
    return true;
  },
  setVariants: (ids: string[]) => {
    set({ selectedVariantIds: ids.slice(0, 4) });
  },
  removeVariant: (id: string) => {
    set({ selectedVariantIds: get().selectedVariantIds.filter((item) => item !== id) });
  },
  clear: () => set({ selectedVariantIds: [] }),
  hasVariant: (id: string) => get().selectedVariantIds.includes(id),
}));
