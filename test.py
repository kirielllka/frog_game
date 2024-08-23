from game_main.GameDao.ItemsDAO.WeaponsDAO import WeaponsDAO
from game_main.GameDao.BaseDAO import BaseDAO
from models.Items_models.Weapon_models import Weapon_Category,Weapons

from game_main.GameDao.nonname import weapons

import random


def get_random_weapon(weapons):
    total_rare = sum(weapon['rare'] for weapon in weapons.values())
    random_num = random.randint(1, total_rare)

    cumulative_rare = 0
    for weapon_key, weapon_value in weapons.items():
        cumulative_rare += weapon_value['rare']
        if random_num <= cumulative_rare:
            return weapon_key

def test():
    result = []
    wood = 0
    testsw = 0
    for i in range(1000):
        result.append(get_random_weapon(weapons))
    for i in result:
        if i == 'wooden sword':
            wood += 1
        if i == 'test sword':
            testsw +=1
    print(f'wood:{wood}|testsw:{testsw}')

test()
