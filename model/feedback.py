
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from dbconnect import Base

class FeedbackBase(BaseModel):
    customerId: Optional[int] = None
    productId: int
    description: str
    rating: float
    createdAt: Optional[str] = None
    # customer: Optional[str] = None

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customerId = Column(Integer, nullable=True)
    productId = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    rating = Column(Float, nullable=True)
    createdAt = Column(String(255), nullable=True)
