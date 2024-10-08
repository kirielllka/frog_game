from math import trunc
from database import session_maker

from models.Frog_models import Frog
from models.Items_models.Weapon_models import Weapons

from .BaseDAO import BaseDAO

from .algos import Algorithms

import random

from sqlalchemy import select, insert, update


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
            return
        atrs = Algorithms.point_update(10)#
        query = insert(Frog).values(name=frog_name, strengh=atrs['strg'],
                                    agility=atrs['agl'], endurance=atrs['end'])#
        session.execute(query)#
        session.commit()#

    @classmethod
    def create_frog_dict(cls, frog: Frog):#
        frog = frog[0]
        weapon = session_maker().query(Weapons).filter(Weapons.frog_id == frog.id, Weapons.active == True)[0]
        print(weapon.name)
        return {
            'id': frog.id,
            'name': frog.name,
            'lvl': frog.lvl,
            'strengh': frog.strengh,
            'agility': frog.agility,
            'endurance': frog.endurance,
            'weapon': weapon.name,
            'critical': int((frog.agility * 0.5) + (frog.strengh * 0.3) - (frog.max_lvl * 0.1) * 1.5 + weapon.critic),
            'atack': frog.atack+weapon.attack,
            'health': frog.endurance * 5,
            'damage': frog.atack + frog.strengh+weapon.attack,
            'dodge': cls.calculate_dodge_chance(agility=frog.agility,player_level=frog.max_lvl)
        }#

    @classmethod
    def update_atrs(cls, model_id):#
            session = session_maker()
            frog = cls.find_by_id(model=cls.model, model_id=model_id)[0]#
            if frog:#
                result = Algorithms.point_update(point=3)#
                query = (update(Frog).values(strengh=result['strg'] + frog.strengh,
                                            agility=result['agl'] + frog.agility,
                                            endurance=result['end'] + frog.endurance).where(Frog.id == frog.id))#
                session.execute(query)#
                session.commit()#
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

        query = update(Frog).where(Frog.id == frog_id).values(lvl=lvl, max_lvl=max_lvl)#
        session.execute(query)#
        session.commit()#

    @classmethod
    def fight(cls, enemy: dict = None, frog: dict = None):
        # print(f"🐸 {frog}")
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
                'super': super,  # Get the actual boolean value from the list
                'max_health': enemy_health
            }

        # Critical hit probability (convert percentage to decimal)
        critical_probability = frog['critical'] / 100

        # Dodge probability (convert percentage to decimal)
        dodge_probability = frog['dodge'] / 100

        # Calculate Damage
        if random.random() < critical_probability:
            damage = random.randint(trunc(frog['damage'] * 0.8), trunc(frog['damage'] * 1.2)) * 1.5
            dmg_text = f'Вы нанесли {damage}⚔️ критического урона 💥'
        else:
            damage = random.randint(trunc(frog['damage'] * 0.8), trunc(frog['damage'] * 1.2)) * 1.5
            dmg_text = f'Вы нанесли {damage}⚔️ урона'

        damage_enemy = random.randint(trunc(enemy['damage'] * 0.8), trunc(enemy['damage'] * 1.2))

        # Check for Win/Loss
        if enemy['health'] <= 0:
            if enemy['super']:  # Check if super is True
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
    def calculate_dodge_chance(cls,agility, player_level):
        base_chance = agility * 0.5
        dodge_chance = min(base_chance, 60)  # Шанс уклонения не может быть больше 60%
        dodge_chance -= player_level * 0.1  # Уменьшение шанса уклонения при повышении уровня игрока
        return dodge_chance

    @classmethod
    def print_frog_stats(cls, frog_stats: dict):
        print("🐸  Характеристики вашей жабы  🐸")
        print("-" * 30)
        print(f"Имя: {frog_stats['name']}")
        print(f"Уровень: {frog_stats['lvl']}")
        print(f"Сила: {frog_stats['strengh']} 💪")
        print(f"Ловкость: {frog_stats['agility']} 💨")
        print(f"Выносливость: {frog_stats['endurance']} 🐢")
        print(f'Оружие: {frog_stats['weapon']}')
        print(f'Критический шанс: {frog_stats['critical']}% 💥')
        print(f"Атака: {frog_stats['atack']} ⚔️")
        print(f"Здоровье: {frog_stats['health']} ❤️")
        print(f"Урон: {frog_stats['damage']} 💢")
        print(f"Шанс уклонения: {frog_stats['dodge']:.2f}% 🤸‍♂️")
        print("-" * 30)






