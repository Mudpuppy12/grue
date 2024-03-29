from discord import app_commands, Interaction
from discord.ext import commands
import openai
import configparser
import requests
import os
import datetime


# Load the config file
config = configparser.ConfigParser()
config.read('bot.ini')

class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="openai-image", description="Create an image.")
    async def openai_image(self, inter: Interaction, desc : str):
        openai.api_key = config['OPENAI']['API_KEY']
        await inter.response.send_message(f"Generating imaged from {desc}.")
        
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

        await inter.followup.send(f"{image_url}")

    @app_commands.command(name="openai-story", description="OpenAI test story generation.")
    async def openai_story(self, inter: Interaction, prompt: str):
        openai.api_key = config['OPENAI']['API_KEY']

        await inter.response.send_message(f"Generating content base on {prompt}.")

        response = openai.Completion.create(model="text-davinci-001",prompt=prompt,
                                            temperature=0.4, max_tokens=1024,top_p=1,
                                            frequency_penalty=0,presence_penalty=0
        )
        await inter.followup.send(f"{response['choices'][0].text}")
    
async def setup(bot):
    await bot.add_cog(OpenAI(bot))