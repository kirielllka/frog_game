from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base

class Item(Base):
    id = Column(Integer, primary_key=True)
    class_item = Column(String)
    item = String()