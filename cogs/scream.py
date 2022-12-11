from nextcord import Interaction, slash_command, Embed, voice_client
from nextcord.ext.commands import Bot, Cog
from nextcord import FFmpegPCMAudio

class Scream(Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="scream", description="Scream")
    
    async def scream(self, inter):
        source = FFmpegPCMAudio('media/WilhelmScream.wav')   
        guild_id = inter.guild_id

        if guild_id not in self.bot.server_sessions:
            return await inter.send(f'Bot is  not connected to any voice channel!')

        session = self.bot.server_sessions[guild_id].voice_client
    
        if session.is_connected():
            session.play(source)

        await inter.send(
                embed=Embed(
                    description="BLEEEH",
                    color=0xFD45B5,
                )
            )

def setup(bot):
    bot.add_cog(Scream(bot))