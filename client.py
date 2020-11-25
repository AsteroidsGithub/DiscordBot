import requests

import json
import urllib
import urllib.parse as urlparse
import sys, os, traceback
import asyncio, datetime

import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands

def prefix(bot, message):
    id = message.guild.id
    try:
        return guildData['data'][f'{id}']['settings']['prefix']
    except KeyError:
        return "!"

token = os.getenv("DISCORD_BOT_TOKEN")
apiKey = os.getenv("JSON_STORE_API")

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
storeName = 'DiscordBot'

res = requests.get(f'https://json.psty.io/api_v1/stores/{urlparse.quote_plus(storeName)}', headers={'Api-Key':f'{apiKey}'}).text
guildData = json.loads(res)

extensions = [
    "cogs.levels",
    "cogs.moderation", 
    "cogs.minecraft"
  ]

for extension in extensions:
    print(f"Loaded {extension}")
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Game(name='Whimcraft.xyz'))
    
    await writeServer(bot)

@bot.event
async def on_guild_join(guild):
    writeServer()

async def writeData():
    print(f"Saved Data:\n{guildData}")
    res = requests.put(f'https://json.psty.io/api_v1/stores/{storeName}', headers={'Api-Key':f'{apiKey}','Content-Type':'application/json'}, data=json.dumps(guildData['data']))

async def writeServer(bot):
    for guild in bot.guilds:
        try:
            print(guildData['data'][f'{guild.id}'])
        except KeyError:
            guildData['data'][f'{guild.id}'] = {
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
            await writeData()

async def embedSend(ctx, type, title, data, thumbnail):
    if type == "Error":
        color = 0xff1100
    elif type == "Good":
        color = 0x27db1d
    elif type == "Info":
        color = 0x008cff

    embed = discord.Embed(title=title, description=data, colour=color)

    embed.set_author(name=f"{guildData['data'][f'{ctx.channel.guild.id}']['serverName']}",
                     icon_url=guildData['data'][f'{ctx.channel.guild.id}']['serverIcon'])
                     
    time = datetime.datetime.now()                  
    embed.set_footer(text=f"Sent by {ctx.author.name} at {time.strftime('%I:%M%p %x')}")
    if thumbnail != None:
        embed.set_thumbnail(url=thumbnail)

    await ctx.channel.send(embed=embed)
    
@bot.event
async def on_command_error(self, ctx, error):
    # get the original exception
    error = getattr(error, 'original', error)
    
    if isinstance(error, commands.MissingPermissions):
        missing =""
        for perm in error.missing_perms:
            print(perm)
            missing = missing + f"{perm}\n"

        embedSend(ctx, "Error", "Missing Permissions", f"You are mssing the following perms: \n{missing}", None)
        return
    
    if isinstance(error, commands.MissingRequiredArgument):
        missing =""
        for argue in error.param:
            print(argue)
            missing = missing + f"{argue}\n"
            
        embedSend(ctx, "Error", "Missing Arguments", f"You are mssing the following arguments: \n{missing}", None)
        return

bot.run(token)