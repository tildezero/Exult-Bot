import discord
from discord.ext import commands

import urllib
import requests
import random
import json

from ast import literal_eval

from database.ai import aiDB

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.bid = ""
        self.key = ""
        self.uid = ""
        self.rapidkey = ""

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        x = await aiDB(self.bot.db).get()
        aichannels = literal_eval(x[0])
        if message.channel.id in aichannels:
            if len(message.attachments) > 0:
                return await message.channel.send("Please don't send files whilst interacting with me!")
            if "my name is" in message.content.lower() or "call me" in message.content.lower():
                return await message.channel.send("Very well.")
            url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"
            querystring = {"bid": f"{self.bid}", "key": f"{self.key}",
                        "uid": f"{self.uid}", "msg": f"{message.content}"}
            headersBrainShop = {
                'x-rapidapi-host': "acobot-brainshop-ai-v1.p.rapidapi.com",
                'x-rapidapi-key': f"{self.rapidkey}"
            }
            response = requests.request("GET", url, headers=headersBrainShop, params=querystring)
            if response.status_code != 200:
                return False
            await message.channel.send(json.loads(response.text)['cnt'])

    @commands.group(invoke_without_command=True)
    async def ai(self, ctx: commands.Context):
        channels = "**Channels currently set up with AI:\n\n**"
        x = await aiDB(self.bot.db).get()
        aichannels = literal_eval(x[0])
        for channel in ctx.guild.text_channels:
            if channel.id in aichannels:
                channels += f"{channel.mention}\n"
            else:
                pass
        if channels == "**Channels currently set up with AI:\n\n**":
            channels = f"There are currently no channels in this server with the AI function set up in. To set one up, do `{ctx.prefix}ai setup`!"
        else:
            channels += f"\nTo add more AI channels, simply do {ctx.prefix}ai start!"
        await ctx.message.reply(embed=discord.Embed(title="AI", description=channels, colour=self.bot.red))

    @ai.command(aliases=['setup'])
    async def start(self, ctx, channel: discord.TextChannel=None):
        channel = ctx.channel if channel is None else channel
        await aiDB(self.bot.db).add(channel.id)
        await ctx.message.reply(f"AI has been successfully set up in {channel.mention}!")

    @ai.command(aliases=['cancel', 'end'])
    async def stop(self, ctx, channel: discord.TextChannel=None):
        channel = ctx.channel if channel is None else channel
        await aiDB(self.bot.db).remove(channel.id)
        await ctx.message.reply(f"AI has been been removed from {channel.mention}!")

def setup(bot):
    bot.add_cog(AI(bot))