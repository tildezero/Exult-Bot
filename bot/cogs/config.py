import discord
from discord.ext import commands
from kimetsu import embed
Embed = embed.Embed.embed

import json
from database.event import EventDB
from database.cases import CasesDB

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = discord.Embed(
                title="An Unexpected Error Occurred!",
                description=f"""
                ```cmd
                {error.original}
                ```
                """,
                colour=0xef534e
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="An Unexpected Error Occurred!",
                description=f"""
                ```cmd
                retry after: {error.retry_after} seconds
                ```
                """,
                colour=0xef534e
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="An Unexpected Error Occurred!",
                description=f"""
                ```cmd
                {error.message}
                ```
                """,
                colour=0xef534e
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def botnick(self, ctx, *, nickname: str=None):
        if nickname is None:
            return await ctx.send(embed=discord.Embed(description=f"My nickname is **{ctx.guild.me.display_name}**!", colour=self.bot.red))
        oldnick = ctx.guild.me.display_name
        if nickname.lower() == "reset":
            nickname = self.bot.user.name
        await ctx.guild.me.edit(nick=nickname)
        await ctx.send(embed=discord.Embed(description=f"Successfully changed my nickname from **{oldnick}** -> **{nickname}**!", colour=discord.Colour.green()))

def setup(bot):
    bot.add_cog(Config(bot))
