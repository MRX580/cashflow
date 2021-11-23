import random, sqlite3, data


class assets:
    def __init__(self, userid, number, price, coin = None, bondes = None, business = None):
        self.userid = userid
        self.coin = coin
        self.bondes = bondes
        self.business = business
        self.number = number
        self.price = price


        self.conn = sqlite3.connect('cashflow/users.db')
        self.cur = self.conn.cursor()
        self.conn.commit()
        print('Database connected')

    def random_cript(self):
        btc_price = random.randint(54000, 64000)
        bnb_price = random.randint(450, 540)
        avax_price = random.randint(80, 102)
        sol_price = random.randint(150, 197)
        eth_price = random.randint(3950, 4022)

        return str('Выбери крипту:\n1.Bitcoin ' + str(btc_price) + '$\n2.Binance Coin' + str(bnb_price) + '$\n3.Avalanche' + str(avax_price) + '$\n4.Solana' + str(sol_price) + '$\n5.Ethereum' + str(eth_price) + '$')

    def choise_insurance(self):
        return '1.Страховка на жизнь - 5 000 руб\n2.Страховка на имущество - 3000 руб'

    def insuranceUser(self):
        sqlite_select_query = """SELECT * FROM game"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i

    def coinUser(self):
        sqlite_select_query1 = """SELECT * FROM coins"""
        self.cur.execute(sqlite_select_query1)
        record1 = self.cur.fetchall()
        for i in record1:
            if i[0] == self.userid:
                return i


    def database_user_stock(self):
        self.cur.execute("""SELECT * FROM stock""")
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
    def database_user_bondes(self):
        self.cur.execute("""SELECT * FROM bondes""")
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return  i
    def database_user_businesses(self):
        self.cur.execute("""SELECT * FROM businesses""")
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i

    # Покупка акций
    def database_buys_stock(self):
        dataUser = data.data(self.userid).dataUser()
        dataStock = self.database_user_stock()
        if self.number * self.price <= dataUser[4]:
            for i in range(1,5):
                if self.coin == dataStock[i]:
                    coin = dataStock[i]
                    self.number += coin
                    break
            summ = dataUser[4] - (self.number * self.price)
            self.cur.execute(f"""Update stock set {self.coin} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            print('Нищеброд!')
    def database_buys_bondes(self):
        dataUser = data.data(self.userid).dataUser()
        dataBondes = self.database_user_bondes()
        if self.number * self.price <= dataUser[4]:
            if self.bondes == dataBondes[1]:
                bondes = dataBondes[1]
                self.number += bondes
            summ = dataUser[4] - (self.number * self.price)
            self.cur.execute(f"""Update bondes set {self.bondes} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update bondes set Доход = {self.number * 300} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            print('Нищеброд!')
    def database_buys_businesses(self):
        dataUser = data.data(self.userid).dataUser()
        dataBusinesses = self.database_user_bondes()
        if self.number * self.price <= dataUser[4]:
            if self.business == dataBusinesses[1]:
                businesses = dataBusinesses[1]
                self.number += businesses
            summ = dataUser[4] - (self.number * self.price)
            self.cur.execute(f"""Update businesses set {self.business} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходAMD = {self.number * 500} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходIntel = {self.number * 700} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходNvidia = {self.number * 900} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходApple = {self.number * 1200} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            print(summ)
            self.conn.commit()
        else:
            print('Нищеброд!')
if __name__ == '__main__':
    assets = assets(672532296, 'Связьком','Вексель','AMD',10, 10,)
    assets.random_cript()
    assets.database_buys_stock()
    assets.database_buys_bondes()
    assets.database_buys_businesses()