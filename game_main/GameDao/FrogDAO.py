from database import session_maker as session

from model import Frog



from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound

class FrogDAO:
    @classmethod
    def find_frog_by_name(cls, frog_name: str):
        query = select(Frog).where(Frog.name == frog_name)
        try:
            result = session().execute(query).scalar_one()
            return result
        except NoResultFound:
            return None

    @classmethod
    def create_frog(cls):
        cur_atr = 10
        frog_name = input('Введите имя вашей жабы:')

        while True:
            try:
                strg = int(input(f'Введите количество камней повышения (у вас есть {cur_atr}) '
                                 f'которые вы хотите потратить на силу: '))
                if 0 <= strg <= cur_atr:
                    cur_atr -= strg
                    break
                else:
                    print('Неверное количество камней. Введите число от 0 до', cur_atr)
            except ValueError:
                print('Некорректный ввод. Введите целое число.')

        while True:
            try:
                agl = int(input(f'Введите количество камней повышения (у вас есть {cur_atr}) '
                                f'которые вы хотите потратить на ловкость: '))
                if 0 <= agl <= cur_atr:
                    cur_atr -= agl
                    break
                else:
                    print('Неверное количество камней. Введите число от 0 до', cur_atr)
            except ValueError:
                print('Некорректный ввод. Введите целое число.')

        while True:
            try:
                end = int(input(f'Введите количество камней повышения (у вас есть {cur_atr}) '
                                f'которые вы хотите потратить на выносливость: '))
                if 0 <= end <= cur_atr:
                    cur_atr -= end
                    break
                else:
                    print('Неверное количество камней. Введите число от 0 до', cur_atr)
            except ValueError:
                print('Некорректный ввод. Введите целое число.')

        new_frog = Frog(
            name=frog_name,
            strengh=strg,
            agility=agl,
            endurance=end
        )
        session().add(new_frog)
        session().commit()
        session().close()