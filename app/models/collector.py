from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from app.models.user import User


class Collector(User):
    __tablename__ = "collector"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    document = Column(String)
    telephone = Column(String)
    cep = Column(String)
    address = Column(String)
    district = Column(String)
    allow_delivery = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'collector'
    }


class CollectorResponse(BaseModel):
    msg: str


class CollectorListResponse(BaseModel):
    email: str
    telephone: str
    cep: str
    address: str
    district: int
    allow_delivery: bool
