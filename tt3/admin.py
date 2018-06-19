import discord, asyncio, sys, traceback, checks, useful
import sqlite3 as lite
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot



    # @commands.command()
    # @checks.is_not_banned()
    # #@checks.has_roleedit_permission()
    # async def addrole(self, ctx, *, roleName):
    #     role = discord.utils.get(ctx.guild.roles, name= roleName)



    # @commands.command()
    # @checks.justme()
    # async def botban(self, ctx, member):
    #     memberid = int(useful.getid(member))
    #     print(memberid)
    #     self.bot.cur.execute("UPDATE Users SET banned=1 WHERE userID =?", (memberid,))
    #     self.bot.con.commit()
    #
    # @commands.command()
    # @checks.justme()
    # async def botunban(self, ctx, member):
    #     memberid = int(useful.getid(member))
    #     print(memberid)
    #     self.bot.cur.execute("UPDATE Users SET banned=0 WHERE userID =?", (memberid,))
    #     self.bot.con.commit()
    #
    # async def on_guild_join(self, ctx):
    #     self.bot.cur.execute('''INSERT OR IGNORE INTO Guilds (guildID) VALUES(?)''',(ctx.id,))
    #     self.bot.con.commit()
    #
    # async def on_member_join(self, ctx):
    #     self.bot.cur.execute('''INSERT OR IGNORE INTO Users (userID) VALUES(?)''',(ctx.id,))
    #     self.bot.con.commit()
    #     IDs=[(ctx.guild.id),(ctx.id)]
    #     self.bot.cur.execute('''INSERT OR IGNORE INTO GuildUsers (guildID, userID) VALUES(?,?)''', IDs)
    #     self.bot.con.commit()

    async def on_ready():
        print('------')
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')



def setup(bot):
    bot.add_cog(adminCog(bot))