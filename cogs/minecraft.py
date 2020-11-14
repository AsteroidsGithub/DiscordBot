import bot
import json
import urllib

import discord
from discord.ext import commands

class minecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='online')
    async def online(self, ctx, *, server=None):
        server = bot.botData[f'{ctx.guild.id}']['settings']['ip']

        existing = await ctx.channel.webhooks()

        with urllib.request.urlopen(f"https://api.mcsrvstat.us/2/{server}") as url:
            data = json.loads(url.read().decode())
            strdata = ""

            for x in data['players']['list']:
                strdata = strdata + f"\n{x}"
        
        await bot.webhookSend(ctx, "Online Players", strdata, None)
        strdata = ""
        
def setup(bot):
    bot.add_cog(minecraftCog(bot))