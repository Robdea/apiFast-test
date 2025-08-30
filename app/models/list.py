import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class List(Base):
    __tablename__="lists"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    board_id = Column(String(36), ForeignKey("boards.id"))
    title= Column(String(90), nullable=False)
    position = Column(Integer, nullable=False)
    
    board = relationship("Board", back_populates="lists")
    cards = relationship("Card", back_populates="list")
    
