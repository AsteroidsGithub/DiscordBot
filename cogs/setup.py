import asyncio
import random

import discord
from discord.ext import commands

class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='status')
    async def _status(self, ctx: commands.Context, type, *, status):
        """ Changes the status of the bot """
        if type == "watching":
            type = discord.ActivityType.watching
        elif type == "listening":
            type = discord.ActivityType.listening
        elif type == "playing":
            type = discord.ActivityType.playing
        else:
            await ctx.send("Failed")
            return

        await self.bot.change_presence(activity=discord.Activity(type=type, name="{}".format(status)))
        await ctx.send("Status changed to '{}'".format(status))

def setup(bot):
    bot.add_cog(Setup(bot))