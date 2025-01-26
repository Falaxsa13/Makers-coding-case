from pydantic import BaseModel
from typing import List

class Computer(BaseModel):
    id: int
    name: str
    quantity: int
    category: str
    price: float
    price_category: str
    brand: str
    description: str

class Inventory(BaseModel):
    computers: List[Computer]
