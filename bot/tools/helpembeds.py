from typing import Text
import discord

arrow = "<a:arrow:882812954314154045>"

class HelpEmbeds:
    def __init__(self, ctx, bot):
        self.ctx = ctx
        self.bot = bot
    
    def mainmenu(self):
        ilink = "https://discord.com/api/oauth2/authorize?client_id=889185777555210281&permissions=8&scope=bot%20applications.commands"
        embed = discord.Embed(title="Help Menu",
                             description=f"Invite the bot to your server [here]({ilink})\n"
                                         f"Join the support server [here](https://discord.gg/NAFTAtAz5d)\n\n"
                                         "**Categories:**\n"
                                         f"{arrow} To view all command categories, click on the **dropdown menu below**!\n\n"
                                         "**Guide:**\n"
                                         f"{arrow} For command categories: Select a category below or do `{self.ctx.prefix}help <category>`\n"
                                         f"{arrow} For help with specific commands: do `{self.ctx.prefix}help <command>`\n\n"
                                         f"{arrow} If you run into any issues with any commands, feel free to join [the support server](https://discord.gg/NAFTAtAz5d) for further assistance!",
                            colour=self.bot.red)
        embed.set_footer(text="If the select menu disappears, it simply means the command has timed out. Run the command again to re-use the menu!")
        return embed
    
    def moderation(self):
        mod_commands = [["Ban", f"Bans a member.\n`{self.ctx.prefix}ban`"], 
                        ["Kick", f"Kicks a member.\n`{self.ctx.prefix}kick`"], 
                        ["Purge", f"Purges a channel.\n`{self.ctx.prefix}purge`"], 
                        ["Slowmode", f"Puts a channel in slowmode.\n`{self.ctx.prefix}slowmode`"], 
                        ["Timeout", f"Puts a member in time out.\n`{self.ctx.prefix}timeout`"], 
                        ["Untimeout", f"Removes a member's timeout\n`{self.ctx.prefix}untimeout`"], 
                        ["Unban", f"Unbans a member.\n`{self.ctx.prefix}unban`"]]
        embed = discord.Embed(title="Help Menu: Moderation", colour=self.bot.red)
        for cmd in mod_commands:
            embed.add_field(name=cmd[0], value=cmd[1], inline=True)
        return embed
    
    def news(self):
        def import_news():
            with open ("./info/news.txt", "r") as f:
                text = f.read()
                return text
        embed = discord.Embed(title="Help Menu: News", description=import_news(), colour=self.bot.red)
        exult = self.ctx.bot.get_guild(912148314223415316)
        embed.set_thumbnail(url=exult.icon.url)
        return embed
        
    def miscellaneous(self):
        misc_commands = [["Avatar", f"Display someones avatar and banner.\n`{self.ctx.prefix}avatar`"],
                         ["RoleInfo", f"Display information on a role.\n`{self.ctx.prefix}roleinfo`"],
                         ["ServerInfo", f"Display information on the current server.\n{self.ctx.prefix}serverinfo"],
                         ["UserInfo", f"Display information on a given member.\n{self.ctx.prefix}userinfo"],
                         ["Inrole", f"Displays everyone who has a given role.\n{self.ctx.prefix}inrole"],
                         ["RNG", f"Randomly generates a number between 1 and a number you provide.\n{self.ctx.prefix}rng"]]
        embed = discord.Embed(title="Help Menu: Miscellaneous", colour=self.bot.red)
        for cmd in misc_commands:
                embed.add_field(name=cmd[0], value=cmd[1], inline=True)
        return embed
    
    def utility(self):
        util_commands = [["Help", f"Displays this help menu.\n`{self.ctx.prefix}help`"], 
                         ["Invite", f"Invite me to your server.\n`{self.ctx.prefix}invite`"], 
                         ["Ping", f"Displays the bots latency.\n`{self.ctx.prefix}ping`"], 
                         ["Support", f"Join the support server.\n`{self.ctx.prefix}support`"], 
                         ["Feedback", f"Give feedback on the bot!\n`{self.ctx.prefix}feedback`"], 
                         ["Info", f"Displays key info about the bot.\n`{self.ctx.prefix}info`"]]
        embed = discord.Embed(title="Help Menu: Utility", colour=self.bot.red)
        for cmd in util_commands:
            embed.add_field(name=cmd[0], value=cmd[1], inline=True)
        return embed
    
    def music(self):
        music_commands = [["Disconnect", f"Disconnects the bot from the currently active vc.\n`{self.ctx.prefix}disconnect`"], 
                          ["Lyrics", f"Find lyrics for a song.\n`{self.ctx.prefix}lyrics`"], 
                          ["Now", f"Displays currently playing song.\n`{self.ctx.prefix}now`"],
                          ["Pause", f"Pause the currently playing song.\n`{self.ctx.prefix}pause`"], 
                          ["Play", f"Add a song to the queue.\n`{self.ctx.prefix}play`"], 
                          ["Playlist", f"Make your own playlist.\n`{self.ctx.prefix}playlist`"], 
                          ["Queue", f"Display the bot's song queue\n`{self.ctx.prefix}queue`"], 
                          ["Remove", f"Remove a song from the queue\n`{self.ctx.prefix}remove`"], 
                          ["Repeat", f"Repeat the currently playing song\n`{self.ctx.prefix}repeat`"], 
                          ["Seek", f"Seek through the currently playing song.\n`{self.ctx.prefix}seek`"], 
                          ["Shuffle", f"Shuffle the current queue.\n`{self.ctx.prefix}shuffle`"], 
                          ["Skip", f"Skip the currently playing song.\n`{self.ctx.prefix}skip`"], 
                          ["Stop", f"Stop the queue.\n`{self.ctx.prefix}queue`"], 
                          ["Volume", f"Adjust the volume for the currently playing song.\n`{self.ctx.prefix}volume`"]]
        embed = discord.Embed(title="Help Menu: Music", colour=self.bot.red)
        for cmd in music_commands:
            embed.add_field(name=cmd[0], value=cmd[1], inline=True)
        return embed
    
    def fun(self):
        fun_commands = [["Animal", f"Sends a random animal.\n`{self.ctx.prefix}animal`"], 
                        ["Fact", f"Sends a random fact.\n`{self.ctx.prefix}fact`"], 
                        ["Joke", f"Sends a random joke.\n`{self.ctx.prefix}joke`"],
                        ["Roast", f"Sends a random roast.\n`{self.ctx.prefix}roast`"], 
                        ["Weather", f"Find out the weather for a specfic location.\n`{self.ctx.prefix}weather`"],
                        ["WPM", f"Do a type speed test!\n`{self.ctx.prefix}wpm`"], 
                        ["WTP", f"Who's that pokemon?\n`{self.ctx.prefix}wtp`"]]
        embed = discord.Embed(title="Help Menu: Fun", colour=self.bot.red)
        for cmd in fun_commands:
            embed.add_field(name=cmd[0], value=cmd[1], inline=True)
        return embed
    
    def economy(self):
        eco_commands = [["Economy commands", "Coming soon!"]]
        embed = discord.Embed(title="Help Menu: Economy", colour=self.bot.red)
        for cmd in eco_commands:
            embed.add_field(name=cmd[0], value=cmd[1], inline=True)
        return embed
    
    def configuration(self):
        conf_commands = [["Prefix", f"Change the bots prefix.\n`{self.ctx.prefix}help prefix`"]]
        embed = discord.Embed(title="Help Menu: Configuration", colour=self.bot.red)
        for cmd in conf_commands:
            embed.add_field(name=cmd[0], value=cmd[1], inline=True)
        return embed