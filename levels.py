import random

class Level:
    def profession(self):
        num = random.randint(0, 11)
        Professions = [
            ['Стройщик', 'Менеджер продаж', 'Бариста', 'Продавец-консультант', 'Администратор магазина',
            'Бармен', 'Банкир', 'Юрист', 'Копирайтер', 'Логопед', 'Системный администратор', 'Педагог'],
                  [25000, 20000, 15000, 18000, 17000, 19000, 23000, 22000, 20000, 16000, 17000, 21000]
        ]
        return Professions[0][num] + ' ' + str(Professions[1][num])
    def lvl_user(self):
        mssLevel = [1,2]
        level = 0
        if level == 108:
            print(f"Ваш уровень: {mssLevel[0]}")


Level().lvl_user()

