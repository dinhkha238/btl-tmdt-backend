
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from dbconnect import Base
class PaymentBase(BaseModel):
    name: str
    currency: Optional[str] = None
    cardNum: Optional[str] = None
    type: Optional[str] = None
    discriminator: Optional[str] = None

# class Payment(PaymentBase):
#     id: int

#     class Config:
#         orm_mode = True



class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    currency = Column(String(255), nullable=True)
    cardNum = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    discriminator = Column(String(255), nullable=True)

