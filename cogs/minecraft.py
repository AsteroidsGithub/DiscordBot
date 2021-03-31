import client

import socket, json, os, shutil, re, urllib

import discord
from discord.ext import commands, tasks

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='online')
    async def online(self, ctx, *, server=None):
        """Shows who's on the Minecraft server"""
        server = server or "HorizonsSMP.apexmc.co"

        with urllib.request.urlopen(f"https://api.mcsrvstat.us/2/{server}") as url:
            data = json.loads(url.read().decode())
            strdata = f"The following people are playing on {server}\n"
            
            try: 
                for x in data['players']['list']:
                    strdata = strdata + f"\n`{x}`"
            except KeyError:
                await ctx.send("There is nobody playing on '{}'".format(server))
                return
        
        await ctx.send(strdata)
        strdata = ""

def setup(bot):
    bot.add_cog(Minecraft(bot))

