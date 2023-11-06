from typing import Optional

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.collector import Collector
from app.models.donator import Donator
from app.config import SECRET_KEY, ALGORITHM

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=403, detail="Erro ao validar credenciais")
    except JWTError:
        raise HTTPException(status_code=403, detail="Erro ao validar credenciais")

    donator = db.query(Donator).filter(Donator.email == email).first()
    collector = db.query(Collector).filter(Collector.email == email).first()

    if donator is None or collector is None:
        raise HTTPException(status_code=403, detail="User não encontrado")

    return email


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
    user = db.query(User).filter(User.email == username).first()

    db.close()

    if not user:
        return False

    if not pwd_context.verify(password, user.hashed_password):
        return False

    return user
