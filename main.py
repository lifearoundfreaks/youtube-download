from flask import Flask, request
from os import getenv as env
from telegram import setup_bot
from waitress import serve

server = Flask(__name__)
handle_bot_update = setup_bot()


@server.route('/', methods=['GET'])
def ping():

    return "!", 200


@server.route(f'/{env("TELEGRAM_BOT_TOKEN")}', methods=['POST'])
def telegram_update():

    handle_bot_update(request.stream.read().decode("utf-8"))

    return "!", 200


serve(server, host="0.0.0.0", port=int(env("PORT")))
