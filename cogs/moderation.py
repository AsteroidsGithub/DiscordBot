import bot
import json
import urllib

import discord
from discord.ext import commands

class moderationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='listrole')
    @commands.has_role("Developers")
    async def listrole(self, ctx, *, role: discord.Role):
        memberlist = ""

        for member in role.members:
            memberlist = memberlist + f"\n{member}"

        await bot.webhookSend(ctx, f"Member's with the Role: {role.name}",
            f'The following people have the Role: {role.name}, \n{memberlist}',
            None)

    776601394697469997

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        member = ctx.author
        role = member.server.roles['Viewers']
        await bot.add_roles(member, role)
        
def setup(bot):
    bot.add_cog(moderationCog(bot))