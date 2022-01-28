import discord
from discord.ext import commands
from kimetsu import embed
Embed = embed.Embed.embed

from database.prefix import PrefixDB
from database.suggestions import SuggestDB
from tools.components import (
    SuggestConfCatView, 
    SuggestConfChanView,
    SuggestConfSafeCat,
    SuggestConfSafeChan, 
    SuggestConfSafemode,
    SuggestConfCatSafeView,
    SuggestConfChanSafeView)

class ConfigCMD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['settings', 'conf'], invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel", description="✅ = Completed, ❎ = In progress, ❌ = Not started", colour=self.bot.red)
            embed.add_field(name="Bot Settings ❎", value=f"`{ctx.prefix}config bot`")
            embed.add_field(name="Moderation Roles ❌", value=f"`{ctx.prefix}config modroles`")
            embed.add_field(name="Music DJ ❌", value=f"`{ctx.prefix}config dj`")
            embed.add_field(name="Leveling Settings ❌", value=f"`{ctx.prefix}config levels`")
            embed.add_field(name="Economy Settings ❌", value=f"`{ctx.prefix}config eco`")
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command()
    @commands.has_permissions(manage_guild=True)
    async def bot(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Bot", colour=self.bot.red)
            embed.add_field(name="Change Prefix ✅", value=f"`{ctx.prefix}prefix <new_prefix>`")
            embed.add_field(name="Change Bot Nickname ✅", value=f"`{ctx.prefix}botnick <new_nick>`")
            embed.add_field(name="Edit Bot Responses ❌", value=f"`{ctx.prefix}config responses`")
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(aliases=['modrole'])
    @commands.has_permissions(manage_guild=True)
    async def modroles(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Moderation Roles", description="**NOTE:** Moderation Roles provide full access to **ALL** moderation commands as well as full **IMMUNITY** to them.", colour=self.bot.red)
            embed.add_field(name="Show Mod Roles ❌", value=f"`{ctx.prefix}modrole list`")
            embed.add_field(name="Add Mod Role ❌", value=f"`{ctx.prefix}modrole add <role>`")
            embed.add_field(name="Remove Mod Role ❌", value=f"`{ctx.prefix}modrole remove <role>`")
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(aliases=['music'])
    @commands.has_permissions(manage_guild=True)
    async def dj(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Music DJ", colour=self.bot.red)
            embed.add_field(name="Show DJ Roles ❌", value=f"`{ctx.prefix}dj list`")
            embed.add_field(name="Add DJ Role ❌", value=f"`{ctx.prefix}dj add <role>`")
            embed.add_field(name="Remove DJ Role ❌", value=f"`{ctx.prefix}dj remove <role>`", inline=False)
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(aliases=['levelling', 'level'])
    @commands.has_permissions(manage_guild=True)
    async def levels(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Levelling", colour=self.bot.red)
            embed.add_field(name="Blacklist role/member ❌", value=f"`{ctx.prefix}xp blacklist <role/member>`")
            embed.add_field(name="Add DJ Role/Member ❌", value=f"`{ctx.prefix}dj add <role/member>`")
            embed.add_field(name="Remove DJ Role/Member ❌", value=f"`{ctx.prefix}dj remove <role/member>`", inline=False)
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(aliases=['currency', 'eco'])
    @commands.has_permissions(manage_guild=True)
    async def economy(self, ctx):
        if ctx.guild.id == 912148314223415316:
            embed = discord.Embed(title="Config Panel: Economy", colour=self.bot.red)
            embed.add_field(name="Blacklist role/member ❌", value=f"`{ctx.prefix}xp blacklist <role/member>`")
            embed.add_field(name="Add DJ Role/Member ❌", value=f"`{ctx.prefix}dj add <role/member>`")
            embed.add_field(name="Remove DJ Role/Member ❌", value=f"`{ctx.prefix}dj remove <role/member>`", inline=False)
            embed.set_footer(text=f"Having trouble? Join the support server using {ctx.prefix}support!")
            await ctx.send(embed=embed)

    @config.command(slash_command=True, description="change the bot's prefix", aliases=["config prefix"])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix=None):
        """Change the bot's prefix"""
        if new_prefix is None:
            embed = Embed(
                title=f"The prefix for `{ctx.guild.name}` is `{ctx.prefix}`", 
                timestamp=True
            )
            return await ctx.message.reply(embed=embed)
        
        con = PrefixDB(self.bot.db)
        await con.update(ctx.guild.id, new_prefix)
        
        embed = Embed(
            title=f"Prefix for `{ctx.guild.name}` set to `{new_prefix}`",
            timestamp=True
        )
        
        return await ctx.message.reply(embed=embed)

    @config.command(slash_command=True, aliases=['suggest', 'suggestion'])
    @commands.has_permissions(manage_guild=True)
    async def suggestions(self, ctx):
        if ctx.guild.id != 912148314223415316:
            return
        guildconf = await SuggestDB(self.bot.db).getconf(ctx.guild.id)
        if guildconf is None:
            """   SELECT CATEGORY OF THE SUGGESTIONS CHANNEL   """
            view = SuggestConfCatView(ctx)
            embed = discord.Embed(description="Please select the category in which your desired suggestions channel is in below.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon, name="Suggestions Setup")
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            cat_id = view.values[0]
            embed.description += f"\n\n**[EXPIRED] - Category Chosen:** `{ctx.guild.get_channel(int(cat_id)).name}`"
            await msg.edit(embed=embed, view=None)

            """   SELECT CHANNEL WITHIN CHOSEN CATEGORY   """
            view = SuggestConfChanView(ctx.guild.get_channel(int(cat_id)))
            embed = discord.Embed(description="Please select the channel that you would like suggestions to be sent to below.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup")
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            channel_id = view.values[0]
            embed.description += f"\n\n**[EXPIRED] - Channel Chosen:** {ctx.guild.get_channel(int(channel_id)).mention}"
            await msg.edit(embed=embed, view=None)

            """   SAFEMODE ENABLE/DISABLE   """
            view = SuggestConfSafemode()
            embed = discord.Embed(description="**Would you like to enable safemode?**\n\n> Safemode means that a suggestion will have to be allowed by a higher-up before being sent into your suggestions channel. Please select a button below to either enable/disable safemode.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup")
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()
            safemodebool = view.value
            embed.description += f"\n\n**[EXPIRED] - Safemode is:** `{'Enabled' if safemodebool is True else 'Disabled'}`"
            await msg.edit(embed=embed, view=None)

            """   ADD CONFIG TO DATABASE IF NOT SAFEMODE   """
            if not safemodebool:
                await SuggestDB(self.bot.db).setupnon(ctx.guild.id, int(channel_id))

            """   GET SAFEMODE CAT IF ENABLED """
            if safemodebool:
                view = SuggestConfCatSafeView(ctx)
                embed = discord.Embed(description="Please select the Category for the channel that you want suggestions to await acceptance in.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup")
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                safemodecat = view.values[0]
                embed.description += f"\n\n**[EXPIRED] - Category Chosen:** `{ctx.guild.get_channel(int(safemodecat)).name}`"
                await msg.edit(embed=embed, view=None)

                """GET SAFEMODE CHANNEL IF ENABLED"""
                view = SuggestConfChanSafeView(ctx.guild.get_channel(int(safemodecat)))
                embed = discord.Embed(description="Select the channel that you want suggestions to await acceptance in.", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup")
                msg = await ctx.send(embed=embed, view=view)
                await view.wait()
                safemodechannel = view.values[0]
                embed.description += f"\n\n**[EXPIRED] - Channel Chosen:** {ctx.guild.get_channel(int(safemodechannel)).mention}"

                """   ADD CONFIG TO DATABASE   """
                await SuggestDB(self.bot.db).setup(ctx.guild.id, int(channel_id), int(safemodechannel))
            
            """   CONFIRMATION MESSAGE   """
            await ctx.message.reply(embed=discord.Embed(description=f"Suggestions has been successfully setup for `{ctx.guild.name}`!\n\nIf you made a mistake or would like to make edits in future, simply run `{ctx.prefix}config suggestions` again!\n\n**NEW CONFIGURATION:**\nChannel: {ctx.guild.get_channel(int(channel_id)).mention}\nSafemode: {f'Enabled in {ctx.guild.get_channel(int(safemodechannel)).mention}' if safemodebool else 'Disabled'}", colour=self.bot.red).set_author(icon_url=ctx.guild.icon.url, name="Suggestions Setup Complete"))


def setup(bot):
    bot.add_cog(ConfigCMD(bot))