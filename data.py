import sqlite3, random, string, datetime
class data:
    def __init__(self, userid, column = None, changes = None, userName = None, userFirst = None, userLast = None, money = None):
        self.userid = userid
        self.userName = userName
        self.userFirst = userFirst
        self.userLast = userLast
        self.column = column
        self.money = money
        self.changes = changes
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                   userid INT PRIMARY KEY,
                                   username TEXT,
                                   fname TEXT,
                                   lname TEXT,
                                   money INT,
                                   isgame BOOLEAN,
                                   levelOpen INT,
                                   levelNow INT,
                                   premium BOOLEAN,
                                   donate INT,
                                   notification BOOLEAN);
                """)
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS coins(
                                   userid INT PRIMARY KEY,
                                   btc INT,
                                   bnb INT,
                                   avax INT,
                                   sol INT,
                                   eth INT);
                                """)
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS stock(
                                   userid INT PRIMARY KEY,
                                   Связьком INT,
                                   Нефтехим INT,
                                   Инвестбанк INT,
                                   Агросбыт INT,
                                   Металлпром INT);""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS game(userid INT PRIMARY KEY,move1 TEXT,move2 TEXT,move3 TEXT,
        step INT, moves INT, income INT, costs INT, target INT);""")
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS donate(
                                            userid INT PRIMARY KEY,
                                            summ INT,
                                            comment TEXT,
                                            time TEXT);""")
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS bondes(userid INT PRIMARY KEY, Вексель INT, Доход_вексель INT);""")
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS businesses(userid INT PRIMARY KEY, AMD INT, ДоходAMD INT, 
        Intel INT, ДоходIntel, Nvidia INT, ДоходNvidia, Apple INT, ДоходApple INT);""")
        self.conn.commit()

    def dataChanges(self):
        self.cur.execute(f"""Update users set {self.column} = {self.changes} where userid = {self.userid}""")
        self.conn.commit()
        self.cur.close()


    def donate(self):
        code = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 6))
        try:
            self.cur.execute("INSERT INTO donate VALUES(?, ?, ?, ?);",
                             (self.userid, self.money, code, datetime.datetime.now()))
            self.conn.commit()
            return f"К оплате {self.money} грн\nОБЕЗАТЕЛЬНО - к оплате добавьте комментарий {code} без него " \
                   f"покупка не будет совершена\nКомментарий будет действовать сутки после сгенерируйте " \
                   f"новый\nhttps://send.monobank.ua/2nyBFqiKgz?amount={self.money}&f=enabled&text={code}\nВаш запрос " \
                   f"будет обработан в течении 1 минуты "
        except sqlite3.IntegrityError:
            return f"К оплате {self.dataDonate()[1]} грн\nОБЕЗАТЕЛЬНО - к оплате добавьте комментарий {self.dataDonate()[2]} без него " \
                   f"покупка не будет совершена\nКомментарий будет действовать сутки после сгенерируйте " \
                   f"новый\nhttps://send.monobank.ua/2nyBFqiKgz?amount={self.dataDonate()[1]}&f=enabled&text=" \
                   f"{self.dataDonate()[2]}\nВаш запрос будет обработан в течении 1 минуты "

    def databaseNewUser(self):
        if self.dataUser() == False:
            try:
                self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (self.userid, self.userName, self.userFirst, self.userLast, 0, False, 1, 0, False, 0, True))
                self.conn.commit()
                self.cur.execute("INSERT INTO coins VALUES(?, ?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO stock VALUES(?, ?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO game VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 3, 0, 0, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO bondes VALUES(?, ?, ?);",
                                (self.userid, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO businesses VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 0, 0, 0, 0, 0))
                self.conn.commit()
            except sqlite3.IntegrityError as e:
                print(e)


    def dataGame(self):
        sqlite_select_query = """SELECT * FROM game"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False


    def dataDonate(self):
        sqlite_select_query = """SELECT * FROM donate"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False

    def dataUser(self):
        sqlite_select_query = """SELECT * FROM users"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False


    def dataStock(self):
        sqlite_select_query = """SELECT * FROM stock"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False


    def dataBonds(self):
        sqlite_select_query = """SELECT * FROM bondes"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False


    def dataCoins(self):
        sqlite_select_query = """SELECT * FROM coins"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False


    def dataBusinesses(self):
        sqlite_select_query = """SELECT * FROM businesses"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False

if __name__ == "__main__":
    data(0)