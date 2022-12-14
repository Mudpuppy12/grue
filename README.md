# grue
Discord Bot for OSE and OSR games. Currently under construction.

# Setup
Add a bot.ini file (See below) and startup the lavalink container. Then
start the bot.

# Implemented so far
* Lavalink used for both local and YouTube media.
* Docker compose file for Lavalink
* Ping Cog
* Audio Cog

# Audio Cog (Commands)
* /lplay <file> - Play a local media file.
* /ytmusic <search> - Play audio from Youtube video.
* /pause - Pause or stop audio output.
* /resume - Resume a paused audio output.
* /disconnect - Disconnect the bot from a voice channel.
* /volume <[0-100]> - Set volume for audio output.

# Files Cog (Commands)
* /upload <file> - Upload a file to the bot.



# Ping Cog (Commands)
* /ping - Basic bot command to see if bot is responsive.

# Configuration
```
[DEFAULT]

[DISCORD]
APP_ID = Your APP ID
APP_SECRET = Your APP secret
GUILD_ID = Your server ID
BOT_TOKEN = Your Bot Token
PUBLIC_KEY = Your Bot Public Key

[LAVALINK]
# Default from configuration.yml

HOST= localhost
PORT= 6969
PASSWORD = <YOUR CONFIG PASSWORD>
HTTPS = false
```