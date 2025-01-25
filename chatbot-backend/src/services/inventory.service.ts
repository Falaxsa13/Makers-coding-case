import inventory from "../data/inventory.json";

export function getInventory() {
  return inventory;
}

export function getItemDetails(brand: string) {
  return inventory.computers.find(
    (item) => item.brand.toLowerCase() === brand.toLowerCase()
  );
}
