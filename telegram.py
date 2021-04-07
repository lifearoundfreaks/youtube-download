import telebot
from os import getenv as env
import logging
from rq import Queue
from worker import conn
import video
import utils

redis_queue = Queue(connection=conn)


def setup_bot(**kwargs):

    bot = utils.get_bot()
    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)

    @bot.message_handler(commands=['start'])
    def start(message):

        bot.send_message(
            message.chat.id, 'Hello, ' + message.from_user.first_name)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        redis_queue.enqueue(
            video.download, call.from_user.id, *call.data.split())
        bot.answer_callback_query(call.id, call.data)
        bot.delete_message(call.from_user.id, call.message.id)

    @bot.message_handler(func=lambda message: True)
    def message_receiver(message):
        try:
            keyboard = telebot.types.InlineKeyboardMarkup([
                [telebot.types.InlineKeyboardButton(
                    resolution, callback_data=f"{message.text} {resolution}")]
                for resolution in video.get_resolutions(message.text)
            ])
            bot.send_message(
                message.chat.id, 'Pick available resolution.',
                reply_markup=keyboard
            )
        except Exception:
            bot.send_message(
                message.chat.id, 'There was something wrong with your link.')

    bot.remove_webhook()
    bot.set_webhook(url=f'{env("WEB_APP_DOMAIN")}/{env("TELEGRAM_BOT_TOKEN")}')

    def handle_update(request_json):
        bot.process_new_updates([telebot.types.Update.de_json(request_json)])

    return handle_update
