import telebot
from os import getenv as env
import logging
from rq import Queue
from worker import conn
import video
import utils

redis_queue = Queue(connection=conn)

START_TEXT = (
    "Hello! This is a simple youtube video download bot.\n\n"
    "Just send me youtube links and pick a resolution. "
    "When your video is processed it will be sent back to you.\n\n"
    "Sadly, Telegram does not allow bots to send files larger than "
    "50mb, so be aware of that. There may be a solution for that,"
    " I will try to figure something out."
)


def setup_bot(**kwargs):

    bot = utils.get_bot()
    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)

    @bot.message_handler(commands=['start'])
    def start(message):

        bot.send_message(message.chat.id, START_TEXT)

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
        except Exception as e:
            bot.send_message(
                message.chat.id, 'There was something wrong with your link.')
            raise e

    bot.remove_webhook()
    bot.set_webhook(url=f'{env("WEB_APP_DOMAIN")}/{env("TELEGRAM_BOT_TOKEN")}')

    def handle_update(request_json):
        bot.process_new_updates([telebot.types.Update.de_json(request_json)])

    return handle_update
