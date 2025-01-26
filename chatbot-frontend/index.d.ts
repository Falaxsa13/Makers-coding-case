export type BrandResponse = {
  brand: string;
  products: number;
};
export type CategoriesResponse = {
  category: string;
  products: number;
};

export type PriceCategoryResponse = {
  price_category: string;
  count: number;
};

export type Item = {
  id: number;
  name: string;
  quantity: number;
  category: string;
  price: float;
  price_category: string;
  brand: string;
  description: string;
};
