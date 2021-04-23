import os
import subprocess
from uuid import uuid4

from utils import get_bot


def run(command):

    subprocess.run(
        command, shell=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def download_stream(url, time_from, time_to, name):

    run(f'ffmpeg -ss {time_from} -to {time_to} -i "{url}" '
        f'-c:v copy -c:a copy -avoid_negative_ts make_zero {name}.mp4')


def silently_delete(*filenames):

    for name in filenames:
        try:
            os.remove(f'{name}.mp4')
        except OSError:
            pass


def download(chat_id, stream_url, time_from, time_to):

    try:
        video_name = str(uuid4())

        download_stream(stream_url, time_from, time_to, video_name)

        get_bot().send_video(
            chat_id, open(f'{video_name}.mp4', 'rb'), supports_streaming=True,
        )

    except Exception as e:

        get_bot().send_message(
            chat_id, 'Sorry, something was wrong with your video.')
        raise e

    finally:

        silently_delete(video_name)
