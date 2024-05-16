from typing import Optional
from pydantic import BaseModel


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

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
