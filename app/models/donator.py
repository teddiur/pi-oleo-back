from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel

from app.models.user import User


class Donator(User):
    __tablename__ = "donator"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    telephone = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'donator'
    }

class DonatorRequest(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    telephone: str
    user_type: str


class DonatorResponse(BaseModel):
    msg: str


class DonatorListResponse(BaseModel):
    email: str
    name: str
    surname: str
    telephone: str
