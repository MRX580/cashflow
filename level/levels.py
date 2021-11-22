import random
import sqlite3

class Level:
    def __init__(self, moves, income, costs, target, userid):
        self.moves = moves
        self.income = income
        self.costs = costs
        self.target = target
        self.userid = userid

    def insuranceFunc(self):
        mass = ['Страховка 5000']
        return mass[0]

    def work(self):
        num = random.randint(0, 12)
        lvl = ['Первый уровень', 'зарплата']
        works = [['Строитель', 'Менеджер продаж', 'Бариста', 'Продавец-консультант', 'Администратор магазина',
                  'Бармен', 'Банкир', 'Юрист', 'Копирайтер', 'Логопед', 'Системный администратор', 'Социальный педагог','курьер'],
                  [25000, 20000, 11000, 11500, 13000, 11000, 12000, 14000, 14000, 10000, 21500, 8500,16500]
                 ]
        return lvl[0] + ' ' + works[0][num] + ' ' + lvl[1] + ' ' + str(works[1][num])


    def unexpectedExpensesFunc(self):
        UnexpectedExpenses = (f'(СИ) Непредвиденные расходы вы попали в ДТП -800',
                              f'(СЖ) Непредвиденные расходы вы заболели и попали в больницу -1000')
        rand = random.randint(0, len(UnexpectedExpenses) - 1)
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
        return str('Облигация ' + str(investment[rand]['name']) + '\nЦена: ' + str(investment[rand]['price']) + ' руб\nСправедливая цена: ' + str(investment[rand]['defaultPrice']) + ' руб\nПассивный доход ' + str(investment[rand]['passive']) + ' руб')


    def businessFunc(self):
        business = [{'type': 'business',
                     'name': 'AMD',
                     'startPrice': 19000,
                     'fullPrice': 100000,
                     'passive': 500},
                    {'type': 'business',
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
        return str(f'Бизнес %s стоимостью %s руб\nСтартовая цена %s руб\nДолг {business[rand]["fullPrice"] - business[rand]["startPrice"]}\nПассивный доход %s руб' % (business[rand]['name'], business[rand]['fullPrice'], business[rand]['startPrice'],business[rand]['passive']))
    def move_1(self):
        rand = random.randint(1, 4)
        self.work()
        if rand == 1:
            return self.businessFunc()
        if rand == 2:
            return self.investmentFunc()
        if rand == 3:
            return self.stockMarket()
        if rand == 4:
            return self.unexpectedExpensesFunc()
    def database_connect(self):
        self.step = 0
        self.sqlite_select_query = """SELECT * from game"""
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS game(userid INT PRIMARY KEY,move1 TEXT,move2 TEXT,move3 TEXT,step INT, moves INT, income INT, costs INT, target INT);""")
        if self.cur.fetchall() is None:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS game(userid INT PRIMARY KEY,move1 TEXT,move2 TEXT,move3 TEXT,step INT, moves INT, income INT, costs INT, target INT);""")
        self.conn.commit()

    def dataBaseRec(self):
        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            self.cur.execute("INSERT INTO game VALUES(?,?,?,?,?,?,?,?,?);",(self.userid, self.move_1(),self.move_1(),self.move_1(), self.step, self.moves,self.income,self.costs,self.target))
            self.conn.commit()
            self.cur.close()
        except sqlite3.IntegrityError:
            pass

    def dataBaseUpt(self):
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        sqlite_select_query = """SELECT * FROM game"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        for row in records:
            if self.userid:
                self.step = row[4]
            else:
                print('нет такого id')
        self.cur.close()
        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            self.cur.execute(f"""Update game set step = {self.step + 1} where userid = {self.userid}""")
            print(self.step)
            self.conn.commit()
            self.cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if self.conn:
                self.conn.close()
        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * from game")
            if self.userid:
                if self.step == 3:
                    self.step = 1
                    self.cur.execute(f"""Update game set move1 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
            else:
                print('нет такого id')
        except sqlite3.Error as error:
            print(error)
        finally:
            if self.conn:
                self.conn.close()
    def dataBaseMoves(self):
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        sqlite_select_query = """SELECT * FROM game"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        for row in records:
            self.moves = row[5]
            print(self.moves)
        self.cur.close()

        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * from game")
            self.moves = -1
            self.cur.execute(f"""Update game set moves = {self.moves} where userid = {self.userid}""")
            self.conn.commit()
            self.cur.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            if self.conn:
                self.conn.close()

if __name__ == '__main__':
    levelOne = Level(0, 5000, 4000, 50000, 672532296)
    levelOne.database_connect()
    levelOne.move_1()
    levelOne.dataBaseRec()
    levelOne.dataBaseUpt()
    levelOne.dataBaseMoves()