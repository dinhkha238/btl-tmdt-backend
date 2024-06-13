from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from dbconnect import Base

class ProductBase(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None
    releaseDate: Optional[str] = None
    provider: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    spec: Optional[str] = None
    version: Optional[str] = None
    roomType: Optional[str] = None
    series: Optional[str] = None
    discriminator: Optional[str] = None
    employeeId: int
    url: Optional[str] = None


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    summary = Column(String(255), nullable=True)
    releaseDate = Column(String(255), nullable=True)
    provider = Column(String(255), nullable=True)
    brand = Column(String(255), nullable=True)
    model = Column(String(255), nullable=True)
    spec = Column(String(255), nullable=True)
    version = Column(String(255), nullable=True)
    roomType = Column(String(255), nullable=True)
    series = Column(String(255), nullable=True)
    discriminator = Column(String(255), nullable=True)
    employeeId = Column(Integer, nullable=True)
    url = Column(String(255), nullable=True)
