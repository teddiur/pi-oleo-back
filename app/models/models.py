from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    city = Column(String)
    district = Column(String)
    oil_quantity = Column(Integer)
    
class UserRequest(BaseModel):
    email: str
    name: str
    password: str
    city: str
    district: str
    oil_quantity: int
    
class UserResponse(BaseModel):
    msg: str
    
class UserListResponse(BaseModel):
    id: int
    email: str
    name: str
    city: str
    district: str
    oil_quantity: int