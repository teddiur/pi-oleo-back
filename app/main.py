import random
import os

from typing import Union, Annotated, Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

from models.models import User, UserRequest, UserResponse, UserListResponse
from database import get_db, create_tables, drop_tables

load_dotenv()

app = FastAPI()

allow_all = ['*']

app.add_middleware(CORSMiddleware,
                   allow_origins=allow_all,
                   allow_credentials=True,
                   allow_methods=allow_all,
                   allow_headers=allow_all)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup_event():
    drop_tables()
    create_tables()
    
@app.get("/users/", response_model=list[UserListResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post("/create_user/", response_model=UserResponse)
async def create_user(userRequest: UserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == userRequest.email).first()
    
    if existing_user:
        raise HTTPException(status_code=409, detail="O usuário informado já é cadastrado.")
    
    hashed_password = pwd_context.hash(userRequest.password)
    
    user = User(
            name=userRequest.name,
            city=userRequest.city,
            district=userRequest.district,
            oil_quantity=userRequest.oil_quantity,
            email=userRequest.email,
            hashed_password=hashed_password)    
    
    db.add(user)
    db.commit()
    db.close()
    return {"msg": "Uhuu! Usuário criado com sucesso!"}


@app.post("/token/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):    

    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:    
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos!")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=403, detail="Erro ao validar credenciais")
    except JWTError:
        raise HTTPException(status_code=403, detail="Erro ao validar credenciais")

    user = user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise HTTPException(status_code=403, detail="User não encontrado")

    return user.email


@app.get("/descubra/")
async def protected_resource(current_user: UserResponse = Depends(get_current_user)):
    esfiha_payer = ["Ivan",
                    "Mari",
                    "Bob",
                    "Rodrigo",
                    "Edson",
                    "Ocimar",
                    "Nayara"                       
                    ]
    
    return {"msg": "Parabéns! Você acessou o endpoint secreto e agora vai descobrir quem vai pagar o próximo rodízio do Habibão!",
            "rodizio_por_conta_de": random.choice(esfiha_payer), 
            "user": current_user}



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


    



