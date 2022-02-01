import discord
from discord.ext import commands
import kimetsu

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(slash_command=True, description="ban a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a user"""
        await kimetsu.Ban(ctx, member, reason, True).ban()

    @commands.command(slash_command=True, description="kick a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a user"""
        await kimetsu.Kick(ctx, member, reason, True).kick()

    @commands.command(slash_command=True, description="unban a user")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, *, reason=None):
        """Unban a user"""
        await kimetsu.Unban(ctx, member, reason).unban()

    @commands.group(aliases=['clear'], invoke_without_command=True, description="purge messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        """Purge messages"""
        await kimetsu.Purge(ctx).purge(amount)

    @purge.command(slash_command=True, description="purge messages from a member")
    @commands.has_permissions(manage_messages=True)
    async def member(self, ctx, member: discord.Member = None, amount: int = None):
        """Purge messages sent by a given member"""
        await kimetsu.Purge(ctx).member(member, amount)

    @purge.command(slash_command=True, description="purge bot messages")
    @commands.has_permissions(manage_messages=True)
    async def bot(self, ctx, amount: int = None):
        """Purge messages sent by bots"""
        await kimetsu.Purge(ctx).bot(amount)

    @purge.command(slash_command=True, description="purge maximum amount of messages (100)")
    @commands.has_permissions(manage_messages=True)
    async def max(self, ctx):
        """Purge maximum amount of messages (100)"""
        await kimetsu.Purge(ctx).max()

    @purge.command(slash_command=True, description="purge after a message")
    @commands.has_permissions(manage_messages=True)
    async def after(self, ctx, message_id=None):
        """Delete messages after a given message id"""
        await kimetsu.Purge(ctx).after(message_id)

    @purge.command(slash_command=True, description="purge before a message")
    @commands.has_permissions(manage_messages=True)
    async def before(self, ctx, message_id=None):
        """Purge messages before a given message"""
        await kimetsu.Purge(ctx).before(message_id)

    @commands.group(invoke_without_command=True, description="command group for slowmode")
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx):
        pass
    
    @slowmode.command(slash_command=True, description="enable slowmode in a channel")
    @commands.has_permissions(manage_messages=True)
    async def on(self, ctx, time=None):
        """Enable slowmode in a channel"""
        await kimetsu.Slowmode(ctx).on(time)

    @slowmode.command(slash_command=True, description="disable slowmode in a channel")
    @commands.has_permissions(manage_channels=True)
    async def off(self, ctx):
        """Disable slowmode in a channel"""
        await kimetsu.Slowmode(ctx).off()

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration, *, reason=None):
        """Put a member in timeout"""
        await kimetsu.Timeout(ctx, member, duration, reason, True).timeout()

    @timeout.command()
    @commands.has_permissions(moderate_members=True)
    async def off(self, ctx, member: discord.Member, *, reason=None):
        """Disable a member's timeout"""
        await kimetsu.Timeout(ctx, member, "", reason, True).off()

    @commands.command(aliases=['uto', 'unmute'])
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member, *, reason=None):
        """Disable a member's timeout"""
        await kimetsu.Timeout(ctx, member, "", reason, True).off()

    @commands.command(aliases=['nick'])
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, name=None):
        if name == None:
            await member.edit(nick=None)
            return await ctx.send(f"succesfully reset the nickname of {str(member)}!")
        if len(name) < 2 or len(name) > 32:
            return await ctx.send("error: this nick is too long!")
        else:
            await member.edit(nick=name)
            await ctx.send(f"succesfully changed the nick of {str(member)} to {name}!")
        

    

def setup(bot):
    bot.add_cog(Moderation(bot))
