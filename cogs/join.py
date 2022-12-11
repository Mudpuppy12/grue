from nextcord import Interaction, slash_command, Embed, voice_client
from nextcord.ext.commands import Bot, Cog
from nextcord import FFmpegPCMAudio
from sessions.ServerSession import ServerSession

class Join(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name="join", description="Join Grue to a Voice Channel")
    async def join(self, inter):
        guild_id = inter.guild_id

        if guild_id not in self.bot.server_sessions:
            if inter.user.voice is None:
                return await inter.send(f'You are not connected to any voice channel!')
            else:
              vc  = await inter.user.voice.channel.connect()
              if vc.is_connected():
                self.bot.server_sessions[inter.guild_id] = ServerSession(inter.guild_id,vc)
                await inter.send(f'Connected to {vc.channel.name}.')
              else:
                await inter.send(f'Failed to connect to voice channel {inter.user.voice.channel.name}.')
        else:
            session  = self.bot.server_sessions[guild_id].voice_client
            if session.channel != inter.user.voice.channel: 
                   await session.move_to(inter.user.voice.channel)
                   await inter.send(f'Connected to {inter.user.voice.channel}.')
            else:
                await inter.send(f'Connected to {inter.user.voice.channel}.')               
def setup(bot):
    bot.add_cog(Join(bot))