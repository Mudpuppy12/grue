from nextcord import Interaction, slash_command, Embed, voice_client
from nextcord.ext.commands import Bot, Cog
from nextcord import FFmpegPCMAudio
import nextcord, requests
import yt_dlp
import asyncio

ffmpeg_options = {'options': '-vn -sn'}
ytdl_format_options = {'format': 'bestaudio',
                       'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                       'restrictfilenames': True,
                       'no-playlist': True,
                       'nocheckcertificate': True,
                       'ignoreerrors': False,
                       'logtostderr': False,
                       'geo-bypass': True,
                       'quiet': True,
                       'no_warnings': True,
                       'default_search': 'auto',
                       'source_address': '0.0.0.0'}

yt_dlp.utils.bug_reports_message = lambda: ''  # disable yt_dlp bug report
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class Source:
    """Parent class of all music sources"""

    def __init__(self, audio_source, metadata):
        self.audio_source = audio_source
        self.metadata = metadata
        self.title: str = metadata.get('title', 'Unknown title')
        self.url: str = metadata.get('url', 'Unknown URL')

    def __str__(self):
        return f'{self.title} ({self.url})'

class YTDLSource(Source):
    """Subclass of YouTube sources"""

    def __init__(self, audio_source: nextcord.AudioSource, metadata):
        super().__init__(audio_source, metadata)
        self.url: str = metadata.get('webpage_url', 'Unknown URL')  # yt-dlp specific key name for original URL

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        metadata = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in metadata: 
            metadata = metadata['entries'][0]

        if stream:
            filename = metadata['url']
        else:
            filename = ytdl.prepare_filename(metadata)

        return cls(await nextcord.FFmpegOpusAudio.from_probe(filename, **ffmpeg_options), metadata)

class yt(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="yt", description="You tube music player")
    
    async def yt(self, inter, url):
        guild_id = inter.guild_id
        if guild_id not in self.bot.server_sessions:
            return await inter.send(f'Bot is  not connected to any voice channel!')
 
        session = self.bot.server_sessions[guild_id]
   
        await session.add_to_queue(inter,url,self.bot)

        if not session.voice_client.is_playing() and len(session.queue) <= 1:
              await session.start_playing(inter)
    
def setup(bot):
    bot.add_cog(yt(bot))
