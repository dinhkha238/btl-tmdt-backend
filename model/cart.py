
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from dbconnect import Base
class CartBase(BaseModel):
    customerId: int
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None
    totalCart: Optional[float] = None

class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customerId = Column(Integer, nullable=True)
    createdAt = Column(String(255), nullable=True)
    updatedAt = Column(String(255), nullable=True)