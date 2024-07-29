from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Frog(Base):
    __tablename__ = 'frog'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lvl = Column(Integer, default=1)
    strengh = Column(Integer, default=1)
    agility = Column(Integer, default=1)
    endurance = Column(Integer, default=1)
    atack = Column(Integer, default=1)
    update_point = Column(Integer, default=0)
    max_lvl = Column(Integer, default=1)

