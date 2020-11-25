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
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, time, *, reason):
        """Ban naughty memebers of your server"""
        reason = reason or "Reason not provided"

        if member == ctx.author:
            await client.embedSend(ctx.channel, "Error",
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

    @commands.command(name='setprefix')
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, *, prefix):
        """Changes the bot's prefix"""
        await client.embedSend(ctx, "Info", f"Prefix changed!",
                               f"Server prefix changed from {client.guildData['data'][f'{ctx.guild.id}']['settings']['prefix']} to {prefix}",
                               None)

        client.guildData['data'][f'{ctx.guild.id}']['settings']['prefix'] = prefix
        await client.writeData()

def setup(bot):
    bot.add_cog(moderationCog(bot))
