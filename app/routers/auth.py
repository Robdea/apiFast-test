from datetime import timedelta
from fastapi import APIRouter, Cookie, Depends, HTTPException, Body, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError 

from ..models import users
from .. import schemas, auth, database

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    resp: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(users.User).where(
            (users.User.username == form_data.username) | 
            (users.User.email == form_data.username)
        )
    )
    user = result.scalars().first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    
    token = auth.create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = auth.create_refresh_token({"sub": str(user.id)})

    resp.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,   
        samesite="strict",
        max_age=60 * auth.ACCESS_TOKEN_EXPIRE_MINUTES,
        path="/"
    )
    resp.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * int(auth.REFRESH_TOKEN_EXPIRE_DAYS),  # días → segundos
        path="/"
    )

    return {"message": "Login exitoso", "user": {"id": user.id, "username": user.username, "email": user.email}}

@router.post("/refresh")
async def refresh_token(req: Request, response: Response):
    refresh_token = req.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
    
    try:
        payload = jwt.decode(refresh_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        if payload.get("scope") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid scope")
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        new_access_token = auth.create_access_token(
            {"sub": user_id},
            expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,   # en dev puedes usar False
            samesite="strict",
            max_age=60 * auth.ACCESS_TOKEN_EXPIRE_MINUTES,
            path="/"
        )
        
        return {"message": "Access token refreshed"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        


@router.get("/me")
async def get_me(acces_token: str = Cookie(None)):
    if not acces_token:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    payload = auth.decoe_access_token(acces_token)
    user_id = payload.get("sub")
    
    return {"user_id": user_id}

