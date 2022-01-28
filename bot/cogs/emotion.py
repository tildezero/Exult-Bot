from ast import literal_eval
import discord
from discord.ext import commands

import requests

from database.marriage import marriageDB

class Emotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = marriageDB(bot.db)

    def get_link(self, endpoint):
        r = requests.get(f"https://neko-love.xyz/api/v1/{endpoint}")
        return r.json()["url"]

    @commands.command()
    async def kiss(self, ctx, member:discord.Member):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} kisses {member.name}", colour=self.bot.red).set_image(url=self.get_link("kiss")))

    @commands.command()
    async def hug(self, ctx, member:discord.Member):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} hugs {member.name}", colour=self.bot.red).set_image(url=self.get_link("hug")))

    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} pats {member.name}", colour=self.bot.red).set_image(url=self.get_link("pat")))

    @commands.command()
    async def cry(self, ctx):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} cried", colour=self.bot.red).set_image(url=self.get_link("cry")))

    @commands.command()
    async def smug(self, ctx):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} is smug", colour=self.bot.red).set_image(url=self.get_link("smug")))

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} slapped {member.name}", colour=self.bot.red).set_image(url=self.get_link("slap")))

    @commands.command()
    async def punch(self, ctx, member: discord.Member):
        await ctx.send(embed=discord.Embed(title=f"{ctx.author.name} punched {member.name}", colour=self.bot.red).set_image(url=self.get_link("punch")))

    @commands.command()
    async def marry(self, ctx, member: discord.Member):
        check_existing = await self.db.check_existing(ctx.author.id, member.id)
        if type(check_existing) == str:
            return await ctx.send(check_existing)
        await ctx.send(f"{member.mention} do you want to marry {ctx.author.mention}? `(yes/no)`\nYou have 15 seconds to accept!")
        check = lambda m: m.author.id == member.id and m.channel.id == ctx.channel.id
        msg = await self.bot.wait_for('message', timeout=15.0, check=check)
        loop = True
        while loop:
            if "y" in msg.content.lower():
                await self.db.add(ctx.author.id, member.id)
                await ctx.send(f"🥳 {ctx.author.mention} ❣ {member.mention} 🥳")
                loop = False
            elif "n" in msg.content.lower():
                await ctx.send(f"My condolences, {ctx.author.mention}. 💔")
                loop = False
            else:
                loop = True

    @commands.group(invoke_without_command=True)
    async def divorce(self, ctx, member: discord.Member):
        marriages = await self.db.get(ctx.author.id)
        marriages = literal_eval(marriages[0])
        if member.id in marriages:
            await self.db.remove(ctx.author.id, member.id)
            await ctx.send(f"You have divorced {member.mention} 💔")
        else:
            await ctx.send("You are not married to this user!")

    @divorce.command()
    async def all(self, ctx):
        sql = await self.db.removeall(ctx.author.id)
        if type(sql) == str:
            await ctx.send(sql)
        else:
            await ctx.send("Divorced all marriages 💔")

    @commands.command()
    async def marriages(self, ctx, member: discord.Member=None):
        member = ctx.author if member is None else member
        marriages = await self.db.get(ctx.author.id)

def setup(bot):
    bot.add_cog(Emotion(bot))
