from telebot import TeleBot
from os import getenv as env
import exceptions
import const


def get_bot():

    return TeleBot(env("TELEGRAM_BOT_TOKEN"))


def validate_url(url):

    split_url = url.split("&")
    return split_url[0] if split_url else ""


def get_timestamp()


def parse_user_input(string):

    split_input = string.split()
    input_length = len(split_input)

    if input_length == 1:

        timestamp = const.DEFAULT_TIME
        return split_input[0], timestamp, get_second_timestamp(timestamp)

    elif input_length == 2:

        timestamp = validate_timestamp(timestamp)
        return split_input[0], timestamp, get_second_timestamp(timestamp)

    elif input_length == 3:

        timestamp = validate_timestamp(timestamp)
        t


    try:
        url, time_from, time_to = 
    except ValueError:
        raise exceptions.InputValidationException(const.BOT_INPUT_TIP)

