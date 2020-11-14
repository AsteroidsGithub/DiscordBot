import requests

import json
import urllib
import sys
import traceback
import os
import asyncio

import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands

def prefix(bot, message):
    id = message.guild.id
    try:
        return botData[f'{id}']['settings']['prefix']
    except KeyError:
        return "!"

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
botData = json.load(open("data.json", "r"))

botIcon = "https://cdn.discordapp.com/attachments/773578698611752980/775151203381542922/WHIMPLEX.png"
serverURL = "https://api.mcsrvstat.us/2/whimcraft.xyz"

initial_extensions = ['cogs.levels',
                      'cogs.moderation',
                      'cogs.minecraft']

for extension in initial_extensions:
    print(f"Loaded {extension}")
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='Whimplex.xyz'))

    for guild in bot.guilds:
        try:
            print(botData[f'{guild.id}'])
        except KeyError:
            writeServer(bot)

    await writeData()

@bot.event
async def on_guild_join(guild):
    botData[f'{guild.id}'] = {
                "serverName": f"{guild.name}",
                "serverIcon": f"{guild.icon_url_as(format=None, static_format='png', size=1024)}",
                "settings": {
                    "ip": "whimcraft.xyz",
                    "prefix": "!"
                },
                "levels": {
                }
            }

async def writeData():
    while True:
        await asyncio.sleep(10)
        with open("data.json", "w") as f:
            dumped = json.dumps(botData)
            f.write(dumped)
            f.close()

async def writeServer(bot):
    for guild in bot.guilds:
        try:
            print(botData[f'{guild.id}'])
        except KeyError:
            botData[f'{guild.id}'] = {
                "serverName": f"{guild.name}",
                "serverIcon": f"{guild.icon_url_as(format=None, static_format='png', size=1024)}",
                "settings": {
                    "ip": "whimcraft.xyz",
                    "prefix": "!"
                },
                "levels": {
                }
            }

async def webhookSend(ctx, title, data, thumbnail):
    webhook = await ctx.channel.create_webhook(name="Minecraft")
    embed = discord.Embed(title=title, description=data, colour=discord.Colour.blue())

    embed.set_author(name=f"{botData[f'{ctx.channel.guild.id}']['serverName']}",
                     icon_url=botData[f'{ctx.channel.guild.id}']['serverIcon'])

    if thumbnail != None:
        embed.set_thumbnail(url=thumbnail)

    await webhook.send(username="Whimplex Bot", avatar_url=botIcon,
                       embed=embed)
    await webhook.delete()

bot.run("NzM5OTk2NTg1NTM0MDI5ODI0.Xyilhg.SA89Gj-w2o288X5l7DFjuOQj9qg")