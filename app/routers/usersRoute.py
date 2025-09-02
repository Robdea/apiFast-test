from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import users


from .. import schemas, auth, database

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    db_user = users.User(username=user.username, email=user.email, hashed_password=auth.hash_password(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
