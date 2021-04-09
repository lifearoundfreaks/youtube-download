from pytube import YouTube
from utils import get_bot
import ffmpeg
import os
from uuid import uuid4


VIDEO_SETTINGS = {
    'only_video': True,
    'adaptive': True,
    'subtype': "mp4"
}

AUDIO_SETTINGS = {
    'only_audio': True,
    'subtype': "mp4"
}


def validate_url(url):

    split_url = url.split("&")
    return split_url[0] if split_url else ""


def get_resolutions(url):

    yt = YouTube(validate_url(url))
    if yt.publish_date is None:
        raise ValueError
    return list({
        stream.resolution: None
        for stream in yt.streams.filter(**VIDEO_SETTINGS).asc()
    })


def download(chat_id, url, resolution):

    video_name, audio_name, out_name = (str(uuid4()) for _ in range(3))

    yt = YouTube(validate_url(url))
    video = yt.streams.filter(**VIDEO_SETTINGS).first().download(
        filename=video_name)
    video_stream = ffmpeg.input(video_name)
    audio = yt.streams.filter(**AUDIO_SETTINGS).first().download(
        filename=audio_name)
    audio_stream = ffmpeg.input(audio_name)

    try:
        ffmpeg.output(
            audio_stream, video_stream, f'{out_name}.mp4'
        ).run(quiet=True)
    except ffmpeg.Error as e:
        pass

    video = ffmpeg.input(f'{video_name}.mp4')
    audio = ffmpeg.input(f'{audio_name}.mp4')
    out = ffmpeg.output(
        video, audio, f'{out_name}.mp4', vcodec='copy',
        acodec='aac', strict='experimental')
    try:
        out.run(quiet=True)
    except ffmpeg.Error as e:
        pass

    get_bot().send_video(
        chat_id, open(f'{out_name}.mp4', 'rb'),
        supports_streaming=True,
    )

    try:
        for filename in (video_name, audio_name, out_name):
            os.remove(f'{filename}.mp4')
    except OSError:
        pass
