import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Board(Base):
    __tablename__="boards"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(50), nullable=False)
    
    owner = relationship("User", back_populates="boards")
    lists = relationship("List", back_populates="board")
    