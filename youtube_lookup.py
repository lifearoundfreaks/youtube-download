from pytube import YouTube

from const import VIDEO_SETTINGS
import utils


def youtube_lookup(url):

    return YouTube(
        utils.validate_url(url)
    ).streams.filter(**VIDEO_SETTINGS).first().url
