import client
import json
import urllib

import mcrcon
from mcrcon import MCRcon

import discord
from discord.ext import commands

class minecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='online')
    async def online(self, ctx, *, server=None):
        """Shows who's on the Minecraft server"""
        server = client.guildData[f'{ctx.guild.id}']['settings']['minecraft']['ip']

        existing = await ctx.channel.webhooks()

        with urllib.request.urlopen(f"https://api.mcsrvstat.us/2/{server}") as url:
            data = json.loads(url.read().decode())
            strdata = f"The following people are playing on {server}\n"

            for x in data['players']['list']:
                strdata = strdata + f"\n{x}"
        
        await client.embedSend(ctx, "Online Players", strdata, None)
        strdata = ""

    @commands.command(name='sendmc')
    async def sendmc(self, ctx, *, command = None):
        """Sends commands to the Minecraft server""",
        try:
            with MCRcon(f"{client.guildData[f'{ctx.guild.id}']['settings']['minecraft']['ip']}", f"{client.guildData[f'{ctx.guild.id}']['settings']['minecraft']['rconPassword']}") as mcr:
                resp = mcr.command(command)
                message = f"{command} sent to rcon on {mcr.host}:{mcr.port} with password {mcr.password}"

                await client.embedSend(ctx, "Minecraft Commands", message, None)
        except ConnectionRefusedError:
            await client.embedSend(ctx, "Minecraft Commands", "Unable to send connection refused", None)
        
def setup(bot):
    bot.add_cog(minecraftCog(bot))