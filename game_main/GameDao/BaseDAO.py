from database import session_maker

from database import Base

import random

from sqlalchemy import select, insert, delete


class BaseDAO():
    model:Base
    @classmethod
    def find_by_id(cls, model: Base, model_id: int):
            session = session_maker()
            query = select(model).filter_by(id=model_id)
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