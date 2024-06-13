from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from dbconnect import Base
class CustomerBase(BaseModel):
    userId: int

class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, nullable=True)
