from flask import Flask, request
import requests, config
app = Flask(__name__)

def get_from_env(key):
    return eval(f'config.{key}')

def send_message(chat_id, text):
    method = "sendMessage"
    token = get_from_env('TOKEN')
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data = data)

@app.route('/', methods=["POST"]) # Вот сюда телеграмм шлёт свои сообщения
def process():
    chat_id = request.json["message"]["chat"]["id"]
    send_message(chat_id=chat_id, text="Привет")
    return {"ok": True}

if __name__ == '__main__':
    app.run()