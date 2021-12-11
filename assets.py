import random, sqlite3, data

class assets:
    def __init__(self, userid = None, number = None, price = None, coin=None, bondes=None, business=None, insurance = None):
        self.userid = userid
        self.coin = coin
        self.bondes = bondes
        self.business = business
        self.number = int(number)
        self.price = int(price)
        self.insurance = insurance
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.conn.commit()

    def random_cript(self):
        btc_price = random.randint(54000, 64000)
        xrp_price = random.randint(3, 7)
        avax_price = random.randint(80, 102)
        sol_price = random.randint(150, 197)
        eth_price = random.randint(3500, 4300)
        coin = str('Выбери крипту:\n1. Bitcoin ' + str(btc_price) + '\n2. XRP ' + str(
            xrp_price) + '\n3. Avalanche ' + str(avax_price) + '\n4. Solana ' + str(sol_price) + '\n5. Ethereum ' + str(
            eth_price) + '')
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
        return str('1.Страховка на жизнь - 5 000 $\n2.Страховка на имущество - 3000 $\n3.Страховка на раздачу - 1500 $\n4.Страховка на налоги - 1150 $\n5.Страховка от казино - 1000 $\n6.Страховка от ограблений - 900 $')

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

    def database_user_coin(self):
        self.cur.execute("""SELECT * FROM coins""")
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
        dataBuying = data.data(self.userid).dataBuing()
        stockMass = [0, 'Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром']
        buying = '0 0'
        sqlite_select_query = """SELECT * FROM stock"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] - (self.number * self.price)
        if self.number * self.price <= dataUser[4]:
            for i in range(len(stockMass)):
                for row in records:
                    if self.userid == row[0]:
                        if self.coin == stockMass[i]:
                            coin = dataStock[i]
                            buying = dataBuying[i]
                            self.number += coin
                            break
            self.cur.execute(f"""Update buying set {self.coin} = (?) where userid = {self.userid}""", (str(int(buying.split()[0]) + self.price) + ' ' + str(int(buying.split()[1])+1),))
            self.cur.execute(f"""Update stock set {self.coin} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            return str('У вас нет денег!')


    def database_buys_coin(self):
        dataUser = data.data(self.userid).dataUser()
        dataCoin = self.database_user_coin()
        dataBuying = data.data(self.userid).dataBuing()
        coinMass = [0,0, 'Bitcoin', 'XRP', 'Avalanche', 'Solana', 'Ethereum']
        sqlite_select_query = """SELECT * FROM coins"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        buying = '0 0'
        summ = dataUser[4] - (self.number * self.price)
        if self.number * self.price <= dataUser[4]:
            for i in range(len(coinMass)):
                for row in records:
                    if self.userid == row[0]:
                        if self.coin == coinMass[i]:
                            coin = dataCoin[i]
                            buying = dataBuying[i + 4]
                            print(buying)
                            self.number += coin
                            break
            self.cur.execute(f"""Update buying set {self.coin} = (?) where userid = {self.userid}""",
                             (str(int(buying.split()[0]) + self.price) + ' ' + str(int(buying.split()[1]) + 1),))
            self.cur.execute(f"""Update coins set {self.coin} = {self.number} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            return str('У вас нет денег!')

    # Покупка страховок
    def database_buys_insurance(self):
        dataInsurance = data.data(self.userid).dataInsurance()
        sqlite_select_query = """SELECT * FROM insurance"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        self.number = 12
        for row in records:
            if self.userid == row[0]:
                if self.insurance == 'СЖ':
                    self.number += dataInsurance[1]
                elif self.insurance == 'СИ':
                    self.number += dataInsurance[2]
                elif self.insurance == 'СД':
                    self.number += dataInsurance[3]
                elif self.insurance == 'СН':
                    self.number += dataInsurance[4]
                elif self.insurance == 'СК':
                    self.number += dataInsurance[5]
                elif self.insurance == 'СО':
                    self.number += dataInsurance[6]

        self.cur.execute(f"""Update insurance set {self.insurance} = {self.number} where userid = {self.userid}""")
        self.conn.commit()

    # Покупка облигаций
    def database_buys_bondes(self):
        dataUser = data.data(self.userid).dataUser()
        dataBondes = self.database_user_bondes()
        dataBuying = data.data(self.userid).dataBuing()
        sqlite_select_query = """SELECT * FROM bondes"""
        buying = '0 0'
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] - (self.number * self.price)
        if self.number * self.price <= dataUser[4]:
            for row in records:
                if self.userid == row[0]:
                        buying = dataBuying[11]
                        self.number += dataBondes[1]
            self.cur.execute(f"""Update buying set {self.bondes} = (?) where userid = {self.userid}""",
                             (str(int(buying.split()[0]) + self.price) + ' ' + str(int(buying.split()[1]) + 1),))
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
        stockMass = [0, 'Связьком', 'Нефтехим', 'Инвестбанк', 'Агросбыт', 'Металлпром']
        dataUser = data.data(self.userid).dataUser()
        dataStock = self.database_user_stock()
        sqlite_select_query = """SELECT * FROM stock"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] + (self.number * self.price)
        coin = 0
        for row in records:
            if self.userid == row[0]:
                for i in range(len(stockMass)):
                    if self.coin == stockMass[i]:
                        coin = dataStock[i]
                        coin -= self.number
                        break
            self.cur.execute((f"""Update stock set {self.coin} = {coin} where userid = {self.userid}"""))
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        if self.coin:
            if self.number <= 0:
                return str('У вас нету этой акции ')

    def database_sell_coin(self):
        dataUser = data.data(self.userid).dataUser()
        dataCoin = self.database_user_coin()
        coinMass = [0,0, 'Bitcoin', 'XRP', 'Avalanche', 'Solana', 'Ethereum']
        sqlite_select_query = """SELECT * FROM coins"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] + (self.number * self.price)
        coin = 0
        for i in range(len(coinMass)):
            for row in records:
                if self.userid == row[0]:
                    if self.coin == coinMass[i]:
                        coin = dataCoin[i]
                        coin -= self.number
                        break
            self.cur.execute(f"""Update coins set {self.coin} = {coin} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        else:
            return str('У вас нет денег!')

    # Продажа облигаций
    def database_sell_bondes(self):
        dataUser = data.data(self.userid).dataUser()
        dataBondes = self.database_user_bondes()
        sqlite_select_query = """SELECT * FROM bondes"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] + (self.number * self.price)
        bondes = 0
        for row in records:
            if self.userid == row[0]:
                bondes = dataBondes[1]
                bondes -= self.number
            self.cur.execute((f"""Update bondes set {self.bondes} = {bondes} where userid = {self.userid}"""))
            self.cur.execute(f"""Update users set money = {summ} where userid = {self.userid}""")
            self.conn.commit()
        if self.bondes:
            if self.number <= 0:
                return str('У вас нету этой облигации')

    # Продажа бизнесов
    def database_sell_businesses(self):
        dataUser = data.data(self.userid).dataUser()
        dataBusinesses = data.data(self.userid).dataBusinesses()
        bussines = ['0', 'AMD', '5000', 'Intel', '7000', 'Nvidia', '9000', 'Apple', '12000']
        sqlite_select_query = """SELECT * FROM businesses"""
        self.cur.execute(sqlite_select_query)
        records = self.cur.fetchall()
        summ = dataUser[4] + (self.number * self.price)
        if self.number * self.price:
            for row in records:
                if self.userid == row[0]:
                    for i in range(len(bussines)):
                        if self.business == bussines[i]:
                            business = dataBusinesses[i]
                            self.number -= business
            self.cur.execute(f"""Update businesses set {self.business} = {self.number} where userid = {self.userid}""")
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
                    for i in range(len(bussines)):
                        if self.business == bussines[i]:
                            self.businessesNum = dataBusinesses[i]
                            self.number += self.businessesNum
                            break
            summ = self.businessesNum + self.number
            self.cur.execute(f"""Update businesses set {self.business} = {summ} where userid = {self.userid}""")
        except Exception as e:
            print(e)
        try:
            dataCoins = data.data(self.userid).dataCoins()
            self.cur.execute("""SELECT * FROM coins""")
            record = self.cur.fetchall()
            coinMass = [0,0, 'Bitcoin', 'XRP', 'Avalanche', 'Solana', 'Ethereum', 0]
            for row in record:
                if row[0] == self.userid:
                    for i in range(len(coinMass)):
                        if self.business == coinMass[i]:
                            self.CoinNum = dataCoins[i]
                            self.number += self.CoinNum
                            break
            self.cur.execute(f"""Update coins set {data.data(self.userid).dataCoins()[7].split()[0]} = {self.number} where userid = {self.userid}""")
        except Exception as e:
            print(e)
        try:
            dataInsurance = data.data(self.userid).dataInsurance()
            self.cur.execute("""SELECT * FROM insurance""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    if self.insurance == 'СЖ':
                        self.number += dataInsurance[1]
                        self.number = 12
                    elif self.insurance == 'СИ':
                        self.number += dataInsurance[2]
                        self.number = 12
                    elif self.insurance == 'СД':
                        self.number += dataInsurance[3]
                        self.number = 12
                    elif self.insurance == 'СН':
                        self.number += dataInsurance[4]
                        self.number = 12
                    elif self.insurance == 'СК':
                        self.number += dataInsurance[5]
                        self.number = 12
                    elif self.insurance == 'СО':
                        self.number += dataInsurance[6]
                        self.number = 12
            self.cur.execute(f"""Update insurance set {self.insurance} = {self.number} where userid = {self.userid}""")
            self.number = 1
        except Exception as e:
            print(e)
        try:
            self.cur.execute("""SELECT * FROM users""")
            record = self.cur.fetchall()
            for row in record:
                if row[0] == self.userid:
                    credit = row[11]
            if dataUser[4] - self.number * self.price <= 0:
                print(2)
                self.cur.execute(
                    f"""Update users set money = 0 where userid = {self.userid}""")
            else:
                self.cur.execute( f"""Update users set money = {self.number * self.price - dataUser[4]} where userid = {self.userid}""")
            self.cur.execute(f"""Update users set credit = {(credit + self.number * self.price) - dataUser[4]} where userid = {self.userid}""")
        except Exception as e:
            print(e)
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    assets = assets()
    assets.random_criptWrite()