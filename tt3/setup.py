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



    async def on_guild_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Guilds (guildID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id)
            for member in ctx.guild.members:
                query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, member.id)
                query = "INSERT INTO GuildUsers (guildID, userID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, ctx.guild.id, member.id)
        await self.bot.db.release(connection)

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