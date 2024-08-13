from sqlalchemy import insert

from database import session_maker
from models.Items_models.Weapon_models import Weapons, Weapon_Category

class WeaponsDAO:
    
    @classmethod
    def create_weapon(cls, type, attack, critic, active, frog_id):
        query = insert(Weapons).values(type=type, attack=attack, critic=critic, active=active, frog_id=frog_id)
        session_maker().execute(query)
        session_maker().commit()

    
    @classmethod
    def update_weapon(cls, weapon_id, type, attack, critic, active):
        weapon = session_maker().query(Weapons).filter_by(id=weapon_id).first()
        if weapon:
            weapon.type = type
            weapon.attack = attack
            weapon.critic = critic
            weapon.active = active
            session_maker().commit()
            return weapon
        return None

    def switch_active(cls, weapon_id):
        weapon = session_maker().query(Weapons).filter_by(id=weapon_id).first()
        if weapon:
            weapon.active = not (weapon.active)
            session_maker().commit()
            return weapon
        return None
    
class Weapon_categoryDAO:
    
    @classmethod
    def create_weapon_category(cls, name):
        query = insert(Weapon_Category).values(category_name = name)
        session_maker().execute(query)
        session_maker().commit()

