import discord, asyncio, sys, traceback, checks, useful
import sqlite3 as lite
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot
        self.con = lite.connect('tt.db')
        self.cur = self.con.cursor()

    @commands.command()
    @checks.justme()
    async def botban(self, ctx, member):
        memberid = useful.getid(member)
        self.cur.execute("UPDATE Users SET banned=1 WHERE userID =?", memberid,)
        self.con.commit()

    @commands.command()
    @checks.justme()
    async def botunban(self, ctx, member):
        memberid = useful.getid(member)
        self.cur.execute("UPDATE Users SET banned=0 WHERE userID =?", memberid,)
        self.con.commit()

    async def on_guild_join(self, ctx):
        self.cur.execute("SELECT * FROM Guilds WHERE guildID = ?", (ctx.id,))
        result = self.cur.fetchone()
        if not result:
            #self.cur.execute('''SET IDENTITY_INSERT Guilds ON''')
            self.cur.execute('''INSERT INTO Guilds (guildID) VALUES(?)''',(ctx.id,))
           # self.cur.execute('''SET IDENTITY_INSERT Guilds OFF''')
            self.con.commit()

    async def on_member_join(self, ctx):
        print(ctx.id)
        self.cur.execute("SELECT * FROM Users WHERE userID = ?", (ctx.id,))
        if not self.cur.fetchone():
            self.cur.execute('''INSERT INTO Users (userID) VALUES(?)''',(ctx.id,))
            self.con.commit()

        self.cur.execute("SELECT * FROM GuildUsers WHERE guildID = ? AND userID = ?", [(ctx.guild.id,),(ctx.id,)])
        print(self.cur.fetchone())
        if not self.cur.fetchone():
            self.cur.execute('''INSERT INTO GuildUsers (guildID, userID) VALUES(?,?)''',[(ctx.guild.id,),(ctx.id,)])
            self.con.commit()
            print("mew")





def setup(bot):
    bot.add_cog(adminCog(bot))