import random
import sqlite3
import data

class Level:
    def __init__(self, moves = None, income = None, costs = None, target = None, userid = None):
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
        works = ['Строитель', 'Менеджер продаж', 'Бариста', 'Продавец-консультант', 'Администратор магазина',
                  'Бармен', 'Банкир', 'Юрист', 'Копирайтер', 'Логопед', 'Системный администратор', 'Социальный педагог','Курьер']
        dataGame = data.data(self.userid).dataGame()
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute(f"""Update game set profession = (?) where userid = {self.userid}""", (works[num] + ' ' + str(dataGame[6]),))
        conn.commit()

    def writeCosts(self):
        return self.costs

    def writeTarget(self):
        return self.target

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
        mssAssets = [self.stockMarket(), self.investmentFunc(), self.businessFunc(), self.unexpectedExpensesFunc()]
        random.shuffle(mssAssets)
        for i in mssAssets:
            return i
    def database_connect(self):
        self.step = 0
        self.sqlite_select_query = """SELECT * from game"""
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS game(userid INT PRIMARY KEY,move1 TEXT,move2 TEXT,move3 TEXT,step INT, moves INT, income INT, costs INT, target INT, profession TEXT);""")
        if self.cur.fetchall() is None:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS game(userid INT PRIMARY KEY,move1 TEXT,move2 TEXT,move3 TEXT,step INT, moves INT, income INT, costs INT, target INT, profession TEXT);""")
        self.conn.commit()
        self.conn.close()
    def dataBaseRec(self):
        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            self.cur.execute("INSERT INTO game VALUES(?,?,?,?,?,?,?,?,?,?);",(self.userid, self.move_1(),self.move_1(),self.move_1(), self.step,self.moves,self.income,self.costs,self.target, self.work()))
            self.conn.commit()
            self.cur.close()
        except sqlite3.IntegrityError:
            pass
    def dataBaseUpt(self):
        mssAssets = [self.stockMarket(), self.investmentFunc(), self.businessFunc(), self.unexpectedExpensesFunc()]
        random.shuffle(mssAssets)
        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            sqlite_select_query = """SELECT * FROM game"""
            self.cur.execute(sqlite_select_query)
            records = self.cur.fetchall()
            user = data.data(self.userid).dataUser()
            for row in records:
                if user[0] == row[0]:
                    print(row[4])
                    self.step = row[4]

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
            if self.step == 4:
                self.step = 0
                if mssAssets[0] == self.stockMarket() and mssAssets[1] == self.stockMarket() and mssAssets[2] == self.stockMarket() or mssAssets[0] == self.businessFunc() and mssAssets[1] == self.businessFunc() and mssAssets[2] == self.businessFunc() or mssAssets[0] == self.investmentFunc() and mssAssets[1] == self.investmentFunc() and mssAssets[2] == self.investmentFunc() or mssAssets[0] == self.unexpectedExpensesFunc() and mssAssets[1] == self.unexpectedExpensesFunc() and mssAssets[2] == self.unexpectedExpensesFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.stockMarket()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.investmentFunc()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.businessFunc()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.stockMarket() and mssAssets[1] == self.unexpectedExpensesFunc() and mssAssets[2] == self.stockMarket() or mssAssets[0] == self.stockMarket() and mssAssets[1] == self.investmentFunc() and mssAssets[2] == self.stockMarket() or mssAssets[0] == self.stockMarket() and mssAssets[1] == self.stockMarket() and mssAssets[2] == self.investmentFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.businessFunc()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.investmentFunc() and mssAssets[1] == self.investmentFunc() and mssAssets[2] == self.businessFunc() or mssAssets[0] == self.investmentFunc() and mssAssets[1] == self.businessFunc() and mssAssets[2] == self.investmentFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.stockMarket()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.businessFunc() and mssAssets[1] == self.businessFunc() and self.stockMarket() or mssAssets[0] == self.stockMarket() and mssAssets[1] == self.stockMarket() and mssAssets[2] == self.unexpectedExpensesFunc() or mssAssets[0] == self.stockMarket() and mssAssets[1] == self.stockMarket() and mssAssets[2] == self.businessFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.investmentFunc()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.stockMarket() and mssAssets[1] == self.stockMarket() and mssAssets[1] == self.investmentFunc() or mssAssets[0] == self.stockMarket() and mssAssets[1] == self.businessFunc() and mssAssets[1] == self.stockMarket():
                    self.cur.execute(f"""Update game set move1 = "{self.investmentFunc()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.businessFunc() and mssAssets[1] == self.investmentFunc() and mssAssets[2] == self.investmentFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.stockMarket()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.businessFunc() and mssAssets[1] == self.businessFunc() and mssAssets[2] == self.unexpectedExpensesFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.stockMarket()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.investmentFunc() and mssAssets[1] == self.businessFunc() and mssAssets[2] == self.businessFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.stockMarket()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.businessFunc() and mssAssets[1] == self.investmentFunc() and mssAssets[2] == self.investmentFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.stockMarket()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                elif mssAssets[0] == self.businessFunc() and mssAssets[1] == self.stockMarket() and mssAssets[2] == self.businessFunc():
                    self.cur.execute(f"""Update game set move1 = "{self.move_1()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{self.stockMarket()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{self.investmentFunc()}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
                else:
                    self.cur.execute(f"""Update game set move1 = "{mssAssets[0]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{mssAssets[1]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{mssAssets[2]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
                    self.cur.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            if self.conn:
                self.conn.close()

        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        sqlite_select_query = """SELECT * FROM game"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        user = data.data(self.userid).dataUser()
        for row in records:
            if user[0] == row[0]:
                self.step = row[4]
        self.cur.close()
        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            self.cur.execute(f"""Update game set step = {self.step + 1} where userid = {self.userid}""")
            self.conn.commit()
            self.cur.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
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
            row[5] = self.moves
            print(self.moves)
        self.cur.close()

        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * from game")
            self.moves =  -1
            self.cur.execute(f"""Update game set moves = {self.moves} where userid = {self.userid}""")
            self.conn.commit()
            self.cur.close()
        except sqlite3.Error as error:
            print(error)
        finally:
            if self.conn:
                self.conn.close()

if __name__ == '__main__':
    levelOne = Level()
    levelOne.database_connect()
    levelOne.dataBaseRec()
    levelOne.dataBaseUpt()
    levelOne.dataBaseMoves()