import telebot
from os import getenv as env


def setup_bot(**kwargs):

    bot = telebot.TeleBot(env("TELEGRAM_BOT_TOKEN"))

    @bot.message_handler(commands=['start'])
    def start(message):

        bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

    @bot.message_handler(commands=['ping'])
    def ping(message):

        bot.reply_to(message, 'pong')

    bot.remove_webhook()
    bot.set_webhook(url=f'{env("WEB_APP_DOMAIN")}/{env("TELEGRAM_BOT_TOKEN")}')

    def handle_update(request_json):
        bot.process_new_updates([telebot.types.Update.de_json(request_json)])

    return handle_update
