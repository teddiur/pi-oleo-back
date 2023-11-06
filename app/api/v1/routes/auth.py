from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.donator import Donator
from app.config import SECRET_KEY, ALGORITHM

router = APIRouter()


@router.post(path="authenticate")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos!")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=403, detail="Erro ao validar credenciais")
    except JWTError:
        raise HTTPException(status_code=403, detail="Erro ao validar credenciais")

    user = user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=403, detail="User não encontrado")

    return user.email


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Donator).filter(Donator.email == username).first()

    db.close()

    if not user:
        return False

    if not pwd_context.verify(password, user.hashed_password):
        return False

    return user
