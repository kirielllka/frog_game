from sqlalchemy import insert, select

from game_main.GameDao.BaseDAO import BaseDAO

from models.Frog_models import Frog
from database import session_maker
from models.Items_models.Weapon_models import Weapons, Weapon_Category

class WeaponsDAO(BaseDAO):

    @classmethod
    def switch_active(cls, weapon_id):
        session = session_maker()
        weapon = session.query(Weapons).filter_by(id=weapon_id).first()
        if weapon:
            curr_weapon = session.query(Weapons).filter_by(frog_id = weapon.frog_id, active = True).first()
            print(curr_weapon)
            if curr_weapon:
                curr_weapon.active = False
            weapon.active = True
            session.commit()
            return weapon
        return None

    @classmethod
    def find_active(cls, frog_id: int):
            session = session_maker()
            query = select(Weapons).filter_by(frog_id=frog_id, active=True)
            result = session.execute(query)
            return result.fetchall()[0]



