from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, boardsRoute, usersRoute, listsRoute, cardsRoute
from .database import engine, Base
from .models import *

# App
app = FastAPI()

origins = ["http://localhost:5173", "http://127.0.0.1:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas al iniciar
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Rutas
app.include_router(usersRoute.router)
app.include_router(auth.router)
app.include_router(boardsRoute.router)
app.include_router(listsRoute.router)
app.include_router(cardsRoute.router)
