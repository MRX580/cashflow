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

    def windfallIncomeFunc(self):
        dataGame = data.data(self.userid).dataGame()
        dataBonds = data.data(self.userid).dataBonds()
        dataBusinesses = data.data(self.userid).dataBusinesses()
        try:
            bussines = (dataBusinesses[1] * dataBusinesses[2]) + (dataBusinesses[3] * dataBusinesses[4]) + (
                    dataBusinesses[5] * dataBusinesses[6]) + (dataBusinesses[7] * dataBusinesses[8])
            windfallIncome = (
                f'(НД) Непредвиденный доход вы заработали денег в казино +{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(НД) Непредвиденный доход вы заработали денег починив соседке раковину +{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(НД) Непредвиденный доход вы заработали денег починив автомобиль +{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(НД) Непредвиденный доход вы заработали денег на подработке охранником +{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(НД) Непредвиденный доход вы заработали денег на продаже напитков +{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(НД) Непредвиденный доход вы заработали денег на творческом конкурсе +{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $'
            )
            rand = random.randint(0, len(windfallIncome) - 1)
            return windfallIncome[rand]
        except Exception as e:
            windfallIncome = (
                f'(НД) Непредвиденный доход вы заработали денег в казино +500 $',
                f'(НД) Непредвиденный доход вы заработали денег в казино +700 $',
                f'(НД) Непредвиденный доход вы заработали денег в казино +900 $',
                f'(НД) Непредвиденный доход вы заработали денег в казино +1200 $',
                f'(НД) Непредвиденный доход вы заработали денег в казино +1400 $',
                f'(НД) Непредвиденный доход вы заработали денег в казино +1600 $'
            )
            rand = random.randint(0, len(windfallIncome) - 1)
            return windfallIncome[rand]

    def unexpectedExpensesFunc(self):
        dataGame = data.data(self.userid).dataGame()
        dataBonds = data.data(self.userid).dataBonds()
        dataBusinesses = data.data(self.userid).dataBusinesses()
        try:
            bussines = (dataBusinesses[1] * dataBusinesses[2]) + (dataBusinesses[3] * dataBusinesses[4]) + (
                        dataBusinesses[5] * dataBusinesses[6]) + (dataBusinesses[7] * dataBusinesses[8])
            UnexpectedExpenses = (
                f'(СИ) Непредвиденные расходы вы попали в ДТП -{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(СЖ) Непредвиденные расходы вы заболели и попали в больницу -{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(СР) Непредвиденные расходы вы дали денег нуждающемуся -{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(СH) Непредвиденные расходы вы уплатили налоги -{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(CК) Непредвиденные расходы вы проиграли деньги в казино -{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $',
                f'(CВ) Непредвиденные расходы вас ограбили -{(int(dataGame[9].split()[-1]) + int(dataBonds[1] * 300 + bussines)) / 10} $'
            )
            rand = random.randint(0, len(UnexpectedExpenses) - 1)
            return UnexpectedExpenses[rand]
        except Exception as e:
            UnexpectedExpenses = (
            f'(СИ) Непредвиденные расходы вы попали в ДТП -500 $',
            f'(СЖ) Непредвиденные расходы вы заболели и попали в больницу -700 $',
            f'(СР) Непредвиденные расходы вы дали денег нуждающемуся -900 $',
            f'(СH) Непредвиденные расходы вы уплатили налоги -1200 $',
            f'(CК) Непредвиденные расходы вы проиграли деньги в казино -1400 $',
            f'(CВ) Непредвиденные расходы вас ограбили -1600 $'
            )
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
        return str('Акция ' + str(stock[rand]['name']) + '\nЦена: ' + str(stock[rand]['price']) + ' $\nСправедливая цена: ' + str(stock[rand]['defaultPrice']) + ' $')


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
        return str('Облигация ' + str(investment[rand]['name']) + '\nЦена: ' + str(investment[rand]['price']) + ' $\nСправедливая цена: ' + str(investment[rand]['defaultPrice']) + ' $\nПассивный доход ' + str(investment[rand]['passive']) + ' $')


    def businessFunc(self):
        business = [{'type': 'business',
                     'name': 'AMD',
                     'startPrice': 19000,
                     'fullPrice': 100000,
                     'passive': 2500},
                    {'type': 'business',
                     'name': 'Intel',
                     'startPrice': 21000,
                     'fullPrice': 110000,
                     'passive': 3500},
                    {'type': 'business',
                     'name': 'Nvidia',
                     'startPrice': 25000,
                     'fullPrice': 125000,
                     'passive': 4000},
                    {'type': 'business',
                     'name': 'Apple',
                     'startPrice': 35000,
                     'fullPrice': 150000,
                     'passive': 5000}
                    ]
        rand = random.randint(0, len(business) - 1)
        return str(f'Бизнес %s стоимостью %s $\nСтартовая цена %s $\nДолг {business[rand]["fullPrice"] - business[rand]["startPrice"]} $\nПассивный доход %s $' % (business[rand]['name'], business[rand]['fullPrice'], business[rand]['startPrice'],business[rand]['passive']))
    def move_1(self):
        dataUser = data.data(self.userid).dataUser()
        dataGame = data.data(self.userid).dataGame()
        if dataUser[7] == 1 and dataGame[5] >= 31:
            mssAssets = [self.stockMarket(), self.stockMarket(), self.stockMarket()]
            rand = random.randint(0, 6)
            if rand >= 5:
                mssAssets[2] = self.unexpectedExpensesFunc()
            for i in mssAssets:
                return i
        elif dataUser[7] == 2 and dataGame[5] >= 32:
            mssAssets = [self.stockMarket(), self.stockMarket(), self.stockMarket()]
            rand = random.randint(0, 6)
            if rand >= 5:
                mssAssets[2] = self.unexpectedExpensesFunc()
            for i in mssAssets:
                return i
        else:
            mssAssets = [self.stockMarket(), self.investmentFunc(), self.businessFunc(), self.unexpectedExpensesFunc(), self.windfallIncomeFunc()]
            random.shuffle(mssAssets)
            rand = random.randint(0, 7)
            if rand >= 5 and mssAssets[0].split()[0].lower() == '(си)' or mssAssets[0].split()[0].lower() == '(сж)' or mssAssets[0].split()[0].lower() == '(ср)' or mssAssets[0].split()[0].lower() == 'сн' or mssAssets[0].split()[0].lower() == 'ск' or mssAssets[0].split()[0].lower() == 'св':
                random.shuffle(mssAssets)
            else:
                pass
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
        while True:
            mssAssets = [self.move_1(), self.move_1(), self.move_1()]
            dataUser = data.data(self.userid).dataUser()
            dataGame = data.data(self.userid).dataGame()
            if not dataUser[7] == 1 and dataGame[5] >= 31:
                if not dataUser[7] == 2 and dataGame[5] >= 32:
                    if mssAssets[0].split()[0] == mssAssets[1].split()[0] and mssAssets[0].split()[0] == mssAssets[2].split()[0] and mssAssets[1].split()[0] == mssAssets[2].split()[0]:
                        random.shuffle(mssAssets)
                    else:
                        break
                else:
                    break
            else:
                break
        try:
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
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if self.conn:
                self.conn.close()

        try:
            self.conn = sqlite3.connect('users.db')
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * from game")
            if not dataUser[7] == 1 and dataGame[5] >= 35 and self.step == 1:
                if not dataUser[7] == 2 and dataGame[5] >= 36 and self.step == 1:
                    pass
                else:
                    self.cur.execute(f"""Update game set move1 = "{mssAssets[0]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{mssAssets[1]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{mssAssets[2]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
            else:
                self.cur.execute(f"""Update game set move1 = "{mssAssets[0]}" where userid = {self.userid}""")
                self.cur.execute(f"""Update game set move2 = "{mssAssets[1]}" where userid = {self.userid}""")
                self.cur.execute(f"""Update game set move3 = "{mssAssets[2]}" where userid = {self.userid}""")
                self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                self.conn.commit()
            if self.step == 4:
                self.step = 0
                print(self.step)
                if not dataUser[7] == 1 and dataGame[5] >= 31:
                    if not dataUser[7] == 2 and dataGame[5] >= 32:
                        if mssAssets[0] == self.unexpectedExpensesFunc() and mssAssets[1] == self.unexpectedExpensesFunc() or mssAssets[1] == self.unexpectedExpensesFunc() and mssAssets[2] == self.unexpectedExpensesFunc() or mssAssets[0] == self.unexpectedExpensesFunc() and mssAssets[2] == self.unexpectedExpensesFunc():
                            self.cur.execute(f"""Update game set move1 = "{self.investmentFunc()}" where userid = {self.userid}""")
                            self.cur.execute(f"""Update game set move2 = "{self.businessFunc()}" where userid = {self.userid}""")
                            self.cur.execute(f"""Update game set move3 = "{self.stockMarket()}" where userid = {self.userid}""")
                            self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                            self.conn.commit()
                        else:
                            self.cur.execute(f"""Update game set move1 = "{mssAssets[0]}" where userid = {self.userid}""")
                            self.cur.execute(f"""Update game set move2 = "{mssAssets[1]}" where userid = {self.userid}""")
                            self.cur.execute(f"""Update game set move3 = "{mssAssets[2]}" where userid = {self.userid}""")
                            self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                            self.conn.commit()
                    else:
                        self.cur.execute(
                            f"""Update game set move1 = "{mssAssets[0]}" where userid = {self.userid}""")
                        self.cur.execute(
                            f"""Update game set move2 = "{mssAssets[1]}" where userid = {self.userid}""")
                        self.cur.execute(
                            f"""Update game set move3 = "{mssAssets[2]}" where userid = {self.userid}""")
                        self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                        self.conn.commit()
                else:
                    self.cur.execute(f"""Update game set move1 = "{mssAssets[0]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move2 = "{mssAssets[1]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set move3 = "{mssAssets[2]}" where userid = {self.userid}""")
                    self.cur.execute(f"""Update game set step = {self.step} where userid = {self.userid}""")
                    self.conn.commit()
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
            if self.userid == row[0]:
                self.moves = row[5]
        self.cur.close()

        try:
            for row in records:
                if self.userid == row[0]:
                    self.conn = sqlite3.connect('users.db')
                    self.cur = self.conn.cursor()
                    self.cur.execute("SELECT * from game")
                    self.moves += -1
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