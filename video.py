import os
import subprocess
from uuid import uuid4

from utils import get_bot


def run(command):

    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL)


def download_stream(url, time_from, time_to, name):

    run(f'ffmpeg -ss {time_from} -to {time_to} -i "{url}" "{name}.mp4"')


def combine(video, audio, out):

    run(f'ffmpeg -i {video}.mp4 -i {audio}.mp4 -c:v copy -c:a aac {out}.mp4')


def silently_delete(*filenames):

    for name in filenames:
        try:
            os.remove(f'{name}.mp4')
        except OSError:
            pass


def download(chat_id, v_url, a_url, time_from, time_to):

    try:
        video_name, audio_name, out_name = (str(uuid4()) for _ in range(3))

        download_stream(v_url, time_from, time_to, video_name)
        download_stream(a_url, time_from, time_to, audio_name)
        combine(video_name, audio_name, out_name)

        get_bot().send_video(
            chat_id, open(f'{out_name}.mp4', 'rb'), supports_streaming=True,
        )

    except Exception as e:

        get_bot().send_message(
            chat_id, 'Sorry, something was wrong with your video.')
        raise e

    finally:

        silently_delete(video_name, audio_name, out_name)
