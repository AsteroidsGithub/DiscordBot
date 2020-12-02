import client
import json
import urllib

import discord
from discord.ext import commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.group()
    async def ticket(self, ctx):
        if ctx.invoked_subcommand is None:
            await client.embedSend(ctx, "Error", "Missing Sub-Command",
                    f"You are mssing a sub command", None)
    
    @ticket.command()
    async def open(self, ctx, *, name = None):
        size = str(f"{len(client.guildData['data'][f'{ctx.guild.id}']['tickets']) + 1}")
        guild = ctx.guild
        name = name or f"ticket-{size}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(name, overwrites=overwrites)
        client.guildData['data'][f'{ctx.guild.id}']['tickets'][f'{size}'] = {"name": f"{name}",
                                                                             "ticketId": size, 
                                                                             "channelId":channel.id, 
                                                                             "permissions": overwrites, 
                                                                             "members":[
                                                                                 {"id":ctx.auother.id}
                                                                                 ], 
                                                                             "messages": []
                                                                            }

def setup(bot):
    bot.add_cog(Tickets(bot))
