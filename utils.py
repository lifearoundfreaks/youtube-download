from telebot import TeleBot
from os import getenv as env


def get_bot():

    return TeleBot(env("TELEGRAM_BOT_TOKEN"))
