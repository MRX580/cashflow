import sqlite3
class data:
    def __init__(self, userid, userName, userFirst, userLast):
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
           levelNow INT);
        """)
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


    def databaseNewUser(self):
        try:
            self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?);",
                        (self.userid, self.userName, self.userFirst, self.userLast, 0, False, 1, 0))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
