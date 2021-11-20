import sqlite3
class data:
    def __init__(self, userid, column = None, changes = None, userName = None, userFirst = None, userLast = None):
        self.userid = userid
        self.userName = userName
        self.userFirst = userFirst
        self.userLast = userLast
        self.column = column
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
                                   premium BOOLEAN);
                """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS kripta(
                                   userid INT PRIMARY KEY,
                                   btc INT,
                                   bnb INT,
                                   avax INT,
                                   sol INT,
                                   eth INT);
                                """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS stock(
                                   userid INT PRIMARY KEY,
                                   Связьком INT,
                                   Нефтехим INT,
                                   Инвестбанк INT,
                                   Агросбыт INT,
                                   Металлпром INT);""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS game(
                                    userid INT PRIMARY KEY,
                                    move1 TEXT,
                                    move2 TEXT,
                                    move3 TEXT,
                                    step INT);""")
        self.conn.commit()


    def dataChanges(self):
        self.cur.execute(f"""Update users set {self.column} = {self.changes} where userid = {self.userid}""")
        self.conn.commit()
        self.cur.close()


    def dataUser(self):
        sqlite_select_query = """SELECT * FROM users"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False


    def databaseNewUser(self):
        if self.dataUser() == False:
            try:
                self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (self.userid, self.userName, self.userFirst, self.userLast, 0, False, 1, 0, False))
                self.cur.execute("INSERT INTO kripta VALUES(?, ?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 0, 0))
                self.cur.execute("INSERT INTO stock VALUES(?, ?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 0, 0))
                self.cur.execute("INSERT INTO game VALUES(?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 3))
                self.conn.commit()
            except sqlite3.IntegrityError:
                pass


    def dataGame(self):
        sqlite_select_query = """SELECT * FROM game"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
        return False