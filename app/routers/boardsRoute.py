from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import Board
from .. import database
from ..schemasFolder import boards
from ..dependencies import get_current_user
from ..models.users import User

router = APIRouter(prefix="/boards", tags=["Boards"])


@router.get("/", response_model=list[boards.BoardOut])
async def get_boards(  
    db: AsyncSession = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    res = await db.execute(select(Board).where(Board.owner_id == current_user.id))
    
    boards = res.scalars().all()
    return boards
    
    

@router.post("/", response_model=boards.BoardOut)
async def create_board(
    board: boards.BoardCreate, 
    db: AsyncSession = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    new_board = Board(
        name=board.name,
        owner_id=current_user.id
    )
    
    db.add(new_board)
    await db.commit()
    await db.refresh(new_board)
    return new_board


