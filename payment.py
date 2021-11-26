import requests, config, monobank, time,  sqlite3, data as datas
from datetime import datetime
from telebot import TeleBot

bot = TeleBot(config.TOKEN)
while True:
    api = config.MONO
    mono = monobank.Client(api)
    data = {"X-Token": api}
    user = requests.get('https://api.monobank.ua/personal/client-info', headers = data).text
    print(eval(user)['accounts'][0])
    print(mono.get_client_info())
    d = datetime.now()
    unixtime = time.mktime(d.timetuple())
    comm = requests.get(f'https://api.monobank.ua/personal/statement/{0}/{int(unixtime-86400)}', headers = data).text.replace('true', '"da"').replace('false', '"da"')
    print(eval(comm))
    commdatabase = []
    commMono = []
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    sqlite_select_query = """SELECT * FROM donate"""
    cur.execute(sqlite_select_query)
    record = cur.fetchall()
    for i in record:
        commdatabase.append(str(i[0]) + ' ' + i[2])
    for i in eval(comm):
        try:
            commMono.append(i['comment'])
        except KeyError:
            pass
    print(commdatabase)
    print(commMono)
    for i in range(0,len(commdatabase)):
        if commdatabase[i].split()[1] in commMono:
            datas.data(commdatabase[i].split()[0], column='premium', changes=True).dataChanges()
            bot.send_message(commdatabase[i].split()[0], 'Премиум выдан')
            cur.execute(f"""DELETE from donate where userid = {commdatabase[i].split()[0]}""")
            conn.commit()
    time.sleep(60)