import client
import json
import urllib

import discord
from discord.ext import commands

class LevelsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        try:
            level = int(client.guildData['data'][f'{ctx.guild.id}']['levels'][f'{ctx.author.id}']['level'])
        except KeyError:
            level = 0

        try:
            score = int(client.guildData['data'][f'{ctx.guild.id}']['levels'][f'{ctx.author.id}']['score']) + 1
        except KeyError:
            score = 1

        client.guildData['data'][f'{ctx.guild.id}']['levels'][f'{ctx.author.id}'] = {"name":f"{ctx.author.name}", "score":f"{score}", "level":F"{level}"}

        levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 250, 500]
        lvl = len([x for x in levels if score > x])

        if lvl > level:
            await client.embedSend(ctx, "Level Up", f'Hello {ctx.author.name}, you have gone up to level {lvl}', ctx.author.avatar_url_as(format=None, static_format='png', size=1024))
            client.guildData['data'][f'{ctx.guild.id}']['levels'][f'{ctx.author.id}']['level'] = f"{lvl}"
        else:
            return
        await client.writeData()


    @commands.command()
    async def level(self, ctx, *, member: discord.Member = None):
        """Shows you or your friends level on this server"""
        member = member or ctx.author

        await client.embedSend(ctx, f"{member.name}'s Level", f'Hello {member.name}, you have {client.guildData["data"][f"{ctx.guild.id}"]["levels"][f"{member.id}"]["score"]} points in total and are at level {client.guildData["data"][f"{ctx.guild.id}"]["levels"][f"{member.id}"]["level"]}', member.avatar_url_as(format=None, static_format='png', size=1024))

def setup(bot):
    bot.add_cog(LevelsCog(bot))
