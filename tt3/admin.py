import discord, asyncio, sys, traceback, checks, useful, asyncpg
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot


    # @commands.command()
    # @checks.is_not_banned()
    # #@checks.has_roleedit_permission()
    # async def addrole(self, ctx, *, roleName):
    #     role = discord.utils.get(ctx.guild.roles, name= roleName)


    @commands.command()
    @checks.justme()
    async def botban(self, ctx, member):
        memberid = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Users SET banned = true WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")


    @commands.command()
    @checks.justme()
    async def botunban(self, ctx, member):
        memberid = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Users SET banned = false WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

def setup(bot):
    bot.add_cog(adminCog(bot))