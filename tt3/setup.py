import discord, asyncio, sys, traceback, checks, useful, asyncpg
from discord.ext import commands


class setupCog:
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    @checks.justme()
    async def addmembers(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            for member in ctx.guild.members:
                query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, member.id)
                query = "INSERT INTO GuildUsers (guildID, userID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, ctx.guild.id, member.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")



    @commands.command()
    @checks.justme()
    async def addguild(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Guilds (guildID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.command()
    @checks.justme()
    async def deletemember(self, member):
        memberid = useful.getid(member)
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM Users WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")


    async def on_guild_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Guilds (guildID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id)
            for member in ctx.members:
                query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, member.id)
                query = "INSERT INTO GuildUsers (guildID, userID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, ctx.id, member.id)
        await self.bot.db.release(connection)

    async def on_guild_remove(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM GuildUsers WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.id)
            query = "DELETE FROM Guilds WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.id)
        await self.bot.db.release(connection)

    async def on_member_remove(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM GuildUsers WHERE userID = $1 AND guildID = $2"
            await self.bot.db.execute(query, ctx.id, ctx.guild.id)
        await self.bot.db.release(connection)

        query = "SELECT * FROM Guilds WHERE guildID = $1 AND banned = false AND leaveEnabled = true"
        result = await self.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            channelID = ("{}".format(result["leavechannel"]))
            leavetext = useful.formatText(ctx, ("{}".format(result["leavetext"])))
            await ctx.guild.get_channel(int(channelID)).send(leavetext)

    async def on_member_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id)
            query = "INSERT INTO GuildUsers (guildID, userID) VALUES($1, $2) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.guild.id, ctx.id)
        await self.bot.db.release(connection)
        query = "SELECT * FROM Guilds WHERE guildID = $1 AND banned = false AND welcomeEnabled = true"
        result = await self.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            channelID = ("{}".format(result["welcomechannel"]))
            welcometext = useful.formatText(ctx, ("{}".format(result["welcometext"])))
            await ctx.guild.get_channel(int(channelID)).send(welcometext)









def setup(bot):
    bot.add_cog(setupCog(bot))