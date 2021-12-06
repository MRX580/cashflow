import sqlite3, random, string, datetime, level.levels as levels

import assets


class data:
    def __init__(self, userid, column=None, changes=None, userName=None, userFirst=None, userLast=None, money=None):
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
                                   notification BOOLEAN,
                                   credit INT);
                """)
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS buying(
                                    userid INT PRIMARY KEY,
                                    Связьком TEXT,
                                    Нефтехим TEXT,
                                    Инвестбанк TEXT,
                                    Агросбыт TEXT,
                                    Металлпром TEXT,
                                    Bitcoin TEXT,
                                    XRP TEXT,
                                    Avalanche TEXT,
                                    Solana TEXT,
                                    Ethereum TEXT,
                                    Вексель TEXT);
                                """)
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS coins(
                                   userid INT PRIMARY KEY,
                                   coinRand TEXT,
                                   Bitcoin INT,
                                   XRP INT,
                                   Avalanche INT,
                                   Solana INT,
                                   Ethereum INT,
                                   choice TEXT);
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
        step INT, moves INT, income INT, costs INT, target INT, profession TEXT);""")
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS donate(
                                            userid INT PRIMARY KEY,
                                            summ INT,
                                            comment TEXT,
                                            time TEXT);""")
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS insurance(
                                                    userid INT PRIMARY KEY,
                                                    СЖ INT,
                                                    СИ INT);""")
        self.conn.commit()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS bondes(userid INT PRIMARY KEY, Вексель INT, Доход_вексель INT);""")
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS businesses(userid INT PRIMARY KEY, AMD INT, ДоходAMD INT, 
        Intel INT, ДоходIntel, Nvidia INT, ДоходNvidia, Apple INT, ДоходApple INT);""")
        self.conn.commit()

    def dataChangesGame(self):
        self.cur.execute(f"""Update game set {self.column} = {self.changes} where userid = {self.userid}""")
        self.conn.commit()
        self.cur.close()
    def dataChangesCoin(self):
        self.cur.execute(f"""Update coins set {self.column} = (?) where userid = {self.userid}""", (self.changes,))
        self.conn.commit()
        self.cur.close()
    def dataChanges(self):
        self.cur.execute(f"""Update users set {self.column} = {self.changes} where userid = {self.userid}""")
        self.conn.commit()
        self.cur.close()
    def dataChangesInsurance(self):
        self.cur.execute(f"""Update insurance set {self.column} = {self.changes} where userid = {self.userid}""")
        self.conn.commit()
        self.cur.close()

    def donate(self):
        code = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 6))
        self.money = 200
        try:
            self.cur.execute("INSERT INTO donate VALUES(?, ?, ?, ?);",
                             (self.userid, self.money, code, datetime.datetime.now()))
            self.conn.commit()
            return f"К оплате {self.money} грн\nОБЕЗАТЕЛЬНО - к оплате добавьте комментарий {code} без него " \
                   f"покупка не будет совершена\nКомментарий будет действовать сутки после сгенерируйте " \
                   f"новый\nhttps://send.monobank.ua/99NN41RNC8?amount={self.money}&f=enabled&text={code}\nВаш запрос " \
                   f"будет обработан в течении 1 минуты "
        except sqlite3.IntegrityError:
            return f"К оплате {self.dataDonate()[1]} грн\nОБЕЗАТЕЛЬНО - к оплате добавьте комментарий {self.dataDonate()[2]} без него " \
                   f"покупка не будет совершена\nКомментарий будет действовать сутки после сгенерируйте " \
                   f"новый\nhttps://send.monobank.ua/99NN41RNC8?amount={self.dataDonate()[1]}&f=enabled&text=" \
                   f"{self.dataDonate()[2]}\nВаш запрос будет обработан в течении 1 минуты "

    def databaseNewUser(self):
        if self.dataUser() == False:
            try:
                self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                 (self.userid, self.userName, self.userFirst, self.userLast, 2000, False, 1, 0, False, 0, True, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO coins VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(self.userid, assets.assets(self.userid, 0, 0).random_cript(), 0, 0, 0, 0, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO buying VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                 (self.userid, '0 0', '0 0', '0 0', '0 0', '0 0', '0 0', '0 0', '0 0', '0 0', '0 0', '0 0'))
                self.conn.commit()
                self.cur.execute("INSERT INTO stock VALUES(?, ?, ?, ?, ?, ?);",(self.userid, 0, 0, 0, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO insurance VALUES(?, ?, ?);", (self.userid, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO game VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (self.userid, levels.Level(0, 0, 0, 0, self.userid).move_1(),levels.Level(0, 0, 0, 0, self.userid).move_1(), levels.Level(0, 0, 0, 0, self.userid).move_1(), 1, 0, 0, 0, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO bondes VALUES(?, ?, ?);",(self.userid, 0, 0))
                self.conn.commit()
                self.cur.execute("INSERT INTO businesses VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(self.userid, 0, 5000, 0, 7000, 0, 9000, 0, 12000))
                self.conn.commit()
            except sqlite3.IntegrityError as e:
                print(e)
    def dataNewGame(self):
        self.cur.execute(f'Update users set money = 2000 where userid = {self.userid}')
        self.cur.execute(f'Update bondes set Вексель = 0 where userid = {self.userid}')
        self.cur.execute(f'Update bondes set Доход_вексель = 0 where userid = {self.userid}')
        self.cur.execute(f'Update businesses set AMD = 0 where userid = {self.userid}')
        self.cur.execute(f'Update businesses set Intel = 0 where userid = {self.userid}')
        self.cur.execute(f'Update businesses set Nvidia = 0 where userid = {self.userid}')
        self.cur.execute(f'Update businesses set Apple = 0 where userid = {self.userid}')
        self.cur.execute(f'Update coins set Bitcoin = 0 where userid = {self.userid}')
        self.cur.execute(f'Update coins set XRP = 0 where userid = {self.userid}')
        self.cur.execute(f'Update coins set Avalanche = 0 where userid = {self.userid}')
        self.cur.execute(f'Update coins set Solana = 0 where userid = {self.userid}')
        self.cur.execute(f'Update coins set Ethereum = 0 where userid = {self.userid}')
        self.cur.execute(f'Update stock set Связьком = 0 where userid = {self.userid}')
        self.cur.execute(f'Update stock set Нефтехим = 0 where userid = {self.userid}')
        self.cur.execute(f'Update stock set Инвестбанк = 0 where userid = {self.userid}')
        self.cur.execute(f'Update stock set Агросбыт = 0 where userid = {self.userid}')
        self.cur.execute(f'Update stock set Металлпром = 0 where userid = {self.userid}')
        self.cur.execute(f'Update users set levelNow = 0 where userid = {self.userid}')
        self.cur.execute(f'Update users set credit = 0 where userid = {self.userid}')
        self.cur.execute(f'Update insurance set СЖ = 0 where userid = {self.userid}')
        self.cur.execute(f'Update insurance set СИ = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Связьком = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Нефтехим = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Инвестбанк = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Агросбыт = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Металлпром = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Bitcoin = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set XRP = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Avalanche = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Solana = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Ethereum = 0 where userid = {self.userid}')
        self.cur.execute(f'Update buying set Вексель = 0 where userid = {self.userid}')
        self.conn.commit()
    def dataGame(self):
        sqlite_select_query = """SELECT * FROM game"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False

    def dataBuing(self):
        sqlite_select_query = """SELECT * FROM buying"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False

    def dataInsurance(self):
        sqlite_select_query = """SELECT * FROM insurance"""
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
