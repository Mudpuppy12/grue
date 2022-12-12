#!/usr/bin/env python3
import configparser
import wavelink
from nextcord import Interaction, slash_command
from nextcord.ext.commands import Bot, Cog
from discord.ext import commands

# Load the config file
config = configparser.ConfigParser()
config.read('bot.ini')

class Music(Cog):
    """Music cog to hold Wavelink related commands and listeners."""

    def __init__(self, bot: Bot):
        self.bot = bot
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.bot,
                                            host=config['LAVALINK']['HOST'],
                                            port=config['LAVALINK'].getint('PORT'),
                                            password=config['LAVALINK']['PASSWORD'],
                                            https=config['LAVALINK'].getboolean('HTTPS')
        )
    @Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        """Play a song with the given search query.

        If not connected, connect to our voice channel.
        """
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        await vc.play(search)

def setup(bot: Bot) -> None:
    bot.add_cog(Music(bot))
