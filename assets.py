import random, sqlite3, data

class assets:
    def __init__(self, userid, number, price = None, coin=None, bondes=None, business=None, kripta = None):
        self.userid = userid
        self.coin = coin
        self.bondes = bondes
        self.business = business
        self.number = int(number)
        self.price = int(price)
        self.kripta = kripta
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
        coin = str('Выбери крипту:\n1. Bitcoin ' + str(btc_price) + '$\n2. Binance Coin ' + str(
            bnb_price) + '$\n3. Avalanche ' + str(avax_price) + '$\n4. Solana ' + str(sol_price) + '$\n5. Ethereum ' + str(
            eth_price) + '$')
        return coin

    def random_criptWrite(self):
        coin = self.random_cript()
        self.cur.execute(f"""UPDATE coins SET coinRand = (?) WHERE userid = {self.userid}""", (coin,))
        self.conn.commit()
        return coin
    def choise_insurance(self):
        return str('1.Страховка на жизнь - 5 000 руб\n2.Страховка на имущество - 3000 руб')

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
                return i

    def database_user_businesses(self):
        self.cur.execute("""SELECT * FROM businesses""")
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i

    def database_user_credit(self):
        self.cur.execute("""SELECT * FROM users""")
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i

    # Покупка акций
    def database_buys_stock(self):
        dataUser = data.data(self.userid).dataUser()
        dataStock = self.database_user_stock()
        if self.number * self.price <= dataUser[4]:
            for i in range(1, 5):
                if self.coin == dataStock[i]:
                    coin = dataStock[i]
                    self.number += coin
                    break
            summ = dataUser[4] - (self.number * self.price)
            self.cur.execute(f"""Update stock set {self.coin} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            return str('У вас нет денег!')

    # Покупка облигаций
    def database_buys_bondes(self):
        dataUser = data.data(self.userid).dataUser()
        dataBondes = self.database_user_bondes()
        if self.number * self.price <= dataUser[4]:
            if self.bondes == dataBondes[1]:
                bondes = dataBondes[1]
                self.number += bondes
            summ = dataUser[4] - (self.number * self.price)
            self.cur.execute(f"""Update bondes set {self.bondes} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update bondes set Доход_вексель = {self.number * 300} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            return str('У вас нет денег!')

    # Покупка бизнесов
    def database_buys_businesses(self):
        dataUser = data.data(self.userid).dataUser()
        dataBusinesses = self.database_user_businesses()
        bussines = ['0', 'AMD', '1', 'Intel', '1', 'Nvidia', '1', 'Apple', '1']
        if self.number * self.price <= dataUser[4]:
            for i in range(1, 8):
                print(self.business, dataBusinesses[i])
                if self.business == bussines[i]:
                    coin = dataBusinesses[i]
                    self.number += coin
                    break
            summ = dataUser[4] - (self.number * self.price)
            self.cur.execute(f"""Update businesses set {self.business} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходAMD = {self.number * 500} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходIntel = {self.number * 700} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходNvidia = {self.number * 900} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходApple = {self.number * 1100} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            return str('У вас нет денег!')

    # Продажа акций
    def database_sell_stock(self):
        dataUser = data.data(self.userid).dataUser()
        dataStock = self.database_user_stock()
        if self.number * self.price:
            if self.coin == dataStock[1]:
                coin = dataStock[1]
                self.number -= coin
            summ = dataUser[4] + (self.number * self.price)
            self.cur.execute((f"""Update stock set {self.coin} = {self.number} where userid = {self.userid}"""))
            print(self.coin, self.number)
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        if self.coin:
            if self.number <= 0:
                return str('У вас нету этой акции ')

    # Продажа облигаций
    def database_sell_bondes(self):
        dataUser = data.data(self.userid).dataUser()
        dataBondes = self.database_user_bondes()
        if self.number * self.price:
            if self.bondes == dataBondes[1]:
                bondes = dataBondes[1]
                self.number -= bondes
            summ = dataUser[4] + (self.number * self.price)
            self.cur.execute((f"""Update bondes set {self.bondes} = {self.number} where userid = {self.userid}"""))
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        if self.bondes:
            if self.number <= 0:
                return str('У вас нету этой облигации')

    # Продажа бизнесов
    def database_sell_businesses(self):
        dataUser = data.data(self.userid).dataUser()
        dataBondes = self.database_user_bondes()
        if self.number * self.price:
            if self.business == dataBondes[1]:
                business = dataBondes[1]
                self.number -= business
            summ = dataUser[4] + (self.number * self.price)
            self.cur.execute(f"""Update businesses set {self.business} = {self.number} where userid = {self.userid}""")
            print(self.business, self.number)
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        if self.business:
            if self.number <= 0:
                return str('У вас нету этого бизнеса')

    def crediUser(self):
        global bondes, stock, businesses, credit, kripta
        dataUser = data.data(self.userid).dataUser()
        credit = dataUser[11]
        try:
            self.cur.execute("""SELECT * FROM stock""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    stock = row[1]
            self.cur.execute(f"""Update stock set {self.coin} = {stock + self.number} where userid = {self.userid}""")
        except sqlite3.OperationalError as e:
            print(e)
        try:
            self.cur.execute("""SELECT * FROM bondes""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    bondes = row[1]
            self.cur.execute(f"""Update bondes set {self.bondes} = {bondes + self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update bondes set Доход_вексель = {self.number * 300} where userid = {self.userid}""")
        except sqlite3.OperationalError as e:
            print(e)
        try:
            self.cur.execute("""SELECT * FROM businesses""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    businesses = row[1]
            self.cur.execute(f"""Update businesses set {self.business} = {businesses + self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходAMD = {self.number * 500} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходIntel = {self.number * 700} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходNvidia = {self.number * 900} where userid = {self.userid}""")
            self.cur.execute(f"""Update businesses set ДоходApple = {self.number * 1100} where userid = {self.userid}""")
        except sqlite3.OperationalError as e:
            print(e)
        try:
            self.cur.execute("""SELECT * FROM coins""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    kripta = row[2]
            self.cur.execute(f"""Update coins set {self.kripta} = {kripta + self.number} where userid = {self.userid}""")
        except sqlite3.OperationalError as e:
            print(e)
        try:
            self.cur.execute("""SELECT * FROM users""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    credit = row[11]
            self.cur.execute(f"""Update users set credit = {credit + self.number * self.price} where userid = {self.userid}""")
        except sqlite3.OperationalError as e:
            print(e)
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    assets = assets(userid=672532296, number=10)
    assets.random_criptWrite()