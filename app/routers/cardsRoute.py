from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user
from .. import database
from sqlalchemy.future import select
from ..models import Card, User, List
from ..schemasFolder import cards


router = APIRouter(prefix="/lists", tags=["Cards"])

@router.get("/{list_id}/card", response_model=list[cards.CardOut])
async def get_cards(
    list_id: str,
    db: AsyncSession = Depends(database.get_db),
):
    res = await db.execute(select(Card).where(Card.list_id == list_id).order_by(Card.position))
    
    return res.scalars().all()
    

@router.post("/{list_id}/card", response_model=cards.CardCreate)
async def create_card(
    list_id: str,
    card_data: cards.CardCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: User = Depends(get_current_user)
):
    res = await db.execute(
        select(List).where(List.id == list_id)
    )
    
    list_user = res.scalars().first()
    
    if not list_user:
        raise HTTPException(status_code=404, detail="Lista no encontrado o no permitido")
    
    new_card = Card(
        title = card_data.title,
        description = card_data.description,
        position = card_data.position,
        list_id = list_user.id
    )
    
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card
    