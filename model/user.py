from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from dbconnect import Base

class UserBase(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    gender: Optional[str] = None
    birth: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    fullname = Column(String(255), nullable=True)
    gender = Column(String(255), nullable=True)
    birth = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    contact = Column(String(255), nullable=True)    


