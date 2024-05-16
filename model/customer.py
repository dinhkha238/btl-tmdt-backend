from pydantic import BaseModel

class CustomerBase(BaseModel):
    userId: int

class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True