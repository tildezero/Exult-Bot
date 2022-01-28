import discord
from discord.ext import commands
from datetime import datetime
import asyncio

from database import cases
from kimetsu import embed

Embed = embed.Embed.embed

class LoopControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = True
        
    async def loop_control(self):
        asyncio.create_task(LoopControl(self.bot).loop_punish_check())
        print("[LOOP CONTROLLER] Loop Activated")
    
    async def punish_check(self):
        outdated = await cases.CasesDB(self.bot.db).get_outdated()
        try:
            guild = self.bot.get_guild(outdated[0]["guild_id"])
        except IndexError:
            return
        member = guild.get_member(outdated[0]["user_id"])
        reason = outdated[0]["reason"]
        case_type = outdated[0]["case_type"]
        if case_type == "Ban":
            await guild.unban(discord.Object(id=int(member.id)), reason="Time Served")
            await cases.CasesDB(self.bot.db).case_remove(case_type, guild.id, member.id, reason, outdated[0]["expiration_date"])
            embed = Embed(
                title="You have been unbanned",
                description=f"**Guild:** {guild.name}\n**Reason for ban:** {reason}")
            try:
                await member.send(embed=embed)
            except:
                return
        
    async def loop_punish_check(self):
        while self.loop:
            await LoopControl(self.bot).punish_check()
            await asyncio.sleep(5)

def setup(bot):
    bot.add_cog(LoopControl(bot))