from database import session_maker as session

from model import Frog

from .BaseDAO import BaseDAO

from .algos import Algorithms

import random

from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound

class FrogDAO(BaseDAO): #модель со всеми основными функциями
    model = Frog

    @classmethod
    def find_frog_by_name(cls, frog_name: str): #поиск жабы по имени

            query = select(Frog).where(Frog.name == frog_name) #ищем жабу по имени
            result = session.execute(query).scalar_one_or_none() #сохраняем найденный результат
            return result #возвращаем результат

    @classmethod
    def create_frog(cls): #
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
        return {
            'id': frog.id,
            'name': frog.name,
            'lvl': frog.lvl,
            'strengh': frog.strengh,
            'agility': frog.agility,
            'endurance': frog.endurance,
            'atack': frog.atack,
            'health': frog.endurance * 5,
            'damage': frog.atack + frog.strengh,
            'dodge': (frog.agility * 5 // frog.lvl) / 100
        }#

    @classmethod
    def update_atrs(cls, model_id):#
            frog = cls.find_by_id(model=cls.model, model_id=model_id)#
            if frog:#
                result = Algorithms.point_update(point=3)#
                query = (update(Frog).values(strengh=result['strg'] + frog.strengh,
                                            agility=result['agl'] + frog.agility,
                                            endurance=result['end'] + frog.endurance)
                         .where(Frog.id == frog.id))#
                session.execute(query)#
                session.commit()#
            else:#
                print(f'Жаба с ID {model_id} не найдена.')#

    @classmethod
    def lvl_up(cls, frog_id):#
        frog = cls.find_by_id(model=cls.model, model_id=frog_id)[0]#

        choise = input("Вы получили ключ нынешней комнаты, желаете пройти в следующую?\n"
                       "Учтите, что с каждой новой комнатой ваш уровень повышается, и вместе с этим ваши враги становятся сильнее.\n"
                       "Введите 'да' для перехода, 'нет' для отказа: ")#

        if choise.lower() == 'да':#
            lvl = frog.lvl + 1#
            max_lvl = frog.max_lvl + 1#
        else:#
            lvl = frog.lvl#
            max_lvl = frog.max_lvl + 1#

        with session(bind=cls.engine)() as sess:#
            query = update(Frog).where(Frog.id == frog_id).values(lvl=lvl, max_lvl=max_lvl)#
            sess.execute(query)#
            sess.commit()#
    pr
    @classmethod#
    def fight(cls, enemy: dict = None, frog: dict = None):#
        print(f"🐸 {frog}")#

        if frog is None:#
            return None
        if enemy is None:
            if frog['lvl'] < 10:
                probability = 1 // frog['lvl']
            else:
                probability = 3 // frog['lvl']
            super = random.choices([False, True], weights=[1 - probability, probability])[0]
            frog = cls.create_frog_dict(cls.find_frog_by_name(frog_name=frog['name']))
            enemy = {
                'health': frog['lvl'] * 5,
                'damage': frog['lvl'] * 3,
                'super': super
            }

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
            print(f"Ваш шанс уклонения: {frog['dodge']} 💨\n")
            print(f"Здоровье вашего противника: {enemy['health']} из {frog['lvl'] * 5} 💔")
            print(f"Урон вашего противника: {enemy['damage']} 🗡️")

            choise = int(input("Что вы хотите сделать?\n1 - Атаковать ⚔️\n2 - Сбежать 🏃‍♂️\n"))

            match choise:
                case 1:
                    enemy['health'] -= frog['damage']
                    frog['health'] -= enemy['damage']
                    cls.fight(enemy=enemy, frog=frog)
                case 2:
                    print("🏃‍♂️ Вы сбежали! 🏃‍♂️")


