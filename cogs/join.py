from nextcord import Interaction, slash_command, Embed, voice_client
from nextcord.ext.commands import Bot, Cog
from nextcord import FFmpegPCMAudio

class Join(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        
    @slash_command(name="join", description="Join Grue to a Voice Channel")
    async def join(self, inter: Interaction):
    
        guild_id = inter.guild_id
        if guild_id not in self.bot.server_sessions:
            if inter.user.voice is None:
                return await inter.send(f'You are not connected to any voice channel!')
            else:
              session  = await inter.user.voice.channel.connect()
              if session.is_connected():
                self.bot.server_sessions[inter.guild_id] = session 
                await inter.send(f'Connected to {session.channel.name}.')
              else:
                await inter.send(f'Failed to connect to voice channel {inter.user.voice.channel.name}.')
        else:
            session = self.bot.server_sessions[guild_id]
            if session.channel != inter.user.voice.channel: 
                   print("channel move")
                   await session.move_to(inter.user.voice.channel)
                   await inter.send(f'Connected to {inter.user.voice.channel}.')
            else:
                await inter.send(f'Connected to {inter.user.voice.channel}.')
                  
    
def setup(bot: Bot) -> None:
    bot.add_cog(Join(bot))