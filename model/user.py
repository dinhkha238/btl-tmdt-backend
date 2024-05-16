from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str
    fullname: Optional[str] = None
    gender: Optional[str] = None
    birth: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
