from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, boardsRoute, usersRoute, listsRoute
from .database import engine, Base
from .models import *

# App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción pon tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al iniciar
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(usersRoute.router)
app.include_router(auth.router)
app.include_router(boardsRoute.router)
app.include_router(listsRoute.router)
