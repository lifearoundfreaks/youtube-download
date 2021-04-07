import telebot
from os import getenv as env
import logging
from rq import Queue
from worker import conn
from time import sleep

redis_queue = Queue(connection=conn)


def get_bot():

    return telebot.TeleBot(env("TELEGRAM_BOT_TOKEN"))


def rq_work(chat_id):

    sleep(10)
    get_bot().send_message(chat_id, 'Some computationally hard response.')


def setup_bot(**kwargs):

    bot = get_bot()
    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)

    @bot.message_handler(commands=['start'])
    def start(message):

        bot.send_message(
            message.chat.id, 'Hello, ' + message.from_user.first_name)

    @bot.message_handler(commands=['ping'])
    def ping(message):

        bot.send_message(message.chat.id, 'pong')

    @bot.message_handler(commands=['work'])
    def work(message):

        redis_queue.enqueue(rq_work, message.chat.id)
        bot.send_message(
            message.chat.id,
            f'Job added. It is currently in #{len(redis_queue.jobs)} position.'
        )

    bot.remove_webhook()
    bot.set_webhook(url=f'{env("WEB_APP_DOMAIN")}/{env("TELEGRAM_BOT_TOKEN")}')

    def handle_update(request_json):
        bot.process_new_updates([telebot.types.Update.de_json(request_json)])

    return handle_update
