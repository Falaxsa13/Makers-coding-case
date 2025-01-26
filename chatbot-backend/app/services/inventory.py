import json
from typing import Dict, List
from app.models.inventory import Inventory, Computer

def load_inventory() -> Inventory:
    with open("app/data/inventory.json", "r") as file:
        data = json.load(file)
    return Inventory(computers=[Computer(**item) for item in data])

def get_item_details(brand: str) -> Computer:
    inventory = load_inventory()
    for item in inventory.computers:
        if item.brand.lower() == brand.lower():
            return item
    return None


# Quantity of products in inventory of the same brand
def count_products_by_brand() -> List[Dict[str, int]]:
    inventory = load_inventory()
    brand_counts = {}
    for item in inventory.computers:
        brand = item.brand
        if brand in brand_counts:
            brand_counts[brand] += 1
        else:
            brand_counts[brand] = 1
    return [{"brand": brand, "products": count} for brand, count in brand_counts.items()]

# Quantity of products by category
def count_products_by_category() -> List[Dict[str, int]]:
    inventory = load_inventory()
    category_counts = {}
    for item in inventory.computers:
        category = item.category
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1
    return [{"category": category, "products": count} for category, count in category_counts.items()]



# Sorting products by quantity 
def sort_items_by_quantity(descending: bool = True) -> List[Computer]:
    inventory = load_inventory()
    return sorted(inventory.computers, key=lambda x: x.quantity, reverse=descending)

# Sorting products by price
def sort_items_by_price(descending: bool = True) -> List[Computer]:
    inventory = load_inventory()
    return sorted(inventory.computers, key=lambda x: x.price, reverse=descending)

