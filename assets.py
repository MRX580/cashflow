import random, sqlite3, data


class assets:
    def __init__(self, userid, kripta, colvo, price):
        self.userid = userid
        self.kripta = kripta
        self.colvo = colvo
        self.price = price
        data.data(0, 0, 0, 0).database_connect()
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.conn.commit()
        print('Database connected')

    def random_cript(self):
        btc_price = random.randint(54000, 64000)
        bnb_price = random.randint(450, 540)
        avax_price = random.randint(80, 102)
        sol_price = random.randint(150, 197)
        eth_price = random.randint(3950, 4022)
        return 'Выбери крипту:\n1.Bitcoin ' + str(btc_price) + '$\n2.Binance Coin' + str(
            bnb_price) + '$\n3.Avalanche' + str(avax_price) + '$\n4.Solana' + str(sol_price) + '$\n5.Ethereum' + str(
            eth_price) + '$'

    def kriptaUser(self):
        sqlite_select_query = """SELECT * FROM kripta"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i

    # МОЙ КОД -------------------------------

    def database_user_stock(self):
        self.cur.execute("""SELECT * FROM stock""")
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i

    def database_buys_stock(self):
        dataUser = data.data(self.userid).dataUser()
        if self.colvo * self.price <= dataUser[4]:
            summ = dataUser[4] - (self.colvo * self.price)
            self.cur.execute(f"""Update stock set {self.kripta} = {self.colvo} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        elif self.colvo / self.price >= dataUser[4]:
            summ_back = dataUser[4] + (self.colvo * self.price)
            self.cur.execute(f"""Update stock set {self.kripta} = {self.colvo} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ_back} where userid = {self.userid}""")
            self.conn.commit()

if __name__ == '__main__':
<<<<<<< Updated upstream
    assets = assets(951679992, 'Связьком', 10, 10)
    assets.random_cript()
    assets.database_buys_stock()
=======
    cript1 = assets(1)
    cript1.random_cript()
    cript1.database_connect()
>>>>>>> Stashed changes
