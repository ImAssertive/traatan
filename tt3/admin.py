import discord, asyncio, sys, traceback, checks, useful, asyncpg
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


    @commands.command()
    @checks.justme()
    async def botban(self, ctx, member):
        memberid = int(useful.getid(member))
        await ctx.channel.send(":green_tick: | Done!")
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Users SET banned = true WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)

    @commands.command()
    @checks.justme()
    async def botunban(self, ctx, member):
        memberid = int(useful.getid(member))
        await ctx.channel.send(":green_tick: | Done!")
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Users SET banned = false WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)

    async def on_guild_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Guilds (guildID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id)
        await self.bot.db.release(connection)

    async def on_member_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id)
            query = "INSERT INTO GuildUsers (guildID, userID) VALUES($1, $2) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.guild.id, ctx.id)
            print("nyoom desu poi")
        await self.bot.db.release(connection)




def setup(bot):
    bot.add_cog(adminCog(bot))