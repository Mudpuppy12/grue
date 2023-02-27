#!/usr/bin/env python3
import configparser
import wavelink
from discord import app_commands
from discord.ext import commands

# Load the config file
config = configparser.ConfigParser()
config.read('bot.ini')

class Audio(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""
    
    def __init__(self, bot):
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
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @app_commands.command(name="ytmusic", description="Play some music from Youtube")
    async def play(self, inter, search: str):
        """ Play music from Youtube. """

        search = await wavelink.YouTubeTrack.search(query=search,return_first=True)
        if inter.user.voice is None:

            return await inter.response.send_message(f'You are not connected to any voice channel!')

        # If the bot isn't in a voice channel
        if not inter.guild.voice_client:
            vc: wavelink.Player = await inter.user.voice.channel.connect(cls=wavelink.Player)
        else:
          #See if the bot is in another channel
          if inter.guild.voice_client.channel != inter.user.voice.channel:
            await inter.guild.voice_client.move_to(inter.user.voice.channel) 
            
        vc: wavelink.Player = inter.guild.voice_client
        await vc.play(search)
        await inter.response.send_message(f'Playing {search.title}')

    @app_commands.command(name="lplay", description="Play some local music or SFX")
    async def lplay(self, inter, search:str):
        """ Play a local file in the lavalink /media volume """

        path = "/media/" + search 
        try:   
            search = await wavelink.LocalTrack.search(query=path,return_first=True)
        except:
            return await inter.response.send_message(f'{path} Not found!') 

        if inter.user.voice is None:
            return await inter.response.send_message(f'You are not connected to any voice channel!')

        # If the bot isn't in a voice channel
        if not inter.guild.voice_client:
            vc: wavelink.Player = await inter.user.voice.channel.connect(cls=wavelink.Player)
        else:
          #See if the bot is in another channel
          if inter.guild.voice_client.channel != inter.user.voice.channel:
            await inter.guild.voice_client.move_to(inter.user.voice.channel) 
            await inter.response.send_message(f'Connected to {inter.user.voice.channel}.')
            
        vc: wavelink.Player = inter.guild.voice_client

        await vc.play(search)
        await inter.response.send_message(f'Playing {search.title}')
  
    @app_commands.command(name="volume", description="Pause bot audio output.")
    async def volume(self, inter, volume : int):
        """ Change bot output volume """
        vc = inter.guild.voice_client
        if vc:
         await vc.set_volume(volume)
         await inter.response.send_message(f"Volume changed to {volume}")
        else:
            await inter.response.send_message(f"Grue isn't connected to a voice channel.")

    @app_commands.command(name="pause", description="Pause bot audio output.")
    async def pause(self, inter):
       """ Pause audio output of Bot """
        
       vc = inter.guild.voice_client
       if vc:
            await vc.pause()
            await inter.response.send_message("Audio stopped/paused.")
       else:
           await inter.response.send_message("The bot is not connected to a voice channel")
   
    @app_commands.command(name="resume", description="Resume bot audio output.")
    async def resume(self, inter):
       """ Resume audio playback from bot."""

       vc = inter.guild.voice_client
       if vc:
           if vc.is_paused():
              await vc.resume()
              await inter.response.send_message("Audio resumed.")
           else:
              await inter.response.send_message("Nothing is paused.")
       else:
          await inter.response.send_message("The bot is not connected to a voice channel")

    @app_commands.command(name="disconnect", description="Disconnect Grue from a voice channel")
    async def disconnect(self, inter): 
       """ Disconnect bot from a voice channel. """

       vc = inter.guild.voice_client
       if vc:
          await vc.disconnect()
          await inter.response.send_message("Grue has left the channel.")
       else:
          await inter.response.send_message("Grue is not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Audio(bot))
