import client
import json
import urllib

import discord
from discord.ext import commands

class Settings(commands.Cog):
      def __init__(self, bot):
          self.bot = bot
          self._last_member = None

      @commands.command()
      async def ping(self, ctx):
          await ctx.send(f'Pong! {round(client.latency, 1)}')
  
      @commands.has_permissions(manage_guild=True)
      @commands.group()
      async def set(self, ctx):
          if ctx.invoked_subcommand is None:
              await client.embedSend(ctx, "Error", "Missing Sub-Command",
                      f"You are mssing a sub command", None)
      
      @set.command()
      async def prefix(self, ctx, *, prefix):
          """Changes the bot's prefix"""
          await client.embedSend(ctx, "Info", f"Prefix changed!",
                                 f"Server prefix changed from {client.guildData['data'][f'{ctx.guild.id}']['settings']['prefix']} to {prefix}",
                                 None)
  
          client.guildData['data'][f'{ctx.guild.id}']['settings']['prefix'] = prefix
          await client.writeData()
  
      @set.command()
      async def rconPassword(self, ctx, *, password):
          """Changes the bot's Rcon Password"""
          await client.embedSend(ctx, "Info", f"Password changed!",
                                 f"Server prefix changed from ||{client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['rconPassword']}|| to ||{password}||",
                                 None)
  
          client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['rconPassword'] = password
          await client.writeData()
  
      @set.command()
      async def ip(self, ctx, *, ip):
          """Changes the bot's ip"""
          await client.embedSend(ctx, "Info", f"IP changed!",
                                 f"Server prefix changed from {client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['ip']} to {ip}",
                                 None)
  
          client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['ip'] = ip
          await client.writeData()
  
      @set.command()
      async def rconPort(self, ctx, *, port):
          """Changes the bot's Rcon Port"""
          await client.embedSend(ctx, "Info", f"Port changed!",
                                 f"Server prefix changed from ||{client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['rconPort']}|| to ||{port}||",
                                 None)
  
          client.guildData['data'][f'{ctx.guild.id}']['settings']['minecraft']['rconPort'] = port
          await client.writeData()
  
      @set.error
      async def setError(self, ctx, error):
          if isinstance(error, commands.MissingPermissions):
              await client.embedSend(ctx, "Error", "Missing Permissions",
                      f"You are mssing the following permissions: `Ban Members`", None)
              return
  
          if isinstance(error, commands.MissingRequiredArgument):
              await client.embedSend(ctx, "Error", "Missing Arguments", f"You are mssing the following arguments: `<member>`", None)
              return

def setup(bot):
    bot.add_cog(Settings(bot))
