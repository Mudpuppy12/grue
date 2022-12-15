#!/usr/bin/env python3
import configparser
import wavelink
import discord
from discord.ext import commands

# Load the config file
config = configparser.ConfigParser()
config.read('bot.ini')

# Set variables from config file

TEST_GUILD_ID = config['DISCORD'].getint('GUILD_ID')
BOT_TOKEN = config['DISCORD']['BOT_TOKEN']


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(default_guild_ids=[TEST_GUILD_ID],
                         command_prefix="!", 
                         intents=discord.Intents.all()
                         )
    async def on_ready(self):
        print('Bot is ready!')
        
bot = Bot()
bot.load_extension("cogs.audio")
bot.load_extension("cogs.ping")
bot.load_extension("cogs.files")
bot.load_extension("cogs.openai")
bot.run(BOT_TOKEN)
