import os
import sys
import traceback

import asyncio


import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands

import store

token = os.getenv("DISCORD_BOT_TOKEN")
api_key = os.getenv("JSON_STORE_API")

bot = commands.Bot(command_prefix="r!", intents=discord.Intents.all())
discord_data = store.Data(bot, "DiscordBot", api_key)

def init():
    for ext in ['cogs.setup','cogs.msuic', 'cogs.minecraft', 'cogs.fun']:
        bot.load_extension(ext)
        print(f"{ext} Has been loaded.")
        

    bot.run(token)

    discord_data.check_guilds()
    print(bot.guilds)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.CustomActivity(name='Policing OutpostMC'))

init()

