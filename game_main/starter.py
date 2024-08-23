from GameDao.FrogFunc import FrogDAO, Algorithms

def main():
    frog_name = input('Enter frog name:')
    frog = FrogDAO.find_frog_by_name(frog_name=frog_name)[0]
    if frog is None:
        print('Такой жабы не существует :(')
        choise = input('Хотите создать новую?')
        if choise.lower() == 'нет':
            main()
        if choise.lower() == 'да':
            FrogDAO.create_frog()

    while True:
        choise = int(input('1 для исследования \n2 меню'))
        match choise:
            case 1:
                # FrogDAO.fight(frog=FrogDAO.create_frog_dict(frog=frog))
                FrogDAO.find_chest_weapon(frog_dict=FrogDAO.create_frog_dict(frog=frog))
            case 2:
                chois = int(input('\t1 посмотреть жабу \n\t2 сменить оружие \n\t3 выкинуть вещь'))
                match chois:
                    case 1:
                        Algorithms.print_frog_stats(frog_stats=FrogDAO.create_frog_dict(frog=frog))
                    case 2:
                        FrogDAO.weapon_activate_list(frog_id=frog.id)
                    case 3:
                        FrogDAO.delete_item_from_inv(frog_id=frog.id)
if __name__ == '__main__':
    main()