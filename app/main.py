from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import create_tables, drop_tables
from api.v1.routes import user, auth

allow_all = ['*']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all,
)

app.include_router(auth.router)
app.include_router(user.router)


@app.on_event("startup")
async def startup_event():
    drop_tables()
    create_tables()
