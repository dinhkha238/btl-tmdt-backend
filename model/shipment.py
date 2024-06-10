
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from dbconnect import Base

class ShipmentBase(BaseModel):
    fees: float
    address: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    note: Optional[str] = None

class Shipment(Base):
    __tablename__ = 'shipment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fees = Column(Float, nullable=True)
    address = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    note = Column(String(255), nullable=True)

# class Shipment(ShipmentBase):
#     id: int

#     class Config:
#         orm_mode = True

