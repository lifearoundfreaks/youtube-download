VIDEO_SETTINGS = {
    'progressive': True,
    'subtype': 'mp4'
}

MAX_VIDEO_SECONDS = 60

DEFAULT_TIME = 0

BOT_INPUT_TIP = (
    "You need to send me your video in one of the following formats:\n"
    "<code>{youtube link}</code>\n"
    "<code>{youtube link} {timestamp from}</code>\n"
    "<code>{youtube link} {timestamp from} {timestamp to}</code>\n"
    "<code>{youtube link}t={starting second} {timestamp to}</code>\n"
    "<code>{youtube link} {timestamp from} {amount of seconds}s</code>\n\n"
    "For example:\n"
    "<code>https://www.youtube.com/watch?v=dQw4w9WgXcQ</code>\n"
    "<code>https://www.youtube.com/watch?v=dQw4w9WgXcQ 1:31</code>\n"
    "<code>https://www.youtube.com/watch?v=dQw4w9WgXcQ 00:01:31 2:15</code>\n"
    "<code>https://www.youtube.com/watch?v=dQw4w9WgXcQ 1:31 15s</code>\n"
    "<code>https://www.youtube.com/watch?v=dQw4w9WgXcQ 15 30</code>\n"
    "In case of missing starting timestamp default value will be "
    f"{DEFAULT_TIME}. Default and maximum video length is "
    f"{MAX_VIDEO_SECONDS} seconds."
)

START_TEXT = (
    "Hello, I am a bot for downloading short parts of youtube videos.\n"
    f"\n{BOT_INPUT_TIP}"
)
