#!/usr/bin/env python3

class ServerSession:
    def __init__(self, guild_id, voice_client):
        self.guild_id: int = guild_id
        self.voice_client = voice_client
        self.queue: List[Source] = []

    def display_queue(self):
        currently_playing = f'Currently playing: 0. {self.queue[0]}'
        return currently_playing + '\n' + '\n'.join([f'{i + 1}. {s}' for i, s in enumerate(self.queue[1:])])

    async def add_to_queue(self, ctx, url):  # does not auto start playing the playlist
        yt_source = await YTDLSource.from_url(url, loop=bot.loop, stream=False)  # stream=True has issues and cannot use Opus probing
        self.queue.append(yt_source)
        if self.voice_client.is_playing():
            async with ctx.typing():
                await ctx.send(f'Added to queue: {yt_source.title}')
            pass  # to stop the typing indicator

    async def start_playing(self, ctx):
        async with ctx.typing():
            self.voice_client.play(self.queue[0].audio_source, after=lambda e=None: self.after_playing(ctx, e))
        await ctx.send(f'Now playing: {self.queue[0].title}')

    async def after_playing(self, ctx, error):
        if error:
            raise error
        else:
            if self.queue:
                await self.play_next(ctx)

    async def play_next(self, ctx):  # should be called only after making the first element of the queue the song to play
        self.queue.pop(0)
        if self.queue:
            async with ctx.typing():
                await self.voice_client.play(self.queue[0].audio_source, after=lambda e=None: self.after_playing(ctx, e))
            await ctx.send(f'Now playing: {self.queue[0].title}')