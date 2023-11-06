from sqlalchemy.orm import Session

from models.collector import Collector, CollectorRequest
from models.donator import Donator, DonatorRequest
from services.auth_service import hash_password


def get_donator_by_email(db: Session, email: str):
    return db.query(Donator).filter(Donator.email == email).first()


def get_collector_by_email(db: Session, email: str):
    return db.query(Collector).filter(Collector.email == email).first()


def get_donators(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Donator).offset(skip).limit(limit).all()


def get_collectors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Collector).offset(skip).limit(limit).all()


def create_donator(db: Session, request: DonatorRequest):
    hashed_password = hash_password(request.password)

    new_donator = Donator(
        name=request.name,
        surname=request.surname,
        email=request.email,
        password=hashed_password,
        telephone=request.telephone
    )

    db.add(new_donator)
    db.commit()
    db.close()


def create_collector(db: Session, request: CollectorRequest):
    hashed_password = hash_password(request.password)

    new_collector = Collector(
        document=request.document,
        email=request.email,
        telephone=request.telephone,
        hashed_password=hashed_password,
        cep=request.cep,
        address=request.address,
        district=request.district,
        allow_delivery=request.allow_delivery
    )

    db.add(new_collector)
    db.commit()
    db.close()
