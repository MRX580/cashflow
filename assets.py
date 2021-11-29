import random, sqlite3, data

class assets:
    def __init__(self, userid, number, price, coin=None, bondes=None, business=None, kripta = None):
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
    def enterCript(self):
        sqlite_select_query = """SELECT * FROM coins"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i[1]
    def choise_insurance(self):
        return str('1.Страховка на жизнь - 5 000 $\n2.Страховка на имущество - 3000 $')

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
        sqlite_select_query = """SELECT * FROM stock"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] - (self.number * self.price)
        if self.number * self.price <= dataUser[4]:
            for i in range(1, 5):
                for row in records:
                    if self.userid == row[0]:
                        if self.coin == dataStock[i]:
                            coin = dataStock[i]
                            self.number += coin
                            break
            self.cur.execute(f"""Update stock set {self.coin} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            return str('У вас нет денег!')

    # Покупка облигаций
    def database_buys_bondes(self):
        dataUser = data.data(self.userid).dataUser()
        dataBondes = self.database_user_bondes()
        sqlite_select_query = """SELECT * FROM bondes"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] - (self.number * self.price)
        if self.number * self.price <= dataUser[4]:
            for row in records:
                if self.userid == row[0]:
                        self.number += dataBondes[1]
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
        bussines = ['0', 'AMD', '5000', 'Intel', '7000', 'Nvidia', '9000', 'Apple', '12000']
        sqlite_select_query = """SELECT * FROM businesses"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] - (self.number * self.price)
        if self.number * self.price <= dataUser[4]:
            for i in range(1, 8):
                print(self.business, dataBusinesses[i], i)
                for row in records:
                    if self.userid == row[0]:
                        if self.business == bussines[i]:
                            coin = dataBusinesses[i]
                            self.number += coin
                            break
            self.cur.execute(f"""Update businesses set {self.business} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            return str('У вас нет денег!')

    # Продажа акций
    def database_sell_stock(self):
        dataUser = data.data(self.userid).dataUser()
        dataStock = self.database_user_stock()
        sqlite_select_query = """SELECT * FROM stock"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] + (self.number * self.price)
        if self.number * self.price:
            for row in records:
                if self.userid == row[0]:
                    if self.coin == dataStock[1]:
                        coin = dataStock[1]
                        self.number -= coin
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
        sqlite_select_query = """SELECT * FROM bondes"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] + (self.number * self.price)
        if self.number * self.price:
            for row in records:
                if self.userid == row[0]:
                    if self.bondes == dataBondes[1]:
                        bondes = dataBondes[1]
                        self.number -= bondes
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
        sqlite_select_query = """SELECT * FROM businesses"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] + (self.number * self.price)
        if self.number * self.price:
            for row in records:
                if self.userid == row[0]:
                    if self.business == dataBondes[1]:
                        business = dataBondes[1]
                        self.number -= business
            self.cur.execute(f"""Update businesses set {self.business} = {self.number} where userid = {self.userid}""")
            print(self.business, self.number)
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        if self.business:
            if self.number <= 0:
                return str('У вас нету этого бизнеса')

    def crediUser(self):
        dataUser = data.data(self.userid).dataUser()
        credit = dataUser[11]
        stockMass = [0, 'Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром']
        try:
            self.cur.execute("""SELECT * FROM stock""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    for i in range(len(stockMass)):
                        if self.coin == stockMass[i]:
                            self.stock = int(row[i])
                            print(row[1])
                            break
            sum = int(self.stock) + int(self.number)
            self.cur.execute(f"""Update stock set {self.coin} = {sum} where userid = {self.userid}""")
        except Exception as e:
            print(e)
        try:
            self.cur.execute("""SELECT * FROM bondes""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    self.bondesNum = row[1]
            summ = self.bondesNum + self.number
            print(self.bondesNum)
            print(self.number)
            self.cur.execute(f"""Update bondes set {self.bondes} = {summ} where userid = {self.userid}""")
            self.cur.execute(f"""Update bondes set Доход_вексель = {summ * 300} where userid = {self.userid}""")
        except Exception as e:
            print(e)
        try:
            dataBusinesses = data.data(self.userid).dataBusinesses()
            self.cur.execute("""SELECT * FROM businesses""")
            record = self.cur.fetchall()
            bussines = ['0', 'AMD', '1', 'Intel', '1', 'Nvidia', '1', 'Apple', '1']
            for row in record:
                if row[0] == self.userid:
                    for i in range(1, 8):
                        print(self.business, dataBusinesses[i])
                        if self.business == bussines[i]:
                            self.businessesNum = dataBusinesses[i]
                            self.number += self.businessesNum
                            break
            summ = self.businessesNum + self.number
            self.cur.execute(f"""Update businesses set {self.business} = {summ} where userid = {self.userid}""")
        except Exception as e:
            print(e)
        try:
            self.cur.execute("""SELECT * FROM coins""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    self.kripta = row[2]
            self.cur.execute(f"""Update coins set {self.kripta} = {self.kripta + self.number} where userid = {self.userid}""")
        except Exception as e:
            print(e)
        try:
            self.cur.execute("""SELECT * FROM users""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    credit = row[11]
            self.cur.execute(f"""Update users set credit = {credit + self.number * self.price} where userid = {self.userid}""")
        except Exception as e:
            print(e)
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    assets = assets(userid=672532296, number=10)
    assets.random_criptWrite()