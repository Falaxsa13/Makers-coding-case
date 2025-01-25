from pydantic import BaseModel
from typing import List

class Computer(BaseModel):
    id: int
    brand: str
    quantity: int

class Inventory(BaseModel):
    computers: List[Computer]
