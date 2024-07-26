from database import session_maker as session
from model import Frog

from sqlalchemy import select

from GameDao.FrogDAO import FrogDAO

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
        print('ueeeee')

if __name__ == '__main__':
    main()