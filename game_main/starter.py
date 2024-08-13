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
        choise = int(input('1 для исследования \n 2 просмотр жабы'))
        match choise:
            case 1:
                FrogDAO.fight(frog=FrogDAO.create_frog_dict(frog=frog))
            case 2:
                FrogDAO.print_frog_stats(frog_stats=FrogDAO.create_frog_dict(frog=frog))
if __name__ == '__main__':
    main()