
from typing import Optional
from pydantic import BaseModel

class StatisticProductItemBase(BaseModel):
    productItemId: int
    nameProductItem: str
    totalQuantity:int
    totalRevenue:float

class StatisticProductItem(StatisticProductItemBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True