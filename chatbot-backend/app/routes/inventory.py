from fastapi import APIRouter, HTTPException
from app.services.inventory import count_products_by_category, count_products_by_brand, count_products_by_price_category, load_inventory, sort_items_by_price, sort_items_by_quantity

router = APIRouter()

@router.get("/")
def get_inventory():
    return load_inventory()


@router.get("/count-by-brand")
def get_count_by_brand():
    return count_products_by_brand()

@router.get("/count-by-category")
def get_count_by_category():
    return count_products_by_category()




@router.get("/sort-by-quantity")
def get_sorted_by_quantity(descending: bool = True):
    return sort_items_by_quantity(descending)

@router.get("/sort-by-price")
def get_sorted_by_price(descending: bool = True):
    return sort_items_by_price(descending)