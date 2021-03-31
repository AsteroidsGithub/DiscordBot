import asyncio
import random

import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.nword = {"id":"6"}
    
    

    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context):
        print("l")
        if "nigga" in ctx.Message or "nigger" in ctx.Message or "Nigga" in ctx.Message or "Nigger" in ctx.Message:
            self.nword[f'{user.id}'] += 1
    
    @commands.command(name='kill')
    async def _kill(self, ctx: commands.Context, user: discord.User, *, method = None):
        """ Kills the User provided using a random method """
        methods = ["A Sword", "HarmlessBird's Body Odor", "The Block Of Peace", "The Sun Gods"]

        method = method or random.choice(methods)

        await ctx.send("{} Has killed {} Using {}".format(ctx.author.name, user.name, method))

    @commands.command(name='nword')
    async def _nigga(self, ctx: commands.Context, user: discord.User = None):
        user = user or ctx.author
        try:
            await ctx.send("{} has said the N Word {} times".format(user, self.nword[f'{user.id}']))
        except KeyError:
            self.nword[f'{user.id}'] = 0
            await ctx.send("{} has said the N Word {} times".format(user, self.nword[f'{user.id}'])) 

def setup(bot):
    bot.add_cog(Fun(bot))