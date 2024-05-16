
from typing import Optional
from pydantic import BaseModel


class CartProductItemBase(BaseModel):
    cartId: Optional[int] = None
    productItemId: int
    quantity: int
    name: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None

class CartProductItem(CartProductItemBase):
    id: int

    class Config:
        orm_mode = True