import random
import sqlite3
class assets:
    def __init__(self, userid, kripta, colvo, price):
        self.userid = userid
        self.userid = kripta
        self.userid = colvo
        self.userid = price
    def random_cript(self):
        btc_price = random.randint(54000, 64000)
        bnb_price = random.randint(450, 540)
        avax_price = random.randint(80, 102)
        sol_price = random.randint(150, 197)
        eth_price = random.randint(3950, 4022)
        #print('Выбери крипту:\n1.Bitcoin ' + str(btc_price) + '$\n2.Binance Coin' + str(bnb_price) + '$\n3.Avalanche' + str(avax_price) + '$\n4.Solana' + str(sol_price) + '$\n5.Ethereum' + str(eth_price) + '$')
        return 'Выбери крипту:\n1.Bitcoin ' + str(btc_price) + '$\n2.Binance Coin' + str(bnb_price) + '$\n3.Avalanche' + str(avax_price) + '$\n4.Solana' + str(sol_price) + '$\n5.Ethereum' + str(eth_price) + '$'

    def database_connect(self):
        self.conn = sqlite3.connect('kripta.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS kripta(
           userid INT PRIMARY KEY,
           btc INT,
           bnb INT,
           avax INT,
           sol INT,
           eth INT);
        """)
        self.conn.commit()
        print('Database connected')

    def kriptaUser(self):
        self.database_connect()
        sqlite_select_query = """SELECT * FROM kripta"""
        self.cur.execute(sqlite_select_query)
        record = self.cur.fetchall()
        for i in record:
            if i[0] == self.userid:
                return i
            elif i[1] == self.kripta:
                return i
            elif i[2] == self.colvo:
                return i
            elif i[3] == self.price:
                return i



if __name__ == '__main__':
    assets = assets(1, 2, 3, 4)
    assets.random_cript()
    assets.database_connect()
    assets.kriptaUser()








