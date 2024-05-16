from typing import Optional
from model.product import ProductBase

class ProductItemBase(ProductBase):
    productId: int
    employeeId: int
    price:float
    addedDate: Optional[str] = None
    inStock: int    

class ProductItem(ProductItemBase):
    id: int

    class Config:
        orm_mode = True
