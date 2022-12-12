#!/usr/bin/env python3
import configparser
import wavelink
from nextcord import Interaction, slash_command
from nextcord.ext.commands import Bot, Cog
from discord.ext import commands

# Load the config file
config = configparser.ConfigParser()
config.read('bot.ini')

class Audio(Cog):
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

    @slash_command(name="ytmusic", description="Play some music from Youtube")
    async def play(self, inter: Interaction, search):
        search = await wavelink.YouTubeTrack.search(query=search,return_first=True)
        """Play a song with the given search query.

        If not connected, connect to our voice channel.
        """
        if inter.user.voice is None:
            return await inter.send(f'You are not connected to any voice channel!')

        # If the bot isn't in a voice channel
        if not inter.guild.voice_client:
            vc: wavelink.Player = await inter.user.voice.channel.connect(cls=wavelink.Player)
        else:
          #See if the bot is in another channel
          if inter.guild.voice_client.channel != inter.user.voice.channel:
            await inter.guild.voice_client.move_to(inter.user.voice.channel) 
            await inter.send(f'Connected to {inter.user.voice.channel}.')
            
        vc: wavelink.Player = inter.guild.voice_client
        await vc.play(search)
        await inter.send(f'Playing {search.title}')

    @slash_command(name="lplay", description="Play some local music or SFX")
    async def lplay(self, inter: Interaction, search):
        path = "/media/" + search

        search = wavelink.PartialTrack(query=path, cls=wavelink.LocalTrack)

        if inter.user.voice is None:
            return await inter.send(f'You are not connected to any voice channel!')

        # If the bot isn't in a voice channel
        if not inter.guild.voice_client:
            vc: wavelink.Player = await inter.user.voice.channel.connect(cls=wavelink.Player)
        else:
          #See if the bot is in another channel
          if inter.guild.voice_client.channel != inter.user.voice.channel:
            await inter.guild.voice_client.move_to(inter.user.voice.channel) 
            await inter.send(f'Connected to {inter.user.voice.channel}.')
            
        vc: wavelink.Player = inter.guild.voice_client
       
        try: 
           await vc.play(search)
           await inter.send(f'Playing {search.title}')
        except:
           await inter.send(f'{path} Not found!') 


def setup(bot: Bot) -> None:
    bot.add_cog(Audio(bot))
