
from typing import Optional
from pydantic import BaseModel

class ShipmentBase(BaseModel):
    fees: float
    address: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    note: Optional[str] = None

class Shipment(ShipmentBase):
    id: int

    class Config:
        orm_mode = True