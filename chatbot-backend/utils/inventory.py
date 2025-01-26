import json
from typing import List, Dict, Union

# Load inventory from a JSON file
def load_inventory(file_path: str = "app/data/inventory.json") -> List[Dict[str, Union[str, int]]]:
    with open(file_path, "r") as f:
        return json.load(f)

def getProducts(query: str) -> str:
    """
    Returns a JSON string of products that match the 'query' in name or description.
    """
    inventory = load_inventory()
    query_lower = query.lower()
    results = [item for item in inventory 
               if query_lower in item["name"].lower() or query_lower in item["description"].lower()]

    return json.dumps(results, ensure_ascii=False)

def reply(message: str) -> str:
    """
    A trivial function that just returns the message. 
    You might choose to let the AI call 'reply' as a final step 
    or do it yourself in code, but here it's shown for illustration.
    """
    return message

def createNewOrder(customerId: int, productId: int, quantity: int, unitPrice: float) -> str:
    """
    Basic example of "creating an order" by deducting inventory and returning an order summary.
    """
    inventory = load_inventory()
    # Find product
    for item in inventory:
        if item["id"] == productId:
            if item["quantity"] < quantity:
                return f"Not enough stock for {item['name']}."
            # Deduct stock
            item["quantity"] -= quantity
            # Normally you would also store the "order" in a DB or local file
            # For demonstration, let's just write back the updated inventory:
            with open("app/data/inventory.json", "w", encoding="utf-8") as f:
                json.dump(inventory, f, ensure_ascii=False, indent=2)
            total = unitPrice * quantity
            return f"Order created: Customer {customerId}, {quantity}x {item['name']} at ${unitPrice} each. Total=${total}"

    return f"Product with id={productId} not found."


# Filter items by category
def filter_by_category(category: str, inventory: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:
    return [item for item in inventory if item["category"] == category and item["quantity"] > 0]

# Find an item by name
def find_item_by_name(item_name: str, inventory: List[Dict[str, Union[str, int]]]) -> Dict[str, Union[str, int]]:
    for item in inventory:
        if item_name.lower() in item["name"].lower():
            return item
    return None

# Load all item names
def load_all_item_names(inventory: List[Dict[str, Union[str, int]]]) -> List[str]:
    return [item["name"] for item in inventory]