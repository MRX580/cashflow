import random
import sqlite3
class assets:
    def __init__(self, userid):
        self.userid = userid
    def random_cript(self):
        btc_price = random.randint(54000, 64000)
        bnb_price = random.randint(450, 540)
        avax_price = random.randint(80, 102)
        sol_price = random.randint(150, 197)
        eth_price = random.randint(3950, 4022)
        #print('Выбери крипту:\n1.Bitcoin ' + str(btc_price) + '$\n2.Binance Coin' + str(bnb_price) + '$\n3.Avalanche' + str(avax_price) + '$\n4.Solana' + str(sol_price) + '$\n5.Ethereum' + str(eth_price) + '$')
        return 'Выбери крипту:\n1.Bitcoin ' + str(btc_price) + '$\n2.Binance Coin' + str(bnb_price) + '$\n3.Avalanche' + str(avax_price) + '$\n4.Solana' + str(sol_price) + '$\n5.Ethereum' + str(eth_price) + '$'

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



if __name__ == '__main__':
    cript1 = assets(1)
    cript1.random_cript()
    cript1.database_connect()








