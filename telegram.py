import telebot
import logging
from os import getenv as env
from rq import Queue
from worker import conn

import video
import utils
import const
import exceptions
from youtube_lookup import youtube_lookup
from input_parser import Parser

redis_queue = Queue(connection=conn)


def setup_bot(**kwargs):

    global logger
    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)

    bot = utils.get_bot()

    @bot.message_handler(commands=['start'])
    def start(message):

        bot.send_message(message.chat.id, const.START_TEXT)

    @bot.message_handler(func=lambda message: True)
    def message_receiver(message):

        chat_id = message.chat.id

        try:

            url, time_from, time_to = Parser(message.text).all()

            try:
                stream_url = youtube_lookup(url)
            except Exception:
                raise exceptions.InputValidationException(
                    "There was something wrong with the link you sent."
                )

            redis_queue.enqueue(
                video.download, chat_id, stream_url, time_from, time_to
            )

            _len = len(redis_queue.jobs)
            status_text = \
                f"Your video is currently in position #{_len} in queue." \
                if _len else "Your video will start processing immediately."

            bot.send_message(
                chat_id, f"Thank you for your request! {status_text}"
            )

        except (
            exceptions.InputValidationException,
            exceptions.ForbiddenUserOperation,
        ) as e:
            bot.send_message(chat_id, e)

        except Exception as e:
            bot.send_message(chat_id, 'Oops! Something went wrong.')
            raise e

    bot.remove_webhook()
    bot.set_webhook(url=f'{env("WEB_APP_DOMAIN")}/{env("TELEGRAM_BOT_TOKEN")}')

    def handle_update(request_json):
        bot.process_new_updates([telebot.types.Update.de_json(request_json)])

    return handle_update
