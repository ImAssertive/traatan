import discord, asyncio, sys, traceback, checks, useful
import sqlite3 as lite
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot

    #@commands.command()
    #@checks.has_roleedit_permission()

    @commands.command()
    @checks.justme()
    async def botban(self, ctx, memberid):
        self.bot.cur.execute("UPDATE Users SET banned=1 WHERE userID =?", memberid,)
        self.bot.con.commit()

    @commands.command()
    @checks.justme()
    async def botunban(self, ctx, memberid):
        self.bot.cur.execute("UPDATE Users SET banned=0 WHERE userID =?", memberid,)
        self.bot.con.commit()

    async def on_guild_join(self, ctx):
        self.bot.cur.execute("SELECT * FROM Guilds WHERE guildID = ?", (ctx.id,))
        result = self.bot.cur.fetchone()
        if not result:
            self.bot.cur.execute('''INSERT INTO Guilds (guildID) VALUES(?)''',(ctx.id,))
            self.bot.con.commit()

    async def on_member_join(self, ctx):
        self.bot.cur.execute("SELECT * FROM Users WHERE userID = ?", (ctx.id,))
        if not self.bot.cur.fetchone():
            self.bot.cur.execute('''INSERT INTO Users (userID) VALUES(?)''',(ctx.id,))
            self.bot.con.commit()
        IDs=[(ctx.guild.id),(ctx.id)]
        self.bot.cur.execute("SELECT * FROM GuildUsers WHERE guildID = ? AND userID = ?", IDs)
        print(self.bot.cur.fetchone())
        if not self.bot.cur.fetchone():
            self.bot.cur.execute('''INSERT INTO GuildUsers (guildID, userID) VALUES(?,?)''', IDs)
            self.bot.con.commit()





def setup(bot):
    bot.add_cog(adminCog(bot))