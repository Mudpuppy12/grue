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
        
        try:   
            search = await wavelink.LocalTrack.search(query=path,return_first=True)
        except:
            return await inter.send(f'{path} Not found!') 

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
  
    @slash_command(name="pause", description="Pause bot audio output.")
    async def pause(self, inter: Interaction):
       vc = inter.guild.voice_client
       if vc:
           if vc.is_playing() and not vc.is_paused():
               await vc.pause()
               await inter.send("Audio stopped/paused.")
           else:
               await inter.send("Nothing is playing.")
       else:
           await inter.send("The bot is not connected to a voice channel")
   
    @slash_command(name="resume", description="Resume bot audio output.")
    async def resume(self, inter: Interaction):
       vc = inter.guild.voice_client
       if vc:
           if vc.is_paused():
              await vc.resume()
              await inter.send("Audio resumed.")
           else:
              await inter.send("Nothing is paused.")
       else:
          await inter.send("The bot is not connected to a voice channel")

    @slash_command(name="disconnect", description="Disconnect Grue from a voice channel")
    async def disconnect(self, inter): 
       vc = inter.guild.voice_client
       if vc:
          await vc.disconnect()
          await inter.send("Grue has left the channel.")
       else:
          await inter.send("Grue is not in a voice channel.")

def setup(bot: Bot) -> None:
    bot.add_cog(Audio(bot))
