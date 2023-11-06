import random

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import authenticate_user, create_access_token, get_current_user
from app.db.database import get_db

router = APIRouter()


@router.post(path="authenticate")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos!")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/quem-vai-pagar-o-habibao/")
def protected_resource(current_user: str = Depends(get_current_user)):
    esfiha_payer = ["Ivan",
                    "Mari",
                    "Bob",
                    "Rodrigo",
                    "Edson",
                    "Ocimar",
                    "Nayara"
                    ]

    return {
        "msg": "Parabéns! Você acessou o endpoint secreto e agora vai descobrir quem vai pagar o próximo rodízio do "
               "Habibão!",
        "rodizio_por_conta_de": random.choice(esfiha_payer),
        "user": current_user}


@router.get("/current-user/")
def get_current_user(current_user: str = Depends(get_current_user)):
    return {"current_user": current_user}
