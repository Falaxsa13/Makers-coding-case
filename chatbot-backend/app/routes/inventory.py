from fastapi import APIRouter, HTTPException
from app.services.inventory import load_inventory, get_item_details

router = APIRouter()

@router.get("/")
def get_inventory():
    return load_inventory()

@router.get("/{brand}")
def get_computer_by_brand(brand: str):
    item = get_item_details(brand)
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")
