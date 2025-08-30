import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Card(Base):
    __tablename__="cards"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    list_id = Column(String(36), ForeignKey("lists.id"))
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    position = Column(Integer, nullable=False)
    
    list = relationship("List", back_populates="cards")
    
    