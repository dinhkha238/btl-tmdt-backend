from typing import Optional
from model.product import ProductBase
from sqlalchemy import Column, Integer, String, Float
from dbconnect import Base

class ProductItemBase(ProductBase):
    productId: int
    employeeId: int
    price:float
    addedDate: Optional[str] = None
    inStock: int    

class ProductItem(Base):
    __tablename__ = 'product_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    productId = Column(Integer, nullable=True)
    employeeId = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
    addedDate = Column(String(255), nullable=True)
    inStock = Column(Integer, nullable=True)
    # discriminator = Column(String(255), nullable=True)

# class ProductItem(ProductItemBase):
#     id: int

#     class Config:
#         orm_mode = True
