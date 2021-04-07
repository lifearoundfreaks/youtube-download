import telebot
from os import getenv as env
import logging
from rq import Queue
from worker import conn
from utils import get_bot

redis_queue = Queue(connection=conn)


def setup_bot(**kwargs):

    bot = get_bot()
    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)

    @bot.message_handler(commands=['start'])
    def start(message):

        bot.send_message(
            message.chat.id, 'Hello, ' + message.from_user.first_name)

    @bot.message_handler(commands=['video'])
    def video(message):
        keyboard = telebot.types.ReplyKeyboardMarkup(
            row_width=1, one_time_keyboard=True)
        keyboard.add("one", "two", "three")
        bot.send_message(
            message.chat.id, 'Pick available format', reply_markup=keyboard)

    # @bot.message_handler(commands=['work'])
    # def work(message):

    #     position = len(redis_queue.jobs) + 1
    #     redis_queue.enqueue(rq_work, message.chat.id)
    #     bot.send_message(
    #         message.chat.id,
    #         f'Job added. It is currently in #{position} position.'
    #     )

    bot.remove_webhook()
    bot.set_webhook(url=f'{env("WEB_APP_DOMAIN")}/{env("TELEGRAM_BOT_TOKEN")}')

    def handle_update(request_json):
        bot.process_new_updates([telebot.types.Update.de_json(request_json)])

    return handle_update
