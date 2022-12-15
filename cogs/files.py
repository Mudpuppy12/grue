from nextcord import Interaction, slash_command, Attachment, Message
from nextcord.ext.commands import Bot, Cog
import os


class Files(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @slash_command(name="upload", description="Upload a file.")
    async def upload(self, inter: Interaction, file: Attachment) -> None:
        path = "uploads/" + str(inter.user.id) + "/"     
        await inter.send(f"Uploading...")
        
        # Create a directory to store user uploads
        if not os.path.exists(path):
            os.mkdir(path)

        await file.save(path + file.filename)
        await inter.send(f"Upload complete.")

def setup(bot: Bot) -> None:
    bot.add_cog(Files(bot))