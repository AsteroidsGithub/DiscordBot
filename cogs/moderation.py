import client
import json
import urllib

import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='listrole')
    @commands.has_permissions(manage_roles=True)
    async def listrole(self, ctx, *, role: discord.Role):
        """Show how many people have a given Role"""
        memberlist = ""

        for member in role.members:
            memberlist = memberlist + f"\n{member}"

        await client.embedSend(ctx,"Info", f"Member's with the Role: {role.name}",
                               f'The following {len(role.members)} people have the Role: {role.name}, \n{memberlist}',
                               None)

def setup(bot):
    bot.add_cog(Moderation(bot))
