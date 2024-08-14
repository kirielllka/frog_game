from game_main.GameDao.ItemsDAO.WeaponsDAO import WeaponsDAO, Weapon_categoryDAO
from game_main.GameDao.BaseDAO import BaseDAO
from models.Items_models.Weapon_models import Weapon_Category,Weapons

WeaponsDAO.create_weapon(type=3,attack=10,critic=1,active=True,frog_id=2,name='wooden sword')