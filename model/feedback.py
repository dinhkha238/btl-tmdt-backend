
from typing import Optional
from pydantic import BaseModel

class FeedbackBase(BaseModel):
    customerId: Optional[int] = None
    productId: int
    description: str
    rating: float
    createdAt: Optional[str] = None
    customer: Optional[str] = None

class Feedback(FeedbackBase):
    id: int

    class Config:
        orm_mode = True