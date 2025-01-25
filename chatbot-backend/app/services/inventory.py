import json
from app.models.inventory import Inventory, Computer

def load_inventory() -> Inventory:
    with open("app/data/inventory.json", "r") as file:
        data = json.load(file)
    return Inventory(**data)

def get_item_details(brand: str) -> Computer:
    inventory = load_inventory()
    for item in inventory.computers:
        if item.brand.lower() == brand.lower():
            return item
    return None
