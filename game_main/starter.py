from GameDao.FrogDAO import FrogDAO
from game_main.GameDao.BaseDAO import BaseDAO
from model import Frog
def main():
    frog_name = input('Enter frog name:')
    frog = FrogDAO.find_frog_by_name(frog_name=frog_name)
    if frog is None:
        print('Такой жабы не существует :(')
        choise = input('Хотите создать новую?')
        if choise.lower() == 'нет':
            main()
        if choise.lower() == 'да':
            FrogDAO.create_frog()

    while True:
        choise = int(input('1 для исследования'))
        FrogDAO.fight(frog=FrogDAO.create_frog_dict(BaseDAO.find_by_id(model_id=3, model=Frog)[0]))

if __name__ == '__main__':
    main()