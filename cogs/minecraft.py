import client

import mcrcon as mcrcon
import socket, json, os, shutil, re, urllib

import discord
from discord.ext import commands, tasks

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class minecraftCog(commands.Cog):
    def __init__(self, bot):
        self.bot = client.bot
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

    @commands.command(name='mc')
    async def mc(self, ctx, *, command = None):
        """Sends commands to the Minecraft server""",
        sock.connect((socket.gethostbyname(client.guildData[f'{ctx.guild.id}']['settings']['minecraft']['ip']), client.guildData[f'{ctx.guild.id}']['settings']['minecraft']['rconPort']))
        mcrcon.login(sock, client.guildData[f'{ctx.guild.id}']['settings']['minecraft']['rconPassword'])

        mcrcon.command(sock, command)
        sock.close()

def setup(bot):
    bot.add_cog(minecraftCog(bot))

