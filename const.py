VIDEO_SETTINGS = {
    'only_video': True,
    'adaptive': True,
    'subtype': 'mp4'
}

AUDIO_SETTINGS = {
    'only_audio': True,
    'subtype': 'mp4'
}

MAX_VIDEO_SECONDS = 60

DEFAULT_TIME = 0

BEST_RESOLUTION_TAG = 'best'

BOT_INPUT_TIP = (
    "You need to send me your video in one of the following formats:\n"
    "`<youtube link>`\n"
    "`<youtube link> <timestamp from>`\n"
    "`<youtube link> <timestamp from> <timestamp to>`\n\n"
    "`<youtube link> <timestamp from> <amount of seconds>s`\n\n"
    "For example:\n"
    "`https://www.youtube.com/watch?v=dQw4w9WgXcQ`\n"
    "`https://www.youtube.com/watch?v=dQw4w9WgXcQ 1:31`\n"
    "`https://www.youtube.com/watch?v=dQw4w9WgXcQ 480p`\n\n"
    "`https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:01:31 2:15`\n"
    "`https://www.youtube.com/watch?v=dQw4w9WgXcQ 1:31 15s`\n"
    "`https://www.youtube.com/watch?v=dQw4w9WgXcQ 1:31 15s 720p`\n\n"
    "In case of missing starting timestamp default value will be "
    f"{DEFAULT_TIME}. Default and maximum video length is "
    f"{MAX_VIDEO_SECONDS} seconds."
)

START_TEXT = (
    "Under construction."
)
