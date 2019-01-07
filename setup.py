import discord, asyncio, sys, traceback, checks, useful, asyncpg, random
from discord.ext import commands


class setupCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "exit", aliases =['quit'], hidden = True)
    @checks.justme()
    async def exit(self, ctx):
        thanos = random.randint(1,5)
        if thanos == 1:
            await ctx.channel.send("Mrs Assertive I dont feel so good...")
        if thanos == 2:
            await ctx.channel.send("Why...")
        if thanos == 3:
            await ctx.channel.send(":wave: Goodbye.")
        if thanos == 4:
            await ctx.channel.send("Faster, Bambi! Don't look back! Keep running! Keep running!")
        if thanos == 5:
            await ctx.channel.send("The horror. The horror.")
        await self.bot.db.close()
        await self.bot.logout()
        sys.exit()
        quit()


    @commands.command(hidden = True)
    @checks.justme()
    async def addmembers(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            for member in ctx.guild.members:
                query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, member.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.command(hidden= True)
    @checks.justme()
    async def addroles(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            for role in ctx.guild.roles:
                query = "INSERT INTO Roles (roleID) VALUES($1) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, role.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")


    @commands.command(hidden = True)
    @checks.justme()
    async def addguild(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Guilds (guildID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.command(hidden = True)
    @checks.justme()
    async def deletemember(self, ctx, member):
        memberid = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM Users WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    async def on_guild_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Guilds (guildID) VALUES($1) ON CONFLICT DO NOTHING" ##Adds guild to database
            await self.bot.db.execute(query, ctx.id)
            query = "INSERT INTO Roles (roleID) VALUES($1) ON CONFLICT DO NOTHING" ##Adds the @everyone role to database
            await self.bot.db.execute(query, ctx.id)
            for role in ctx.roles:
                query = "INSERT INTO Roles (roleID) VALUES($1) ON CONFLICT DO NOTHING" ##Adds all other roles to database
                await self.bot.db.execute(query, role.id)
            for member in ctx.members:
                query = "INSERT INTO Users (userID) VALUES($1) ON CONFLICT DO NOTHING" ## Adds users to database
                await self.bot.db.execute(query)
        await self.bot.db.release(connection)

    async def on_guild_role_create(self, ctx): ##On the creation of a new role adds it to database
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Roles (roleID, guildID) VALUES($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id, ctx.guild.id)
        await self.bot.db.release(connection)

    async def on_guild_role_delete(self, ctx): ##On deletion of a role remove it from database
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM Roles WHERE roleID = $1"
            await self.bot.db.execute(query, ctx.id)
        await self.bot.db.release(connection)

    async def on_member_remove(self, ctx):
        # connection = await self.bot.db.acquire()
        # async with connection.transaction():
        #     query = "DELETE FROM Users WHERE userID = $1"
        #     await self.bot.db.execute(query, ctx.id, ctx.guild.id)
        # await self.bot.db.release(connection)

        query = "SELECT * FROM Guilds WHERE guildID = $1 AND leave = true"
        result = await self.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            channelID = ("{}".format(result["leavechannel"]))
            leavetext = useful.formatTextLeave(ctx, ("{}".format(result["leavetext"])))
            await ctx.guild.get_channel(int(channelID)).send(leavetext)

    async def on_member_join(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "INSERT INTO Users (userID) VALUES ($1) ON CONFLICT DO NOTHING"
            await self.bot.db.execute(query, ctx.id)
        await self.bot.db.release(connection)
        query = "SELECT * FROM Guilds WHERE guildID = $1 AND welcome = true"
        result = await self.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            channelID = ("{}".format(result["welcomechannel"]))
            welcometext = useful.formatText(ctx, ("{}".format(result["welcometext"])))
            await ctx.guild.get_channel(int(channelID)).send(welcometext)


    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandNotFound):
    #         return
    #     elif isinstance(error, commands.CheckFailure):
    #         try:
    #             await ctx.channel.send(":no_entry: | {} caused an error! This is most likely a permission error but due to how bad Assertive is at coding this could be anything.".format(ctx.command))
    #         except:
    #             pass




def setup(bot):
    bot.add_cog(setupCog(bot))