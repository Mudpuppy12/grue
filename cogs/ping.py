from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="A simple ping command.")
    async def ping(self, inter):
        await inter.response.send_message(f"Pong! {self.bot.latency * 1000:.2f}ms")

async def setup(bot):
    await bot.add_cog(Ping(bot))