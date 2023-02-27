#!/usr/bin/env python3
# Dropped nextcord switching to discord.py

import configparser
import discord
import asyncio
from discord.ext import commands
import os



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

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start(BOT_TOKEN)

client = Bot()
asyncio.run(main())          



