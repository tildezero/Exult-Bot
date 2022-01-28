from discord.ext import commands

class BotAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(slash_command=True, description="shut down bot", hidden=True)
    @commands.is_owner()
    async def logout(self, ctx):
        """Logs out and shuts down the bot"""
        await self.bot.close_bot()
        
def setup(bot):
    bot.add_cog(BotAdmin(bot))