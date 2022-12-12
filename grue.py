#!/usr/bin/env python3
import configparser

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Bot

# Load the config file
config = configparser.ConfigParser()
config.read('bot.ini')

# Set variables from config file
TEST_GUILD_ID = config['DISCORD'].getint('GUILD_ID')
BOT_TOKEN = config['DISCORD']['BOT_TOKEN']

# Set the bot commands register for just the server we are testing.
bot = Bot(default_guild_ids=[TEST_GUILD_ID])

# Set bot server sessions
bot.server_sessions={}

# Load the slash commands

bot.load_extension("cogs.ping")
bot.load_extension("cogs.join")
bot.load_extension("cogs.yt")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


bot.run(BOT_TOKEN)
