import requests, config, monobank
api = config.MONO
mono = monobank.Client(api)
data = {"X-Token": api}
user = requests.get('https://api.monobank.ua/personal/client-info', headers = data).text
print(eval(user)['accounts'][0])
print(requests.get(f'https://api.monobank.ua/personal/statement/{0}/{1637410003}', headers = data).text)