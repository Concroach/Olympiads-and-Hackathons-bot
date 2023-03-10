from flask import Flask, request
import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
import json


app = Flask(__name__)

#
def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)  # возвращен серкетный токен (или ключ к платежной системе)


def send_message(chat_id, text):
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route('/', methods=["POST"])  # localhost:5000/ - на этот адрес телеграм шлет свои сообщение
def process():
    chat_id = request.json['message']['chat']['id']
    send_message(chat_id=chat_id, text='Hello')
    return {'ok': True}


if __name__ == '__main__':
    app.run()