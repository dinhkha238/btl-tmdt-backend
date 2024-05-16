
from typing import Optional
from pydantic import BaseModel

class CartBase(BaseModel):
    customerId: int
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    totalCart: Optional[float] = None

class Cart(CartBase):
    id: int

    class Config:
        orm_mode = True