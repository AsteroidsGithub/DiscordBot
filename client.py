import requests

import json
import urllib
import sys
import traceback
import os
import asyncio
import datetime

import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands

def prefix(bot, message):
    id = message.guild.id
    try:
        return guildData[f'{id}']['settings']['prefix']
    except KeyError:
        return "!"

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

guildData = json.load(open("data.json", "r"))
botConfig = json.load(open("bot.json", "r"))

for extension in botConfig['extensions']:
    print(f"Loaded {extension}")
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='whimplex.xyz on Minecraft 1.16.3'))
    
    await writeServer(bot)
    await writeData()

@bot.event
async def on_guild_join(guild):
    writeServer()

async def writeData():
    while True:
        await asyncio.sleep(10)
        with open("data.json", "w") as f:
            dumped = json.dumps(guildData)
            f.write(dumped)
            f.close()

async def writeServer(bot):
    for guild in bot.guilds:
        try:
            print(guildData[f'{guild.id}'])
        except KeyError:
            guildData[f'{guild.id}'] = {
                "serverName": f"{guild.name}",
                "serverIcon": f"{guild.icon_url_as(format=None, static_format='png', size=1024)}",
                "settings": {
                    "minecraft": {
                        "ip": "whimcraft.xyz",
                        "rconPort": 25575,
                        "rconPassword":"password"
                    },
                    "prefix": "!"
                },
                "levels": {
                }
            }

async def embedSend(ctx, title, data, thumbnail):
    embed = discord.Embed(title=title, description=data, colour=discord.Colour.blue())

    embed.set_author(name=f"{guildData[f'{ctx.channel.guild.id}']['serverName']}",
                     icon_url=guildData[f'{ctx.channel.guild.id}']['serverIcon'])
                     
    time = datetime.datetime.now()                  
    embed.set_footer(text=f"Sent by {ctx.author.name} at {time.strftime('%I:%M%p %x')}")
    if thumbnail != None:
        embed.set_thumbnail(url=thumbnail)

    await ctx.send(embed=embed)

bot.run(botConfig['token'])