from database import session_maker as session

from database import Base

import random

from sqlalchemy import select, insert


class BaseDAO():
    model:Base
    @classmethod
    def find_by_id(cls, model: Base, model_id: int):
            query = select(model).filter_by(id=model_id)
            result = session().execute(query)
            return result.fetchall()[0]