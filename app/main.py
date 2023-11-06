from fastapi import FastAPI

from db.database import create_tables, drop_tables
from middleware import get_cors_middleware

app = FastAPI()

app.add_middleware(get_cors_middleware())


@app.on_event("startup")
async def startup_event():
    drop_tables()
    create_tables()
