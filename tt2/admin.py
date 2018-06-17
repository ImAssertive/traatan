import discord, asyncio, sys, traceback, checks, useful
import sqlite3 as lite
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        global con, cur
        self.bot = bot


    # @commands.command()
    # @checks.has_roleedit_permission()

    @commands.command()
    @checks.justme()
    async def botban(self, ctx, memberid):
        cur.execute("UPDATE Users SET banned=1 WHERE userID =?", memberid,)
        con.commit()

    @commands.command()
    @checks.justme()
    async def botunban(self, ctx, memberid):
        cur.execute("UPDATE Users SET banned=0 WHERE userID =?", memberid,)
        con.commit()

    async def on_guild_join(self, ctx):
        cur.execute("SELECT * FROM Guilds WHERE guildID = ?", (ctx.id,))
        result = cur.fetchone()
        if not result:
            cur.execute('''INSERT INTO Guilds (guildID) VALUES(?)''',(ctx.id,))
            con.commit()

    async def on_member_join(self, ctx):
        cur.execute("SELECT * FROM Users WHERE userID = ?", (ctx.id,))
        if not cur.fetchone():
            cur.execute('''INSERT INTO Users (userID) VALUES(?)''',(ctx.id,))
            con.commit()
        IDs=[(ctx.guild.id),(ctx.id)]
        cur.execute("SELECT * FROM GuildUsers WHERE guildID = ? AND userID = ?", IDs)
        print(cur.fetchone())
        if not cur.fetchone():
            cur.execute('''INSERT INTO GuildUsers (guildID, userID) VALUES(?,?)''', IDs)
            con.commit()





def setup(bot):
    bot.add_cog(adminCog(bot))