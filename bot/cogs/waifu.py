import discord
from discord.ext import commands

import asyncio
import random
import time

import waifuim
from waifuim import WaifuAioClient

class Waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def helpdescription(self):
        await self.bot.wait_until_ready()
        rep=await self.bot.wf.endpoints(full=True)
        for c in self.walk_commands():
            for t in rep['sfw']:
                if t['name']==str(c.help.split(' ')[-1]) and t["is_nsfw"]==bool(int(c.help.split(' ')[0])):
                    if not c.parent:
                        c.description=random.choice(["True","1","0","False","false","true"])
                    c.help=f"""{t['description']}
You can see the image by clicking on the title if it do not load.
This will redirect you to the API website where you can also add the image to your favorite gallery :)"""
            for t in rep['nsfw']:
                if t['name']==str(c.help.split(' ')[-1]) and t["is_nsfw"]==bool(int(c.help.split(' ')[0])):
                    if not c.parent:
                        c.description=random.choice(["True","1","0","False","false","true"])
                    c.help=f"""{t['description']}
You can see the image by clicking on the title if it do not load.
This will redirect you to the API website where you can also add the image to your favorite gallery :)"""

    @staticmethod
    async def waifuim_request(ctx,type_,tag):
        start=time.perf_counter()
        info=await getattr(ctx.bot.wf,type_)(tag,raw=True)
        end=time.perf_counter()
        request_time=round(end-start,2)
        info=info["images"][0]
        embed = discord.Embed(colour=int(info["dominant_color"].replace("#",""),16))
        embed.set_author(name=f"{ctx.author.name}'s {tag.capitalize()} picture",url="https://waifu.im/preview/?image="+info["file"]+info["extension"])
        embed.set_image(url=info["url"])
        embed.set_footer(text=f"waifu.im | {request_time}s",icon_url=ctx.author.display_avatar.url)
        await ctx.message.reply(embed=embed)

    async def cog_command_error(self,ctx,error):
        if isinstance(error,waifuim.exceptions.APIException):
            await ctx.send(f"Oops an API error occured : `{error}`")
        elif isinstance(error,commands.NSFWChannelRequired):
            await ctx.send("I cannot Display **NSFW** content here !")
        else:
            await ctx.send(f"Oops an unexpected error occured : `{error}`")

    @commands.group(invoke_without_command=True)
    async def waifu(self,ctx):
        """0 waifu"""
        tag="waifu"
        await self.waifuim_request(ctx,'sfw',tag)
    
    @waifu.command()
    async def maid(self,ctx):
        """0 maid"""
        tag="maid"
        await self.waifuim_request(ctx,'sfw',tag)

    @waifu.command()
    @commands.is_nsfw()
    async def ero(self,ctx):
        """1 ero"""
        tag="ero"
        await self.waifuim_request(ctx,'nsfw',tag)

    @waifu.command()
    @commands.is_nsfw()
    async def hentai(self,ctx):
        """1 hentai"""
        tag="hentai"
        await self.waifuim_request(ctx,'nsfw',tag)

    @waifu.command()
    @commands.is_nsfw()
    async def paizuri(self,ctx):
        """1 paizuri"""
        tag="paizuri"
        await self.waifuim_request(ctx,'nsfw',tag)

    @waifu.command()
    @commands.is_nsfw()
    async def ecchi(self,ctx):
        """1 ecchi"""
        tag="ecchi"
        await self.waifuim_request(ctx,'nsfw',tag)

    @waifu.command(aliases=["hboobs","hboob"])
    @commands.is_nsfw()
    async def oppai(self,ctx):
        """1 ero"""
        tag="oppai"
        await self.waifuim_request(ctx,'nsfw',tag)
        
    @waifu.command()
    @commands.is_nsfw()
    async def hmaid(self,ctx):
        """1 maid"""
        tag="maid"
        await self.waifuim_request(ctx,'nsfw',tag)
        
    @waifu.command()
    @commands.is_nsfw()
    async def uniform(self,ctx):
        """1 uniform"""
        tag="uniform"
        await self.waifuim_request(ctx,'nsfw',tag)
        
    @waifu.command()
    @commands.is_nsfw()
    async def ass(self,ctx):
        """1 ass"""
        tag="ass"
        await self.waifuim_request(ctx,'nsfw',tag)
        
    @waifu.command()
    @commands.is_nsfw()
    async def milf(self,ctx):
        """1 milf"""
        tag="milf"
        await self.waifuim_request(ctx,'nsfw',tag)
        
    @waifu.command()
    @commands.is_nsfw()
    async def selfies(self,ctx):
        """1 selfies"""
        tag="selfies"
        await self.waifuim_request(ctx,'nsfw',tag)
        
    @waifu.command()
    @commands.is_nsfw()
    async def oral(self,ctx):
        """1 oral"""
        tag="oral"
        await self.waifuim_request(ctx,'nsfw',tag)


def setup(bot):
    bot.add_cog(Waifu(bot))