
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from dbconnect import Base

class VoucherBase(BaseModel):
    name: str
    expireDate: str
    quantity: Optional[int] = None
    value: Optional[float] = None
    percentage: Optional[int] = None
    discriminator: Optional[str] = None

class Voucher(Base):
    __tablename__ = 'voucher'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    expireDate = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=True)
    value = Column(Float, nullable=True)
    percentage = Column(Integer, nullable=True)
    discriminator = Column(String(255), nullable=True)
