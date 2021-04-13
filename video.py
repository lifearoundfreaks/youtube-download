import os
import subprocess
from uuid import uuid4

from utils import get_bot


def download(chat_id, v_url, a_url, time_from, time_to):

    try:

        temp_name = str(uuid4())

        command = (
            f'ffmpeg -ss {time_from} -to {time_to} -i "{v_url}" '
            f'-ss {time_from} -to {time_to} -i "{a_url}" '
            "-acodec aac -b:a 192k -avoid_negative_ts make_zero "
            f'-map 0:v:0 -map 1:a:0 "{temp_name}.mp4"'
        )

        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)

        get_bot().send_video(
            chat_id, open(f'{temp_name}.mp4', 'rb'),
            supports_streaming=True,
        )

    except Exception as e:

        get_bot().send_message(
            chat_id, 'Sorry, something was wrong with your video.')
        raise e

    finally:

        try:
            os.remove(f'{temp_name}.mp4')
        except OSError:
            pass
