from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from pathlib import Path
import os
from datetime import timedelta

#configuracion del JWT
os.environ['AUTHJWT_SECRET_KEY'] = os.urandom(24).hex()
os.environ['AUTHJWT_ACCESS_TOKEN_EXPIRES'] = f"{1000000}" # un dia
os.environ[']AUTHJWT_REFRESH_TOKEN_EXPIRES'] = f"{7000000}" # 7 dias
os.environ['DB_SQLITE'] = str(1)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="API Ser_Postales",
    description="Servicios postales",
    version="1.0.0",
    openapi_tags=[],
)

origins = [
    "*",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
from views import *

#declaracion de la base de datos
db_sqlite = os.getenv("DB_SQLITE") or '0'
db_postgresql = os.getenv("DB_POSTGRESQL") or '0'
if db_sqlite == '1' and db_postgresql == '0':
    register_tortoise(
        app,
        db_url=f"sqlite://{BASE_DIR}/db.sqlite3",
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

if db_postgresql == '1':
    hostdb = os.getenv("DB_HOST") or "localhost"
    userdb = os.getenv("DB_USER") or "root"
    passwdb = os.getenv("DB_PASSWD") or "passwd"
    portdb = os.getenv("DB_PORT") or "5432"
    db_db = os.getenv("DB_DB") or "api"
    register_tortoise(
        app,
        db_url=f'postgres://{userdb}:{passwdb}@{hostdb}:{portdb}/{db_db}',
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
