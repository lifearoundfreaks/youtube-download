## Simple youtube video download bot
It tries to solve the problem of adaptive youtube streams being without sound by using `ffmpeg` library to combine audio and video streams.

Currently it is written in a way to only support mp4 streams. You should also note that telegram API only allows file sizes up to 50mb so this bot's capabilities are pretty limited.

## Setting up your own
I wrote it with [Heroku](https://www.heroku.com/home) in mind but I may rewrite it using [Docker](https://www.docker.com/) later to allow easier time hosting your own bot.

- You should set up two environment variables: TELEGRAM_BOT_TOKEN and WEB_APP_DOMAIN (an outside url of your app).
- You need to have Redis installed, for example by using [this](https://elements.heroku.com/addons/redistogo).
- You also need `ffmpeg` installed on your system. I used [this](https://elements.heroku.com/buildpacks/jonathanong/heroku-buildpack-ffmpeg-latest).
- I may have missed something, dm me if you have problems running it.

If you are using Heroku's free dyno hours, be mindful of the fact that an app will go to sleep after 30 minutes of inactivity.
