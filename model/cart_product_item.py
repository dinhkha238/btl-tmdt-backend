
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from dbconnect import Base

class CartProductItemBase(BaseModel):
    cartId: Optional[int] = None
    productItemId: int
    quantity: int
    name: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    inStock: Optional[int] = None

class CartProductItem(Base):
    __tablename__ = 'cart_product_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cartId = Column(Integer, nullable=True)
    productItemId = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)