import game
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('The bot has logged in as {0.user}'.format(client))

@client.command()
async def startGame(client, players):

    await client.send(game.start(players))

client.run("NzM5OTk2NTg1NTM0MDI5ODI0.Xyilhg.SA89Gj-w2o288X5l7DFjuOQj9qg")