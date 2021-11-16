import random, math

firstCircle = ['Зарплата', 'Возможности', 'Рынок', 'Возможности', 'Безделушки', 'Возможности', 'Благотворительность',
               'Возможности', 'Зарплата', 'Возможности', 'Рынок', 'Возможности', 'Безделушки', 'Возможности',
               'Рождение ребёнка', 'Возможности', 'Зарплата', 'Возможности', 'Рынок', 'Возможности', 'Безделушки',
               'Возможности', 'Увольнение', 'Возможности']


def presentFunc():
    present = (f'Непредвиденные доходы перешло наследство от дальнего родсвенника {math.floor(random.randint(1500, 2500))}',
               f'Непредвиденные доходы была дана премия на работе {math.floor(random.randint(1000, 1500))}')
    return None

def unexpectedExpensesFunc():
    UnexpectedExpenses = (f'(СИ) Непредвиденные расходы вы попали в ДТП -800', f'(СЖ) Непредвиденные расходы вы заболели и попали в больницу -1000')
    rand = random.randint(0, len(UnexpectedExpenses)-1)
    return UnexpectedExpenses[rand]

def bondsFunc():
    bonds = [{'type': 'bonds',
              'name': 'Облигации',
              'price': 1000,
              'passive': 20,
              }
             ]
    rand = random.randint(0, len(bonds) - 1)
    return str(f'Облигации\nЦена %s руб\nПассивный доход %s руб' % (bonds[rand]['price'], bonds[rand]['passive']))

def realEstateFunc():
    realEstate = [{'type': 'realEstate',
                   'name': 'Маленький киоск',
                   'defaultPrice': 100000,
                   'firstInstallment ': 16300,
                   'duty': 76700,
                   'passive': -100,
                   'probabilityOfSale': 14,
                   'ROI': -7.4, }]
    return str('')

def stockMarket():
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
    return str('Акция ' + str(stock[rand]['name']) + '\nЦена: ' + \
               str(stock[rand]['price']) + ' руб\nСправедливая цена: ' \
               + str(stock[rand]['defaultPrice']) + ' руб')


def businessFunc():
    business = [{'type': 'business',
                 'name': 'test1',
                 'startPrice': 19000,
                 'fullPrice': 100000,
                 'passive': 500},
                {'type': 'business2',
                 'name': 'test2',
                 'startPrice': 21000,
                 'fullPrice': 120000,
                 'passive': 700},
                ]
    rand = random.randint(0, len(business) - 1)
    return str(f'Бизнес %s стоимостью %s руб\nСтартовая цена %s руб\nДолг {business[rand]["fullPrice"] - business[rand]["startPrice"]}\nПассивный доход %s руб' % (business[rand]['name'],business[rand]['fullPrice'], business[rand]['startPrice'], business[rand]['passive']))


def businessBigFunc():
    return None

def insuranceFunc():
    mass = ['Страховка 5000']
    return mass[0]

def investmentFunc():
    massnum = [8000,9000,10000,11000,12000]
    randnum = random.randint(0, len(massnum)-1)
    investment = [{'type': 'investment',
                   'name': 'Вексель',
                   'price': massnum[randnum],
                   'defaultPrice': 10000,
                   'passive': 300},
                  ]
    rand = random.randint(0, len(investment) - 1)
    return str('Облигация ' + str(investment[rand]['name']) + '\nЦена: ' + \
               str(investment[rand]['price']) + ' руб\nСправедливая цена: ' \
               + str(investment[rand]['defaultPrice']) + ' руб\nПассивный доход ' + str(investment[rand]['passive']) + ' руб')

def firstCircleFuncStockMarket():
    return [stockMarket(), businessFunc(), businessBigFunc(), realEstateFunc(), bondsFunc(), investmentFunc(),
            unexpectedExpensesFunc(), presentFunc(), insuranceFunc()]


def firstCircleFuncBussines():
    return stockMarket()