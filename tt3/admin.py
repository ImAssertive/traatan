import discord, asyncio, sys, traceback, checks, useful, asyncpg
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup', aliases=['botsetup', 'su'])
    async def setup(self, ctx):
        if not ctx.guild:
            await ctx.author.send(":no_good: | This command can not be used in DM!")
        else:
            choice = "choice"
            options = ["info", "yes", "no", "skip"]
            while choice.lower() not in options:
                embed = discord.Embed(title="Welcome to the TraaTan setup menu!", description="This menu allows you to decide which commands will work on this server. If you would like to grant or remove permissions from a specific role please use the UNDEFINED command!",colour=self.bot.getcolour())
                await ctx.channel.send(embed = embed)
                embed = discord.Embed(title="Firstly - would you like to have pubquiz commands enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`",colour=self.bot.getcolour())
                await ctx.channel.send(embed = embed)
                try:
                    msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout = 60.0)
                except asyncio.TimeoutError:
                    try:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        break
                    except TypeError:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        break
                else:
                    choice = msg.content
                    if choice.lower() == "yes":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "UPDATE Guilds SET pubquizEnabled = true WHERE guildID = $1"
                            await self.bot.db.execute(query, ctx.guild.id)
                        await self.bot.db.release(connection)
                        await ctx.channel.send("Got it! Pubquiz commands have been enabled.")
                    elif choice.lower() == "no":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "UPDATE Guilds SET pubquizEnabled = false WHERE guildID = $1"
                            await self.bot.db.execute(query, ctx.guild.id)
                        await self.bot.db.release(connection)
                        await ctx.channel.send("Got it! Pubquiz commands have been disabled.")
                    elif choice.lower == "info":
                        await ctx.channel.send("Info coming soon.")
                    elif choice.lower == "skip":
                        await ctx.channel.send("Got it! I've left your pubquiz settings as is!")
            choice = "choice"
            while choice.lower() not in options:
                embed = discord.Embed(title="Next - would you like to have video game commands enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`",colour=self.bot.getcolour())
                await ctx.channel.send(embed = embed)
                try:
                    msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout = 60.0)
                except asyncio.TimeoutError:
                    try:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        break
                    except TypeError:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        break
                else:
                    choice = msg.content
                    if choice.lower() == "yes":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "UPDATE Guilds SET gamesEnabled = true WHERE guildID = $1"
                            await self.bot.db.execute(query, ctx.guild.id)
                        await self.bot.db.release(connection)
                        await ctx.channel.send("Got it! Game commands have been enabled.")
                    elif choice.lower() == "no":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "UPDATE Guilds SET gamesEnabled = false WHERE guildID = $1"
                            await self.bot.db.execute(query, ctx.guild.id)
                        await self.bot.db.release(connection)
                        await ctx.channel.send("Got it! games commands have been disabled.")
                    elif choice.lower == "info":
                        await ctx.channel.send("Info coming soon.")
                    elif choice.lower == "skip":
                        await ctx.channel.send("Got it! I've left your games settings as is!")
            choice = "choice"
            while choice.lower() not in options:
                embed = discord.Embed(title="Next - would you like to have bluetext commands enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`",colour=self.bot.getcolour())
                await ctx.channel.send(embed = embed)
                try:
                    msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout = 60.0)
                except asyncio.TimeoutError:
                    try:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        break
                    except TypeError:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        break
                else:
                    choice = msg.content
                    if choice.lower() == "yes":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "UPDATE Guilds SET bluetextEnabled = true WHERE guildID = $1"
                            await self.bot.db.execute(query, ctx.guild.id)
                        await self.bot.db.release(connection)
                        await ctx.channel.send("Got it! Bluetext commands have been enabled.")
                    elif choice.lower() == "no":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "UPDATE Guilds SET bluetextEnabled = false WHERE guildID = $1"
                            await self.bot.db.execute(query, ctx.guild.id)
                        await self.bot.db.release(connection)
                        await ctx.channel.send("Got it! Bluetext commands have been disabled.")
                    elif choice.lower == "info":
                        await ctx.channel.send("Info coming soon.")
                    elif choice.lower == "skip":
                        await ctx.channel.send("Got it! I've left your bluetext settings as is!")

                choice = "choice"
                while choice.lower() not in options:
                    embed = discord.Embed(title="Next - would you like to have welcome messages enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`", colour=self.bot.getcolour())
                    await ctx.channel.send(embed=embed)
                    try:
                        msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout=60.0)
                    except asyncio.TimeoutError:
                        try:
                            await ctx.channel.send(
                                ":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                            break
                        except TypeError:
                            await ctx.channel.send(
                                ":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                            break
                    else:
                        choice = msg.content
                        if choice.lower() == "yes":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET welcomeEnabled = true WHERE guildID = $1"
                                await self.bot.db.execute(query, ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! Welcome messages have been enabled. Please use tt!setwelcome to chose the channel to welcome new users!")
                        elif choice.lower() == "no":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET adminEnabled = false WHERE guildID = $1"
                                await self.bot.db.execute(query, ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! Welcome messages have been disabled.")
                        elif choice.lower == "info":
                            await ctx.channel.send("Info coming soon.")
                        elif choice.lower == "skip":
                            await ctx.channel.send("Got it! I've left your welcome message settings as is!")

                choice = "choice"
                while choice.lower() not in options:
                    embed = discord.Embed(title="Next - would you like to have farewell messages enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`", colour=self.bot.getcolour())
                    await ctx.channel.send(embed=embed)
                    try:
                        msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout=60.0)
                    except asyncio.TimeoutError:
                        try:
                            await ctx.channel.send(
                                ":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                            break
                        except TypeError:
                            await ctx.channel.send(
                                ":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                            break
                    else:
                        choice = msg.content
                        if choice.lower() == "yes":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET leaveEnabled = true WHERE guildID = $1"
                                await self.bot.db.execute(query, ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send(
                                "Got it! Farewell messages have been enabled. Please use tt!setfarewell to chose the channel to welcome new users!")
                        elif choice.lower() == "no":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET leaveEnabled = false WHERE guildID = $1"
                                await self.bot.db.execute(query, ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! Welcome messages have been disabled.")
                        elif choice.lower == "info":
                            await ctx.channel.send("Info coming soon.")
                        elif choice.lower == "skip":
                            await ctx.channel.send("Got it! I've left your farewell message settings as is!")

                choice = "choice"
                while choice.lower() not in options:
                    embed = discord.Embed(title="Next - would you like to have admin commands enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`", colour=self.bot.getcolour())
                    await ctx.channel.send(embed=embed)
                    try:
                        msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout=60.0)
                    except asyncio.TimeoutError:
                        try:
                            await ctx.channel.send(
                                ":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                            break
                        except TypeError:
                            await ctx.channel.send(
                                ":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                            break
                    else:
                        choice = msg.content
                        if choice.lower() == "yes":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET adminEnabled = true WHERE guildID = $1"
                                await self.bot.db.execute(query, ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! Admin commands have been enabled.")
                        elif choice.lower() == "no":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET adminEnabled = false WHERE guildID = $1"
                                await self.bot.db.execute(query, ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! admin commands have been disabled.")
                        elif choice.lower == "info":
                            await ctx.channel.send("Info coming soon.")
                        elif choice.lower == "skip":
                            await ctx.channel.send("Got it! I've left your admin command settings as is!")

                await ctx.channel.send("Thanks! You are all set up.")



    @commands.command(name='botglobalban', aliases=['bgb', 'fuckoff'])
    @checks.justme()
    async def botglobalban(self, ctx, member):
        memberid = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Users SET banned = true WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.command()
    @checks.leave_enabled()
    @checks.justme() #CHANGE
    async def setfarewell(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET leavechannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Farewell channel set here.")

    @commands.command()
    @checks.welcome_enabled()
    @checks.justme() #CHANGE
    async def setwelcome(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET welcomechannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Welcome channel set here.")

    @commands.command()
    @checks.welcome_enabled()
    @checks.justme() #CHANGE
    async def setwelcometext(self, ctx, welcometext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET welcometext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, welcometext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Welcome text set to '" + welcometext + "'")

    @commands.command()
    @checks.leave_enabled()
    @checks.justme() #CHANGE
    async def setfarewelltext(self, ctx, leavetext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET leavetext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, leavetext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Welcome text set to '" + leavetext + "'")


    @commands.command(name='botglobalunban', aliases=['bgub', 'wback'])
    @checks.justme()
    async def botglobalunban(self, ctx, member):
        memberid = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Users SET banned = false WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

def setup(bot):
    bot.add_cog(adminCog(bot))