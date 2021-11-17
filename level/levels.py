import math
import random

class Level:
    def __init__(self, moves, income, costs, target):
        self.moves = moves
        self.income = income
        self.costs = costs
        self.target = target

    def insuranceFunc(self):
        mass = ['Страховка 5000']
        #print(mass)
        return mass[0]


    def work(self):
        num = random.randint(0, 12)
        works = [['Строитель', 'Менеджер продаж', 'Бариста', 'Продавец-консультант', 'Администратор магазина',
                  'Бармен', 'Банкир', 'Юрист', 'Копирайтер', 'Логопед', 'Системный администратор', 'Социальный педагог','курьер'],
                  [25000, 20000, 11000, 11500, 13000, 11000, 12000, 14000, 14000, 10000, 21500, 8500,16500]
                 ]
        #print(works[0][num] + ' ' + str(works[1][num]))
        return works[0][num] + ' ' + str(works[1][num])


    def unexpectedExpensesFunc(self):
        UnexpectedExpenses = (f'(СИ) Непредвиденные расходы вы попали в ДТП -800',
                              f'(СЖ) Непредвиденные расходы вы заболели и попали в больницу -1000')
        rand = random.randint(0, len(UnexpectedExpenses) - 1)
        #print(UnexpectedExpenses[rand])
        return UnexpectedExpenses[rand]


    def stockMarket(self):
        stock = [{'type': 'stock',
                  'name': 'Связьком',
                  'defaultPrice': 100,
                  'price': random.randint(80, 120)},
                 {'type': 'stock',
                  'name': 'Нефтехим',
                  'defaultPrice': 80,
                  'price': random.randint(65, 95)},
                 {'type': 'stock',
                  'name': 'Инвестбанк',
                  'defaultPrice': 40,
                  'price': random.randint(30, 50)},
                 {'type': 'stock',
                  'name': 'Агросбыт',
                  'defaultPrice': 20,
                  'price': random.randint(15, 25)},
                 {'type': 'stock',
                  'name': 'Металлпром',
                  'defaultPrice': 60,
                  'price': random.randint(45, 70)},
                 ]
        rand = random.randint(0, len(stock) - 1)
        #print(str('Акция ' + str(stock[rand]['name']) + '\nЦена: ' + str(stock[rand]['price']) + ' руб\nСправедливая цена: ' + str(stock[rand]['defaultPrice']) + ' руб'))
        return str('Акция ' + str(stock[rand]['name']) + '\nЦена: ' + str(stock[rand]['price']) + ' руб\nСправедливая цена: ' + str(stock[rand]['defaultPrice']) + ' руб')


    def investmentFunc(self):
        massnum = [8000, 9000, 10000, 11000, 12000]
        randnum = random.randint(0, len(massnum) - 1)
        investment = [{'type': 'investment',
                       'name': 'Вексель',
                       'price': massnum[randnum],
                       'defaultPrice': 10000,
                       'passive': 300},
                      ]
        rand = random.randint(0, len(investment) - 1)
        #print(str('Облигация ' + str(investment[rand]['name']) + '\nЦена: ' + str(investment[rand]['price']) + ' руб\nСправедливая цена: ' + str(investment[rand]['defaultPrice']) + ' руб\nПассивный доход ' + str(investment[rand]['passive']) + ' руб'))
        return str('Облигация ' + str(investment[rand]['name']) + '\nЦена: ' + str(investment[rand]['price']) + ' руб\nСправедливая цена: ' + str(investment[rand]['defaultPrice']) + ' руб\nПассивный доход ' + str(investment[rand]['passive']) + ' руб')


    def businessFunc(self):
        business = [{'type': 'business',
                     'name': 'AMD',
                     'startPrice': 19000,
                     'fullPrice': 100000,
                     'passive': 500},
                    {'type': 'business2',
                     'name': 'Intel',
                     'startPrice': 21000,
                     'fullPrice': 120000,
                     'passive': 700},
                    {'type': 'business',
                     'name': 'Nvidia',
                     'startPrice': 25000,
                     'fullPrice': 125000,
                     'passive': 900},
                    {'type': 'business',
                     'name': 'Apple',
                     'startPrice': 35000,
                     'fullPrice': 135000,
                     'passive': 1200}
                    ]
        rand = random.randint(0, len(business) - 1)
        #print(str(f'Бизнес %s стоимостью %s руб\nСтартовая цена %s руб\nДолг {business[rand]["fullPrice"] - business[rand]["startPrice"]}\nПассивный доход %s руб' % (business[rand]['name'], business[rand]['fullPrice'], business[rand]['startPrice'],business[rand]['passive'])))
        return str(f'Бизнес %s стоимостью %s руб\nСтартовая цена %s руб\nДолг {business[rand]["fullPrice"] - business[rand]["startPrice"]}\nПассивный доход %s руб' % (business[rand]['name'], business[rand]['fullPrice'], business[rand]['startPrice'],business[rand]['passive']))



if __name__ == '__main__':
    pass