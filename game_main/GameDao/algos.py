

class Algorithms:
    @classmethod
    def point_update(cls,point:int):
        while True:
            try:
                strg = int(input(f'Введите количество камней повышения (у вас есть {point}) '
                                 f'которые вы хотите потратить на силу: '))
                if 0 <= strg <= point:
                    point -= strg
                    break
                else:
                    print('Неверное количество камней. Введите число от 0 до', point)
            except ValueError:
                print('Некорректный ввод. Введите целое число.')

        while True:
            try:
                agl = int(input(f'Введите количество камней повышения (у вас есть {point}) '
                                f'которые вы хотите потратить на ловкость: '))
                if 0 <= agl <= point:
                    point -= agl
                    break
                else:
                    print('Неверное количество камней. Введите число от 0 до', point)
            except ValueError:
                print('Некорректный ввод. Введите целое число.')

        while True:
            try:
                end = int(input(f'Введите количество камней повышения (у вас есть {point}) '
                                f'которые вы хотите потратить на выносливость: '))
                if 0 <= end <= point:
                    point -= end
                    break
                else:
                    print('Неверное количество камней. Введите число от 0 до', point)
            except ValueError:
                print('Некорректный ввод. Введите целое число.')
        return {
            'strg':strg,
            'agl':agl,
            'end':end
        }