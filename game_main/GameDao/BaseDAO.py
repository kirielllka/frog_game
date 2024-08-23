from database import session_maker

from database import Base

import random

from sqlalchemy import select, insert, delete, update


class BaseDAO:
    model:Base
    @classmethod
    def find_by_id(cls, model, model_id: int):
            session = session_maker()
            query = select(model).where(model.id==model_id)
            result = session.execute(query)
            return result.fetchone()

    @classmethod
    def find_all(cls, model: Base):
        session = session_maker()
        query = select(model)
        result = session.execute(query)
        return [row for row in result.scalars()]


    @classmethod
    def delete(cls, model, model_id):
            session = session_maker()
            query = delete(model).where(model.id == model_id)
            session.execute(query)
            session.commit()

    @classmethod
    def update(cls, model, model_id, data:dict):
        with session_maker() as session:
            stmt = update(model).values(**data).where(model.id==model_id)
            session.execute(stmt)
            session.commit()

    @classmethod
    def insert(cls, model, data:dict):
        with session_maker() as session:
            stmt = insert(model).values(**data)