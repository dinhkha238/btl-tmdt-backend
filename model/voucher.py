
from typing import Optional
from pydantic import BaseModel

class VoucherBase(BaseModel):
    name: str
    expireDate: str
    quantity: Optional[int] = None
    value: Optional[float] = None
    percentage: Optional[int] = None
    discriminator: Optional[str] = None

class Voucher(VoucherBase):
    id: int

    class Config:
        orm_mode = True