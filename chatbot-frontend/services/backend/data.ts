"use server";
const BASE_URL = "http://localhost:8000/api/inventory";
export const getInventory = async () => {
  const response = await fetch(BASE_URL);
  const inventory = await response.json();
  return inventory;
};

export const countProductsByBrand = async () => {
  const response = await fetch(`${BASE_URL}/count-by-brand`);
  const count = await response.json();
  return count;
};

export const countProductsByCategory = async () => {
  const response = await fetch(`${BASE_URL}/count-by-category`);
  const count = await response.json();
  return count;
};

export const countProductsByPriceCategory = async () => {
  const response = await fetch(`${BASE_URL}/count-by-price-category`);
  const count = await response.json();
  return count;
};

export const sortByPrice = async (descending: boolean) => {
  const query = !descending ? "?descending=false" : "";
  const response = await fetch(`${BASE_URL}/sort-by-price${query}`);
  const sorted = await response.json();
  return sorted;
};

export const sortByQuantity = async (descending: boolean) => {
  const query = !descending ? "?descending=false" : "";
  const response = await fetch(`${BASE_URL}/sort-by-quantity${query}`);
  const sorted = await response.json();
  return sorted;
};
