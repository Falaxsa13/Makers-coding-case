import json
from typing import List, Dict, Union

# Load inventory from a JSON file
def load_inventory(file_path: str = "app/data/inventory.json") -> List[Dict[str, Union[str, int]]]:
    with open(file_path, "r") as f:
        return json.load(f)

# Find an item by name
def find_item_by_name(item_name: str, inventory: List[Dict[str, Union[str, int]]]) -> Dict[str, Union[str, int]]:
    for item in inventory:
        if item_name.lower() in item["name"].lower():
            return item
    return None
