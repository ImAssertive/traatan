import discord, asyncio, sys, traceback, checks, useful
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot
        self.con = lite.connect(db)
        self.cur = self.con.cursor()

    async def on_guild_join(self, ctx):
        self.cur.execute('''INSERT INTO Guilds (guildID) VALUES(?)''',ctx.id)
        self.con.commit()
        

def setup(bot):
    bot.add_cog(adminCog(bot))