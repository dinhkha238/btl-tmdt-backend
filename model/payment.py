
from typing import Optional
from pydantic import BaseModel

class PaymentBase(BaseModel):
    name: str
    currency: Optional[str] = None
    cardNum: Optional[str] = None
    type: Optional[str] = None
    discriminator: Optional[str] = None

class Payment(PaymentBase):
    id: int

    class Config:
        orm_mode = True