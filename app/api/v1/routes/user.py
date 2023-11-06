from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.collector import Collector, CollectorRequest
from app.models.donator import Donator, DonatorRequest
from app.services.auth_service import pwd_context

router = APIRouter()


@router.get(path="/donators/", description="Lista todos os usuários doadores")
def get_all_donators(db: Session = Depends(get_db)):
    return db.query(Donator).all()


@router.get(path="/collectors/", description="Lista todos os usuários coletores")
def get_all_collectors(db: Session = Depends(get_db)):
    return db.query(Collector).all()


@router.post(path="/donator/", description="Cria um usuário doador")
async def create_donator(request: DonatorRequest, db: Session = Depends(get_db)):
    if request.user_type != "doador":
        raise HTTPException(status_code=400, detail="Tipo de usuário incorreto.")

    existing_donator = db.query(Donator).filter(Donator.email == request.email).first()

    if existing_donator:
        raise HTTPException(status_code=409, detail="O usuário informado já é cadastrado.")

    hashed_password = pwd_context.hash(request.password)

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
    return {"msg": "Uhuu! Usuário criado com sucesso!"}


@router.post(path="/collector/", description="Cria um usuário retirador")
async def create_collector(request: CollectorRequest, db: Session = Depends(get_db)):
    if request.user_type != "retirador":
        raise HTTPException(status_code=400, detail="Tipo de usuário incorreto.")

    existing_collector = db.query(Collector).filter(Collector.email == request.email).first()

    if existing_collector:
        raise HTTPException(status_code=409, detail="O usuário informado já é cadastrado.")

    hashed_password = pwd_context.hash(request.password)

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
    return {"msg": "Uhuu! Usuário criado com sucesso!"}
