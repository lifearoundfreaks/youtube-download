from pytube import YouTube
from utils import get_bot
import ffmpeg
import os


VIDEO_SETTINGS = {
    'only_video': True,
    'adaptive': True,
    'subtype': "mp4"
}

AUDIO_SETTINGS = {
    'only_audio': True,
    'subtype': "mp4"
}


def get_resolutions(url):

    yt = YouTube(url)
    if yt.publish_date is None:
        raise ValueError
    return list({
        stream.resolution: None
        for stream in yt.streams.filter(**VIDEO_SETTINGS).asc()
    })


def download(chat_id, url, resolution):

    try:
        os.remove('out.mp4')
    except OSError:
        pass

    yt = YouTube(url)
    video = yt.streams.filter(**VIDEO_SETTINGS).first().download(
        filename='video')
    video_stream = ffmpeg.input('video')
    audio = yt.streams.filter(**AUDIO_SETTINGS).first().download(
        filename='audio')
    audio_stream = ffmpeg.input('audio')

    try:
        ffmpeg.output(audio_stream, video_stream, 'out.mp4').run(quiet=True)
    except ffmpeg.Error as e:
        pass

    video = ffmpeg.input('video.mp4')
    audio = ffmpeg.input('audio.mp4')
    out = ffmpeg.output(
        video, audio, 'out.mp4', vcodec='copy',
        acodec='aac', strict='experimental')
    try:
        out.run(quiet=True)
    except ffmpeg.Error as e:
        pass

    get_bot().send_video(
        chat_id, open('out.mp4', 'rb'),
        supports_streaming=True,
    )
