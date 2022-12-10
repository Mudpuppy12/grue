#!/usr/bin/env python3
import configparser

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import Bot

config = configparser.ConfigParser()
config.read('bot.ini')

TEST_GUILD_ID = config['DISCORD'].getint('GUILD_ID')
BOT_TOKEN = config['DISCORD']['BOT_TOKEN']

bot = Bot(default_guild_ids=[TEST_GUILD_ID])
bot.server_sessions={}

bot.load_extension("cogs.ping")
bot.load_extension("cogs.join")
bot.load_extension("cogs.scream")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


bot.run(BOT_TOKEN)
