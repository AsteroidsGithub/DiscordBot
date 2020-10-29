import discord
from discord.ext import commands

client = commands.Bot(command_prefix='?')

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member

    @commands.command()
    async def cig(self, ctx, member: discord.Member):
        """Give a friend a Cigi"""
        if member == None:
            await ctx.send(f'{ctx.author.name} gave themselves a Cigi')
        else:
            await ctx.send(f'{ctx.author.name} gave {member.name} a Cigi')

client.add_cog(Greetings(client))

client.run("NzM5OTk2NTg1NTM0MDI5ODI0.Xyilhg.SA89Gj-w2o288X5l7DFjuOQj9qg")