from .nonname import weapons
import random

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

    @classmethod
    def calculate_dodge_chance(cls, agility, player_level):
        base_chance = agility * 0.5
        dodge_chance = min(base_chance, 60)  # Шанс уклонения не может быть больше 60%
        dodge_chance -= player_level * 0.1  # Уменьшение шанса уклонения при повышении уровня игрока
        return dodge_chance

    def get_random_weapon(weapons):
        total_rare = sum(weapon['rare'] for weapon in weapons.values())
        random_num = random.randint(1, total_rare)

        cumulative_rare = 0
        for weapon_key, weapon_value in weapons.items():
            cumulative_rare += weapon_value['rare']
            if random_num <= cumulative_rare:
                return weapon_key

    @classmethod
    def print_weapon_stats(cls, weapon):
        print("⚔️  Характеристики оружия  ⚔️")
        print("-" * 30)
        print(f"Название: {weapon.name}")
        print(f"Тип: {weapon.type} 🗡️")
        print(f"Атака: {weapon.attack} 💪")
        print(f"Критический урон: {weapon.critic}% 💥")
        print("-" * 30)

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