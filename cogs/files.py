from discord import app_commands, Attachment, Message, Interaction
from discord.ext import commands
import os


class Files(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="upload", description="Upload a file.")
    async def upload(self, inter: Interaction, file: Attachment) -> None:
        path = "uploads/" + str(inter.user.id) + "/"     
        await inter.response.send_message(f"Uploading...")
        
        # Create a directory to store user uploads
        if not os.path.exists(path):
            os.mkdir(path)

        await file.save(path + file.filename)
        await inter.response.send_message(f"Upload complete.")

async def setup(bot):
    await bot.add_cog(Files(bot))