from pytube import YouTube

import const
import utils


def youtube_lookup(url, res):

    yt = YouTube(utils.validate_url(url))
    video_settings = {**const.VIDEO_SETTINGS}
    if res != const.BEST_RESOLUTION_TAG:
        video_settings['resolution'] = res
    v_url = yt.streams.filter(**video_settings).first().url
    a_url = yt.streams.filter(**const.AUDIO_SETTINGS).first().url

    return v_url, a_url
