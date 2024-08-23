from math import trunc

import sqlalchemy

from .nonname import weapons

from database import session_maker

from models.Frog_models import Frog
from models.Items_models.Weapon_models import Weapons

from .ItemsDAO.WeaponsDAO import WeaponsDAO
from .BaseDAO import BaseDAO

from .algos import Algorithms

import random

from sqlalchemy import select, insert, update
{'wooden sword': 80,
 'test sword': 20,
 }

class FrogDAO(BaseDAO): #модель со всеми основными функциями
    model = Frog

    @classmethod
    def find_frog_by_name(cls, frog_name: str): #поиск жабы по имени
            session = session_maker()
            query = select(Frog).where(Frog.name == frog_name) #ищем жабу по имени
            result = session.execute(query)#сохраняем найденный результат
            try:

                return result.fetchall()[0] #возвращаем результат

            except IndexError:
                return None

    @classmethod
    def create_frog(cls):
        session = session_maker()
        frog_name = input('Введите имя вашей жабы:')#
        if cls.find_frog_by_name(frog_name=frog_name):#
            print('Жаба с таким именем уже существует')#
            cls.create_frog()#
            return None
        atrs = Algorithms.point_update(10)#
        query = insert(Frog).values(name=frog_name, strengh=atrs['strg'],
                                    agility=atrs['agl'], endurance=atrs['end'])#
        session.execute(query)#
        session.commit()#

    @classmethod
    def create_frog_dict(cls, frog:Frog):
        if isinstance(frog,sqlalchemy.engine.row.Row):
            frog = frog[0]
        frog = BaseDAO.find_by_id(model_id=frog.id, model=Frog)[0]
        if frog:
            weapon = WeaponsDAO.find_active(frog_id=frog.id)[0]
            if weapon:
                weapon_name = weapon.name
            else:
                weapon_name = "No Weapon"
            return {
                'id': frog.id,
                'name': frog.name,
                'lvl': frog.lvl,
                'strengh': frog.strengh,
                'agility': frog.agility,
                'endurance': frog.endurance,
                'weapon': weapon_name,
                'critical': int(
                    (frog.agility * 0.5) + (frog.strengh * 0.3) - (frog.max_lvl * 0.1) * 1.5 + weapon.critic),
                'atack': frog.atack + weapon.attack,
                'health': frog.endurance * 5,
                'damage': frog.atack + frog.strengh + weapon.attack,
                'dodge': Algorithms.calculate_dodge_chance(agility=frog.agility, player_level=frog.max_lvl)
            }
        else:
            return None  # Handle cases where the frog isn't found

    @classmethod
    def update_atrs(cls, model_id):#
            session = session_maker()
            frog = cls.find_by_id(model=cls.model, model_id=model_id)[0]#
            if frog:
                result = Algorithms.point_update(point=3)#
                BaseDAO.update(model=Frog, model_id=model_id, data={'strengh':result['strg'] + frog.strengh,
                                                                    'agility':result['agl'] + frog.agility,
                                                                    'endurance':result['end'] + frog.endurance})
            else:#
                print(f'Жаба с ID {model_id} не найдена.')#

    @classmethod
    def lvl_up(cls, frog_id):#
        session = session_maker()
        frog = cls.find_by_id(model=cls.model, model_id=frog_id)[0]#

        choise = input("Вы получили ключ нынешней комнаты, желаете пройти в следующую?\n"
                       "Учтите, что с каждой новой комнатой ваш уровень повышается, и вместе с этим ваши враги становятся сильнее.\n"
                       "Введите 'да' для перехода, 'нет' для отказа: ")#
        cls.update_atrs(model_id=frog_id)
        if choise.lower() == 'да':#
            lvl = frog.lvl + 1#
            max_lvl = frog.max_lvl + 1#
        else:#
            lvl = frog.lvl#
            max_lvl = frog.max_lvl + 1#

        BaseDAO.update(model=Frog, model_id=frog_id, data={'lvl':lvl,'max_lvl':max_lvl})

    @classmethod
    def fight(cls, enemy: dict = None, frog: dict = None):
        if frog is None:
            return None
        if enemy is None:
            if frog['lvl'] < 10:
                probability = 1 / frog['lvl']
            else:
                probability = 3 // frog['lvl']

            super = random.random() < 1-probability
            frog = cls.create_frog_dict(cls.find_frog_by_name(frog_name=frog['name']))
            enemy_health = random.randint(round(frog['lvl'] * 7 * 0.8), round(frog['lvl'] * 7 * 2))
            enemy = {
                'health': enemy_health,
                'damage': random.randint(round(frog['lvl'] * 3 * 0.8), round(frog['lvl'] * 3 * 1.2)),
                'super': super,
                'max_health': enemy_health
            }

        critical_probability = frog['critical'] / 100

        dodge_probability = frog['dodge'] / 100

        if random.random() < critical_probability:
            damage = random.randint(trunc(frog['damage'] * 0.8), trunc(frog['damage'] * 1.2)) * 1.5
            dmg_text = f'Вы нанесли {damage}⚔️ критического урона 💥'
        else:
            damage = random.randint(trunc(frog['damage'] * 0.8), trunc(frog['damage'] * 1.2)) * 1.5
            dmg_text = f'Вы нанесли {damage}⚔️ урона'

        damage_enemy = random.randint(trunc(enemy['damage'] * 0.8), trunc(enemy['damage'] * 1.2))

        if enemy['health'] <= 0:
            if enemy['super']:
                print("🏆 Вы победили противника! 🏆")
                cls.lvl_up(frog_id=frog['id'])
                frog.clear()
                enemy.clear()
                return None
            else:
                print("🎉 Вы победили противника! 🎉")
                return None

        if frog['health'] <= 0:
            print("💀 Вы пали от рук врага! 💀")
            frog.clear()
            enemy.clear()
        else:
            print(f"Ваше здоровье: {frog['health']} из {frog['lvl'] * 5} 💚")
            print(f"Ваш урон: {frog['damage']} ⚔️")
            print(f"Ваш шанс уклонения: {frog['dodge']}% 💨\n")
            print(f"Здоровье вашего противника: {enemy['health']} из {enemy['max_health']} 💔")
            print(f"Урон вашего противника: {enemy['damage']} 🗡️")

            choise = int(input("Что вы хотите сделать?\n1 - Атаковать ⚔️\n2 - Сбежать 🏃‍♂️\n"))

            match choise:
                case 1:
                    if not random.random() < dodge_probability:
                        frog['health'] -= damage_enemy
                        en_dmg_txt = f'Ваш враг нанес {damage_enemy}⚔️ урона '
                    else:
                        en_dmg_txt = 'Ваш противник промахнулся'

                    enemy['health'] -= damage

                    print(dmg_text)
                    print(en_dmg_txt)
                    cls.fight(enemy=enemy, frog=frog)
                case 2:
                    print("🏃‍♂️ Вы сбежали! 🏃‍♂️")

    @classmethod
    def weapon_activate_list(cls, frog_id):
        weapons = BaseDAO.find_all(Weapons)
        for weapon_index in range(len(weapons)):
            print(f'{weapon_index+1}. {weapons[weapon_index].name}')
        choise = int(input('Выберете оружие которое хотите использовать, или 0 для отмены:'))
        if choise == 0:
            return None
        else:
            weapon = weapons[choise-1]
            Algorithms.print_weapon_stats(weapon)
            choise = input(f'Вы уверены что хотите использовать {weapon.name}:')
            if choise.lower() == 'да':
                WeaponsDAO.switch_active(weapon_id=weapon.id)
            if choise.lower() == 'нет':
                cls.weapon_activate_list(frog_id=frog_id)


    @classmethod
    def find_chest_weapon(cls, frog_dict):

        empty_chest_chance = 0.2

        if random.random() < empty_chest_chance:
            print("😔 Вы нашли сундук, но он пуст...")
            return

        print("✨ Вы наткнулись на сундук! ✨")
        print("🎁 Вы хотите его открыть? 🎁")
        print("1 - Открыть 🔑")
        print("2 - Оставить 🚪")

        choice = input("Ваш выбор: ")

        if choice == "1":
            random_weapon_name = Algorithms.get_random_weapon(weapons)
            weapon_data = weapons[random_weapon_name]

            new_weapon = Weapons(
                name=random_weapon_name,
                type=weapon_data['type'],
                attack=weapon_data['attack'],
                critic=weapon_data['critic'],
                active=False,
                frog_id=frog_dict['id']
            )

            session = session_maker()
            session.add(new_weapon)
            session.commit()
            session.close()

            print(f"🎉 Вы получили {random_weapon_name}! 🎉")
        elif choice == "2":
            print("🚪 Вы решили оставить сундук на потом. 🚪")
        else:
            print("Некорректный выбор. ❌")




    @classmethod
    def delete_item_from_inv(cls, frog_id):
        weapons = BaseDAO.find_all(Weapons)
        for weapon_index in range(len(weapons)):
            print(f'{weapon_index+1}. {weapons[weapon_index].name}')
        choise = int(input('Выберете вещь которую хотите выбросить, или 0 для отмены:'))
        if choise == 0:
            return None
        else:
            weapon = weapons[choise-1]
            Algorithms.print_weapon_stats(weapon)
            choise = input(f'Вы уверены что хотите выбросить {weapon.name}:')
            if choise.lower() == 'да':
                BaseDAO.delete(Weapons,model_id=weapon.id)
            if choise.lower() == 'нет':
                cls.delete_item_from_inv()







