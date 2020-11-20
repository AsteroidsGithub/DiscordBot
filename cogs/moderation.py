import client
import json
import urllib

import discord
from discord.ext import commands

class moderationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='ban')
    @commands.has_role('Developers')
    async def ban(self, ctx, member: discord.Member, time, *, reason):
        """Ban naughty memebers of your server"""
        reason = reason or "Reason not provided"

        if member == ctx.author:
            await client.embedSend(ctx.channel,
                                   "Woah, there!",
                                   f"{ctx.author.mention} You cannot ban yourself",
                                   member.avatar_url_as(format=None, static_format='png', size=1024))

        messageok = f"You have been banned from {ctx.guild.name} for {reason}"

        await client.embedSend(ctx,
                               "Smashed with the Ban Hammer",
                               f"I have banned {member.name} for {reason} it will last {str(time)}h",
                               member.avatar_url_as(format=None, static_format='png', size=1024))

        dm = await member.create_dm()
        await dm.send(messageok)

        await member.ban(reason=reason)

    @commands.command(name='unban')
    @commands.has_role('Developers')
    async def unban(self, ctx, id):
        member = await self.bot.fetch_user(id)

        link = await ctx.channel.create_invite(max_age=300)
        await ctx.guild.unban(member)

        dm = await member.create_dm()
        await dm.send(f"Hello {member.name}, you have been unbanned from {ctx.guild.name}. Welcome back here's a invite {link}")

        await client.embedSend(ctx,
                                "Forgiveness is best",
                                f"I have unbanned {member.name} because they are good",
                                member.avatar_url_as(format=None, static_format='png', size=1024))

    @commands.command(name='listrole')
    @commands.has_role("Developers")
    async def listrole(self, ctx, *, role: discord.Role):
        """Show how many people have a given Role"""
        memberlist = ""

        for member in role.members:
            memberlist = memberlist + f"\n{member}"

        await client.embedSend(ctx, f"Member's with the Role: {role.name}",
                               f'The following {len(role.members)} people have the Role: {role.name}, \n{memberlist}',
                               None)

    @commands.command(name='setprefix')
    @commands.has_role("Developers")
    async def setprefix(self, ctx, *, prefix):
        """Changes the bot's prefix"""
        await client.embedSend(ctx, f"Prefix changed!",
                               f"Server prefix changed from {client.guildData[f'{ctx.guild.id}']['settings']['prefix']} to {prefix}",
                               None)

        client.guildData[f'{ctx.guild.id}']['settings']['prefix'] = prefix

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        role = member.server.roles['Viewers']
        await member.add_roles(member, role)


def setup(bot):
    bot.add_cog(moderationCog(bot))
