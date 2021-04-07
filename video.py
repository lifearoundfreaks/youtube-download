from pytube import YouTube


def get_resolutions(url):

    yt = YouTube(url)
    if yt.publish_date is None:
        raise ValueError
    return list({
        stream.resolution: None
        for stream in yt.streams.filter(only_video=True, adaptive=True).asc()
    })
