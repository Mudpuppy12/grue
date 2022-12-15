from nextcord import Interaction, slash_command
from nextcord.ext.commands import Bot, Cog
import openai
import configparser
import requests
import os
import datetime


# Load the config file
config = configparser.ConfigParser()
config.read('bot.ini')

class OpenAI(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @slash_command(name="openai-image", description="Create an image.")
    async def openai_image(self, inter: Interaction, desc : str) -> None:
        openai.api_key = config['OPENAI']['API_KEY']
        await inter.send(f"Generating imaged from {desc}.")
        
        path =  "uploads/" + str(inter.user.id) + "/"
        filename = datetime.datetime.now().strftime("%y%m%d_%H%M%S") + ".png"
   

        response = openai.Image.create( prompt=desc,n=1,size="1024x1024")
        image_url = response['data'][0]['url']

        img_data = requests.get(image_url).content
 
        # Create a directory to store user uploads
        if not os.path.exists(path):
            os.mkdir(path)

        with open(path + filename, 'wb') as handler:
           handler.write(img_data)

        await inter.send(f"{image_url}")

def setup(bot: Bot) -> None:
    bot.add_cog(OpenAI(bot))