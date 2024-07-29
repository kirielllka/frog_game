from database import session_maker as session

from model import Frog

from .BaseDAO import BaseDAO

from .algos import Algorithms

import random

from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound

class FrogDAO(BaseDAO):
    model = Frog
    @classmethod
    def find_frog_by_name(cls, frog_name: str):
        query = select(Frog).where(Frog.name == frog_name)
        try:
            result = session().execute(query).scalar_one()
            session().close()
            return result

        except NoResultFound:
            return None


    @classmethod
    def create_frog(cls):
        cur_atr = 10
        frog_name = input('Введите имя вашей жабы:')
        if cls.find_frog_by_name(frog_name=frog_name) is None:
            atrs = Algorithms.point_update(10)
            query = insert(Frog).values(name=frog_name, strengh=atrs['strg'],
                                        agility=atrs['agl'], endurance=atrs['end'])
            session_instance = session()
            session_instance.execute(query)
            session_instance.commit()
            session_instance.close()
        else:
            print('Жаба с таким именем уже существует')
            cls.create_frog()

    @classmethod
    def create_frog_dict(cls,frog:Frog):
        return {
            'id': frog.id,
            'name': frog.name,
            'lvl': frog.lvl,
            'strengh': frog.strengh,
            'agility': frog.agility,
            'endurance': frog.endurance,
            'atack': frog.atack,
            'health': frog.endurance*5,
            'damage':frog.atack+frog.strengh,
            'dodge':(frog.agility*5//frog.lvl)/100
        }

    @classmethod
    def update_atrs(cls, model_id):
        frog = cls.find_by_id(model=cls.model, model_id=model_id)[0]
        result = Algorithms.point_update(point=3)
        session_inst = session()
        query = update(Frog).values(update_point=0, strengh=result['strg']+frog.strengh, agility=result['agl']+frog.agility,
                                    endurance=result['end']+frog.endurance).where(Frog.id == frog.id)
        session_inst.execute(query)
        session_inst.commit()
        session_inst.close()
    @classmethod
    def lvl_up(cls,frog_id):
        frog = cls.find_by_id(model=cls.model, model_id=frog_id)[0]
        choise = input('Вы получили ключ нынешней комнаты, желаете пройти в следующую?Учтите что с каждой новой комнатой ваш '
                       'уровень повышается и вместе с этим ваши враги становятся сильнее.')


        if choise.lower() == 'да':
            lvl = frog.lvl + 1
            max_lvl = frog.max_lvl + 1
        else:
            lvl = frog.lvl
            max_lvl = frog.max_lvl+1
        sess = session()
        query = update(Frog).values(lvl=lvl,max_lvl=max_lvl)
        cls.update_atrs(model_id=frog_id)
        sess.execute(query)
        sess.commit()
        sess.close()


    @classmethod
    def fight(cls,enemy:dict=None,frog:dict=None,):
        print(frog)

        if frog is None:
            return None
        if enemy is None:
            if frog['lvl'] < 10:
                probability = 1//frog['lvl']
            else:
                probability = 3//frog['lvl']
            super = random.choices([False, True], weights=[1 - probability, probability])[0]
            frog = cls.create_frog_dict(cls.find_frog_by_name(frog_name=frog['name']))
            enemy = {
                'health': frog['lvl'] * 5,
                'damage': frog['lvl'] * 3,
                'super':super
            }
        if enemy['health'] <= 0:
            if enemy['super']:
                print('Вы победили противника')
                cls.lvl_up(frog_id=frog['id'])
                frog.clear()
                enemy.clear()
                return None
            else:
                print('Вы победили противника')
                return None
        if frog['health'] <= 0:
            print('Вы пали от рук врага')
            frog.clear()
            enemy.clear()
        else:
            print(f'Ваше здоровье:{frog['health']} из {frog['lvl']*5}'
                  f'Ваш урон:{frog['damage']}'
                  f'Ваш шанс уклонения:{frog['dodge']}\n'
                  f'Здоровье вашего противника:{enemy['health']} из {frog['lvl']*5}'
                  f'Урон вашего противника:{enemy['damage']}')
            choise = int(input('Вы можете сбежать если нажмете 2 или атаковать если нажмете 1'))
            match choise:
                case 1:
                    enemy['health']-=frog['damage']
                    frog['health']-=enemy['damage']
                    cls.fight(enemy=enemy,frog=frog)
                case 2:
                    print('Вы сбежали')


