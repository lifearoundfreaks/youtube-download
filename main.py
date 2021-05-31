from flask import Flask, request
from os import getenv as env
from telegram import setup_bot
from waitress import serve
from json import loads
from telebot.types import Update
from worker import conn as redis

server = Flask(__name__)
handle_bot_update = setup_bot()


@server.route('/', methods=['GET'])
def ping():

    return "!", 200


@server.route(f'/{env("TELEGRAM_BOT_TOKEN")}', methods=['POST'])
def telegram_update():

    request_data = request.stream.read().decode("utf-8")
    update = Update.de_json(request_data)
    redis_response = redis.set(
        "recentTelegramChatUpdates", str(update.update_id), ex=300
    )
    print("-"*200)
    print(str(update.update_id))
    print(redis_response)
    handle_bot_update(update)

    return "!", 200


serve(server, host="0.0.0.0", port=int(env("PORT")))
