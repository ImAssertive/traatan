import discord, asyncio, sys, traceback, checks, useful
import sqlite3 as lite
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot
        bot.con = lite.connect('tt.db')
        bot.cur = bot.con.cursor()

    #@commands.command()
    #@checks.has_roleedit_permission()

    @commands.command()
    @checks.justme()
    async def botban(self, ctx, memberid):
        bot.cur.execute("UPDATE Users SET banned=1 WHERE userID =?", memberid,)
        bot.con.commit()

    @commands.command()
    @checks.justme()
    async def botunban(self, ctx, memberid):
        bot.cur.execute("UPDATE Users SET banned=0 WHERE userID =?", memberid,)
        bot.con.commit()

    async def on_guild_join(self, ctx):
        bot.cur.execute("SELECT * FROM Guilds WHERE guildID = ?", (ctx.id,))
        result = bot.cur.fetchone()
        if not result:
            bot.cur.execute('''INSERT INTO Guilds (guildID) VALUES(?)''',(ctx.id,))
            bot.con.commit()

    async def on_member_join(self, ctx):
        bot.cur.execute("SELECT * FROM Users WHERE userID = ?", (ctx.id,))
        if not bot.cur.fetchone():
            bot.cur.execute('''INSERT INTO Users (userID) VALUES(?)''',(ctx.id,))
            bot.con.commit()
        IDs=[(ctx.guild.id),(ctx.id)]
        bot.cur.execute("SELECT * FROM GuildUsers WHERE guildID = ? AND userID = ?", IDs)
        print(bot.cur.fetchone())
        if not bot.cur.fetchone():
            bot.cur.execute('''INSERT INTO GuildUsers (guildID, userID) VALUES(?,?)''', IDs)
            bot.con.commit()





def setup(bot):
    bot.add_cog(adminCog(bot))