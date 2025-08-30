from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import List, Board
from .. import database
from ..schemasFolder import lists
from ..dependencies import get_current_user
from ..models.users import User

router = APIRouter(prefix="/boards", tags=["Lists"])


@router.post("/{board_id}/list", response_model=lists.ListCreate)
async def create_board(
    board_id: str,
    lists_data: lists.ListCreate, 
    db: AsyncSession = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    res = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    
    board = res.scalars().first()
    if not board:
        raise HTTPException(status_code=404, detail="Board no encontrado o no permitido")
    
    new_list = List(
        title=lists_data.title,
        position= lists_data.position,
        board_id=board.id
    )
    
    db.add(new_list)
    await db.commit()
    await db.refresh(new_list)
    return new_list



