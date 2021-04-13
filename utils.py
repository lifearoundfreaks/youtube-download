from telebot import TeleBot
from os import getenv as env


def get_bot():

    return TeleBot(env("TELEGRAM_BOT_TOKEN"))


def validate_url(url):

    split_url = url.split("&")
    return split_url[0] if split_url else ""


def is_int(string):

    try:

        int(string)

    except ValueError:

        return False

    return True
