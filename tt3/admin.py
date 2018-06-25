import discord, asyncio, sys, traceback, checks, useful, asyncpg
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup', aliases=['botsetup', 'su'])
    @checks.justme() # change
    async def setup(self, ctx):
        if not ctx.guild:
            await ctx.author.send(":no_good: | This command can not be used in DM!")
        else:
            timeout = False
            choice = "choice"
            options = ["info", "yes", "no", "skip"]
            embed = discord.Embed(title="Welcome to the TraaTan setup menu!", description="This menu allows you to decide which commands will work on this server. If you would like to grant or remove permissions from a specific role please use the UNDEFINED command!", colour=self.bot.getcolour())
            await ctx.channel.send(embed=embed)
            while choice.lower() not in options and timeout == False:
                embed = discord.Embed(title="Firstly - would you like to have pubquiz commands enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`",colour=self.bot.getcolour())
                await ctx.channel.send(embed = embed)
                try:
                    msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout = 60.0)
                except asyncio.TimeoutError:
                    try:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                    except TypeError:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                    timeout = True
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
                    elif choice.lower() == "info":
                        await ctx.channel.send("Info coming soon.")
                        choice = "choice"
                    elif choice.lower() == "skip":
                        await ctx.channel.send("Got it! I've left your pubquiz settings as is!")
            choice = "choice"
            while choice.lower() not in options and timeout == False:
                embed = discord.Embed(title="Next - would you like to have video game commands enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`",colour=self.bot.getcolour())
                await ctx.channel.send(embed = embed)
                try:
                    msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout = 60.0)
                except asyncio.TimeoutError:
                    try:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                    except TypeError:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                    timeout = True
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
                    elif choice.lower() == "info":
                        await ctx.channel.send("Info coming soon.")
                        choice = "choice"
                    elif choice.lower() == "skip":
                        await ctx.channel.send("Got it! I've left your games settings as is!")
            choice = "choice"
            while choice.lower() not in options and timeout == False:
                embed = discord.Embed(title="Next - would you like to have bluetext commands enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`",colour=self.bot.getcolour())
                await ctx.channel.send(embed = embed)
                try:
                    msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout = 60.0)
                except asyncio.TimeoutError:
                    try:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                    except TypeError:
                        await ctx.channel.send(":no_entry: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                    timeout = True
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
                    elif choice.lower() == "info":
                        await ctx.channel.send("Info coming soon.")
                        choice = "choice"
                    elif choice.lower() == "skip":
                        await ctx.channel.send("Got it! I've left your bluetext settings as is!")
                choice = "choice"
                while choice.lower() not in options and timeout == False:
                    embed = discord.Embed(title="Next - would you like to have welcome messages enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`", colour=self.bot.getcolour())
                    await ctx.channel.send(embed=embed)
                    try:
                        msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout=60.0)
                    except asyncio.TimeoutError:
                        try:
                            await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        except TypeError:
                            await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        timeout = True
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
                        elif choice.lower() == "info":
                            await ctx.channel.send("Info coming soon.")
                            choice = "choice"
                        elif choice.lower() == "skip":
                            await ctx.channel.send("Got it! I've left your welcome message settings as is!")

                choice = "choice"
                while choice.lower() not in options and timeout == False:
                    embed = discord.Embed(title="Next - would you like to have farewell messages enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`", colour=self.bot.getcolour())
                    await ctx.channel.send(embed=embed)
                    try:
                        msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout=60.0)
                    except asyncio.TimeoutError:
                        try:
                            await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        except TypeError:
                            await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        timeout = True
                    else:
                        choice = msg.content
                        if choice.lower() == "yes":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET leaveEnabled = true WHERE guildID = $1"
                                await self.bot.db.execute(query, ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! Farewell messages have been enabled. Please use tt!setfarewell to chose the channel to welcome new users!")
                        elif choice.lower() == "no":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET leaveEnabled = false WHERE guildID = $1"
                                await self.bot.db.execute(query, ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! Welcome messages have been disabled.")
                        elif choice.lower() == "info":
                            await ctx.channel.send("Info coming soon.")
                            choice = "choice"
                        elif choice.lower() == "skip":
                            await ctx.channel.send("Got it! I've left your farewell message settings as is!")

                choice = "choice"
                while choice.lower() not in options and timeout == False:
                    embed = discord.Embed(title="Next - would you like to have admin commands enabled?", description="Options: `Yes`, `No`, `Info`, `Skip`", colour=self.bot.getcolour())
                    await ctx.channel.send(embed=embed)
                    try:
                        msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout=60.0)
                    except asyncio.TimeoutError:
                        try:
                            await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        except TypeError:
                            await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        timeout = True
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
                        elif choice.lower() == "info":
                            await ctx.channel.send("Info coming soon.")
                            choice = "choice"
                        elif choice.lower() == "skip":
                            await ctx.channel.send("Got it! I've left your admin command settings as is!")

                await ctx.channel.send("Thanks! You are all set up.")



    @commands.command(name='botglobalban', aliases=['bgb', 'fuckoff'], hidden = True)
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
    async def setwelcometext(self, ctx, *, welcometext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET welcometext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, welcometext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Welcome text set to '" + welcometext + "'")

    @commands.command()
    @checks.leave_enabled()
    @checks.justme() #CHANGE
    async def setfarewelltext(self, ctx, *, leavetext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET leavetext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, leavetext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Welcome text set to: ```" + leavetext + "```")


    @commands.command()
    async def gdpr(self, ctx):
        embed = discord.Embed(title="Here is the data currently stored about you:", description="", colour=self.bot.getcolour())
        query = "SELECT * FROM Users WHERE userID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.author.id)
        if result:
            embed.add_field(name="Your user ID is: ", value=("{}".format(result["userid"])))
            embed.add_field(name="You are pubquizDM settings are currently:", value=("{}".format(result["pubquizdm"])))
            embed.add_field(name="Your global banned status is currently:", value=("{}".format(result["banned"])))
        query = "SELECT * FROM GuildUsers WHERE userID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.author.id)
        if result:
            embed.add_field(name="For some reason this only works for 1 guild", value="Im working on a fix! Contact @Zootopia#0001 for other guilds if needed.")
            embed.add_field(name="You are currently in guild ID:", value=("{}".format(result["guildid"])))
            embed.add_field(name="Your Total Pub Quiz Score is:", value=("{}".format(result["pubquizscoretotal"])))
            embed.add_field(name="Last Pub Quiz your score was:", value=("{}".format(result["pubquizscoreweekly"])))
            embed.add_field(name="Your banned status here is:", value=("{}".format(result["banned"])))
        query = "SELECT * FROM UserGameAccounts WHERE userID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.author.id)
        if result:
            embed.add_field(name="Im still working on this bit!", value="You should never see this! If you do, contact @Zootopia#0001 for this information.")
        try:
            await ctx.author.send(embed = embed)
        except:
            await ctx.channel.send("Please enable 'Allow direct messages from server members' under 'Privacy & Safety' in settings. For security reasons this information can not be posted publicly.")


    @commands.command(name='botglobalunban', aliases=['bgub', 'wback'], hidden = True)
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