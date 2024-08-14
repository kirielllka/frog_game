from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base



class Weapon_Category(Base):
    __tablename__ = 'weapons_category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String)


class Weapons(Base):
    __tablename__ = 'weapons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(Integer, ForeignKey('weapons_category.id'))
    attack = Column(Integer)
    critic = Column(Integer, default=0)
    active = Column(Boolean, default=False)
    frog_id = Column(Integer, ForeignKey('frog.id'))