import uuid
from pydantic import BaseModel

class CardCreate(BaseModel):
    title: str
    description: str
    position: int

class CardOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    position: int
    list_id: uuid.UUID
    class Config:
        orm_mode = True
    