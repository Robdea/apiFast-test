import uuid
from pydantic import BaseModel

class BoardCreate(BaseModel):
    name: str

class BoardOut(BaseModel):
    id: uuid.UUID
    name: str
    owner_id: int
    class Config:
        orm_mode = True
    