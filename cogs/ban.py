import client
import json
import urllib

import discord
from discord.ext import commands

class banCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, time, *, reason):
        """Ban naughty memebers of your server"""
        reason = reason or "Reason not provided"

        if member == ctx.author:
            await client.embedSend(ctx, "Error",
                                   "Woah, there!",
                                   f"{ctx.author.mention} You cannot ban yourself",
                                   member.avatar_url_as(format=None, static_format='png', size=1024))

        messageok = f"You have been banned from {ctx.guild.name} for {reason}"

        await client.embedSend(ctx, "Good",
                               "Smashed with the Ban Hammer",
                               f"I have banned {member.name} for {reason} it will last {str(time)}h",
                               member.avatar_url_as(format=None, static_format='png', size=1024))

        await member.send(messageok)
        await member.ban(reason=reason)

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id):
        member = await self.bot.fetch_user(id)

        link = await ctx.channel.create_invite(max_age=300)
        await ctx.guild.unban(member)

        await client.embedSend(ctx, "Good",
                                "Forgiveness is best",
                                f"I have unbanned {member.name} because they are good",
                                member.avatar_url_as(format=None, static_format='png', size=1024))

        await member.send(f"Hello {member.name}, you have been unbanned from {ctx.guild.name}. Welcome back here's a invite {link}")

    @ban.error
    async def banError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await client.embedSend(ctx, "Error", "Missing Permissions",
                    f"You are mssing the following permissions: `Ban Members`", None)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await client.embedSend(ctx, "Error", "Missing Arguments", f"You are mssing the following arguments: <member> <time> <reason>", None)
            return
    
    @unban.error
    async def banError(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await client.embedSend(ctx, "Error", "Missing Permissions",
                    f"You are mssing the following permissions: `Ban Members` `Manage Members`", None)
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await client.embedSend(ctx, "Error", "Missing Arguments", f"You are mssing the following arguments: <id>", None)
            return

def setup(bot):
    bot.add_cog(banCog(bot))
