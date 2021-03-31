import client

from mctools import RCONClient
import socket, json, os, shutil, re, urllib

import discord
from discord.ext import commands, tasks

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = client.bot
        self._last_member = None

    @commands.command(name='online')
    async def online(self, ctx, *, server=None):
        """Shows who's on the Minecraft server"""
        server = server or client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['ip']

        existing = await ctx.channel.webhooks()

        with urllib.request.urlopen(f"https://api.mcsrvstat.us/2/{server}") as url:
            data = json.loads(url.read().decode())
            strdata = f"The following people are playing on {server}\n"
            
            try: 
                for x in data['players']['list']:
                    strdata = strdata + f"\n`{x}`"
            except KeyError:
                await client.embedSend(ctx, "Info", "Online Players", f"No one is playing on {server}", None)
                return
        
        await client.embedSend(ctx, "Info", "Online Players", strdata, None)
        strdata = ""

    @commands.command(name='mc')
    # @commands.has_permissions(administrator=True)
    async def mc(self, ctx, *, command):
        """Sends commands to the Minecraft server"""
        rcon = RCONClient(client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['ip'], port=client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['rconPort'])
        if rcon.login(client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['rconPassword']):
            resp = rcon.command(f"{command}")
            await client.embedSend(ctx, "Good", "Minecraft Command Sent", f"sent '{command}' to the mc server", None)
        else:
            await client.embedSend(ctx, "Error", "Minecraft Command Failed", f"failed to send '{command}' to the mc server", None)
        rcon.stop()

    @mc.error
    async def mcError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await client.embedSend(ctx, "Error", "Missing Permissions",
                    f"You are mssing the following permissions: `Administrator`", None)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await client.embedSend(ctx, "Error", "Missing Arguments", f"You are mssing the following arguments: `<command>`", None)
            return

def setup(bot):
    bot.add_cog(Minecraft(bot))

