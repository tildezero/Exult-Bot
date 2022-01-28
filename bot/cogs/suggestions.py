from email.utils import parsedate
import discord
from discord.ext import commands
from kimetsu import parsedate

from database.suggestions import SuggestDB
from tools.components import SuggestVotes, SuggestSafeDecision


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = SuggestDB(bot.db)

    @commands.command()
    @commands.is_owner()
    #@commands.cooldown(1, 60, commands.BucketType.user)
    async def suggest(self, ctx, *, suggestion: str):
        if ctx.guild.id == 912148314223415316:
            guildconf = await self.db.getconf(ctx.guild.id)
            if not guildconf:
                return await ctx.send(embed=discord.Embed(description=f"Oops! Seems like this server doesn't have my suggestions module enabled! To enable it, simply do `{ctx.prefix}config suggestions`!", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Config"))
            channel_id = guildconf[0]
            safemode = guildconf[1]
            await self.db.add(ctx.guild.id, ctx.message.author.id, suggestion)
            data = await self.db.get_id(ctx.guild.id, ctx.message.author.id)
            suggestion_id = data[-1][0]
            suggestion += f"\n\nSuggested at {parsedate.Parsedate(discord.utils.utcnow()).parsedate()}"
            embed = discord.Embed(description=suggestion, colour=self.bot.red).set_author(icon_url=ctx.message.author.avatar.url, name=f"Suggestion from {ctx.message.author}").set_footer(icon_url=ctx.guild.icon.url, text=f"Suggsetion ID: {suggestion_id}").set_thumbnail(url=ctx.author.avatar.url)
            if safemode:
                channel = ctx.guild.get_channel(safemode)
                view = SuggestSafeDecision()
            else:
                channel = ctx.guild.get_channel(channel_id)
                view = SuggestVotes()
            await channel.send(embed=embed, view=view)

    
def setup(bot):
    bot.add_cog(Suggestions(bot))