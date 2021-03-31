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

guildData = json.loads(requests.get(f'https://json.psty.io/api_v1/stores/{urlparse.quote_plus("DiscordBot")}', headers={'Api-Key':f'{apiKey}'}).text)

extensions = [
    "cogs.levels",
    "cogs.moderation", 
    "cogs.minecraft",
    "cogs.ban",
    "cogs.settings",
    "cogs.tickets"
  ]

def init():
    pass

for extension in extensions:
    print(f"Loaded {extension}")
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.CustomActivity(name='Policing OutpostMC'))
    
    await writeServer(bot)

@bot.event
async def on_guild_join(guild):
    writeServer()

async def writeData():
    print(f"Saved Data:\n{guildData}")
    requests.put(f'https://json.psty.io/api_v1/stores/{storeName}', headers={'Api-Key':f'{apiKey}','Content-Type':'application/json'}, data=json.dumps(guildData['data']))

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
                    "prefix": "r!"
                },
                "levels": {
                },
                "tickets": {

                }

            }
            await writeData()

async def embedSend(ctx, title, data, thumbnail, image=none, color:int = none):
    """ Sends Message as a embed """
    color = color or 0x008cff
    image = image or None

    embed = discord.Embed(title=title, description=data, colour=color)

    embed.set_author(name=f"{guildData['data'][f'{ctx.channel.guild.id}']['serverName']}",
                     icon_url=guildData['data'][f'{ctx.channel.guild.id}']['serverIcon'])
    
    embed.set_image(image)
                     
    time = datetime.datetime.now()                  
    embed.set_footer(text=f"Sent by {ctx.author.name} at {time.strftime('%I:%M%p %x')}")
    if thumbnail != None:
        embed.set_thumbnail(url=thumbnail)

    await ctx.channel.send(embed=embed)

@bot.command()
async def embedpages(ctx):
    page1=discord.Embed(
        title='Page 1/3',
        description='Description',
        colour=discord.Colour.orange()
    )
    page2=discord.Embed(
        title='Page 2/3',
        description='Description',
        colour=discord.Colour.orange()
    )
    page3=discord.Embed(
        title='Page 3/3',
        description='Description',
        colour=discord.Colour.orange()
    )
    reactions = ['⏮', '◀', '\u25b6', '\u23ed']

    pages=[page1,page2,page3]

    message=await ctx.channel.send(embed=page2)

    for emoji in reactions:
        await message.add_reaction(emoji)

    i=1
    while True:
        reaction, user = await bot.wait_for('reaction_add')
        print(reaction)

        if user.bot:
            continue

        if reaction.emoji == reactions[0]:
            i=0
            await message.edit(embed=pages[i])
            await message.remove_reaction(reaction, user)
        elif reaction.emoji == reactions[1]:
            if i>0:
                i-=1
                await message.edit(embed=pages[i])
                await message.remove_reaction(reaction, user)
        elif reaction.emoji == reactions[2]:
            if i<2:
                i+=1
                await message.edit(embed=pages[i])
                await message.remove_reaction(reaction, user)
        elif reaction.emoji == reactions[3]:
            i=2
            await message.edit(embed=pages[i])
            await message.remove_reaction(reaction, user)
        

    await bot.clear_reactions(message)
bot.run(token)
