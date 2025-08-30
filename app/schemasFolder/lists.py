import uuid
from pydantic import BaseModel

class ListCreate(BaseModel):
    title: str
    position: int
    

class ListsOut(BaseModel):
    id: uuid.UUID
    title: str
    board_id: uuid.UUID
    position: int
    class Config:
        orm_mode = True
    