import discord, asyncio, sys, traceback, checks, useful
import sqlite3 as lite
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot
        self.con = lite.connect('tt.db')
        self.cur = self.con.cursor()

    async def on_guild_join(self, ctx):
        print(ctx.id)
        self.cur.execute("SELECT * FROM Guilds WHERE guildID = ?", (ctx.id,))
        if not self.cur.fetchone():
            print("mew")
            #self.cur.execute('''SET IDENTITY_INSERT Guilds ON''')
            self.cur.execute('''INSERT INTO Guilds (guildID) VALUES(?)''',(ctx.id,))
           # self.cur.execute('''SET IDENTITY_INSERT Guilds OFF''')
            self.con.commit()
        print("wew")



def setup(bot):
    bot.add_cog(adminCog(bot))