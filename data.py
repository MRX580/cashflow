import sqlite3
class data:
    def __init__(self, userid, userName = None, userFirst = None, userLast = None):
        self.userid = userid
        self.userName = userName
        self.userFirst = userFirst
        self.userLast = userLast


    def database_connect(self):
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
        self.conn.commit()
        print('Database connected')


    def dataUser(self):
        self.database_connect()
        sqlite_select_query = """SELECT * FROM users"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        print(record)
        for i in record:
            if i[0] == self.userid:
                return i
        return False


    def databaseNewUser(self):
        self.database_connect()
        if self.dataUser() == False:
            try:
                self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",
                            (self.userid, self.userName, self.userFirst, self.userLast, 0, False, 1, 0, False))
                self.cur.execute("INSERT INTO kripta VALUES(?, ?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 0, 0))
                self.cur.execute("INSERT INTO stock VALUES(?, ?, ?, ?, ?, ?);",
                                 (self.userid, 0, 0, 0, 0, 0))
                self.conn.commit()
            except sqlite3.IntegrityError:
                pass
