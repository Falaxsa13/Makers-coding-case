import json
from typing import List, Dict, Union

# Load inventory from a JSON file
def load_inventory(file_path: str = "app/data/inventory.json") -> List[Dict[str, Union[str, int]]]:
    with open(file_path, "r") as f:
        return json.load(f)
    
# Filter items by category
def filter_by_category(category: str, inventory: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:
    return [item for item in inventory if item["category"] == category and item["quantity"] > 0]

# Find an item by name
def find_item_by_name(item_name: str, inventory: List[Dict[str, Union[str, int]]]) -> Dict[str, Union[str, int]]:
    for item in inventory:
        if item_name.lower() in item["name"].lower():
            return item
    return None