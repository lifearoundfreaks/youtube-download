import telebot
from os import getenv as env
import logging


def setup_bot(**kwargs):

    bot = telebot.TeleBot(env("TELEGRAM_BOT_TOKEN"))
    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)

    @bot.message_handler(commands=['start'])
    def start(message):

        bot.send_message(
            message.chat.id, 'Hello, ' + message.from_user.first_name)

    @bot.message_handler(commands=['ping'])
    def ping(message):

        bot.send_message(message.chat.id, 'pong')

    bot.remove_webhook()
    bot.set_webhook(url=f'{env("WEB_APP_DOMAIN")}/{env("TELEGRAM_BOT_TOKEN")}')

    def handle_update(request_json):
        bot.process_new_updates([telebot.types.Update.de_json(request_json)])

    return handle_update
