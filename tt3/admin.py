import discord, asyncio, sys, traceback, checks, useful, asyncpg
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup', aliases=['botsetup', 'su'])
    @checks.is_not_banned()
    @checks.justme() # change
    async def setup(self, ctx):
        if not ctx.guild:
            await ctx.author.send(":no_good: | This command can not be used in DM!")
        else:
            timeout = False
            choice = "choice"
            settings = [["Firstly", "Pub Quiz", "pubquizEnabled", "Allows the guild to run a weekly pub quiz complete with custom scoring! For full rules visit NOT DONE YET"],
                        ["Secondly", "Video Game", "gamesEnabled", "Allows the guild to run a weekly pub quiz complete with custom scoring! For full rules visit NOT DONE YET"],
                        ["Next", "bluetext", "bluetextEnabled", "Enables a series of commands allowing members to use blue text emotes to construct sentences."],
                        ["Next", "welcome messages", "welcomeEnabled", "Enables a welcome message when users join the server. This can be set with tt!setwelcome and tt!setwelcometext commands"],
                        ["Next", "farewell messages", "leaveEnabled", "Enables a farewell message when the user leaves the server. This can be set with tt!setleave and tt!setleavetext commands"],
                        ["Finally", "admin", "adminEnabled", "Enables the bots administrator commands. For a list of commands please use UNDEFINED"]]
            options = ["info", "yes", "no", "skip"]
            embed = discord.Embed(title="Welcome to the TraaTan setup menu!", description="This menu allows you to decide which commands will work on this server. If you would like to grant or remove permissions from a specific role please use the UNDEFINED command!", colour=self.bot.getcolour())
            await ctx.channel.send(embed=embed)
            for setting in settings:
                print(setting)
                choice = "choice"
                while choice.lower() not in options and timeout == False:
                    embed = discord.Embed(title=(setting[0] + " - would you like to have " + setting[1] + " commands enabled?"), description="Options: `Yes`, `No`, `Info`, `Skip`",colour=self.bot.getcolour())
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
                                query = "UPDATE Guilds SET $1 = true WHERE guildID = $2"
                                await self.bot.db.execute(query, setting[2], ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! "+ setting[1] +" commands have been enabled.")
                        elif choice.lower() == "no":
                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                query = "UPDATE Guilds SET $1 = false WHERE guildID = $2"
                                await self.bot.db.execute(query, setting[2], ctx.guild.id)
                            await self.bot.db.release(connection)
                            await ctx.channel.send("Got it! "+ setting[1]+" commands have been disabled.")
                        elif choice.lower() == "info":
                            await ctx.channel.send(setting[3])
                            choice = "choice"
                        elif choice.lower() == "skip":
                            await ctx.channel.send("Got it! I've left your " + setting[1] + " settings as is!")
            await ctx.channel.send("Thanks! You are all set up.")

    @commands.command(name = "exit", aliases =['quit'], hidden = True)
    @checks.justme()
    async def exit(self, ctx):
        await ctx.channel.send(":wave: Goodbye.")
        sys.exit()

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

    @commands.command(name="setfarewell", aliases=['setleave'])
    @checks.leave_enabled()
    @checks.is_not_banned()
    @checks.justme() #CHANGE
    async def setfarewell(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET leavechannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Farewell channel set here.")

    @commands.command()
    @checks.is_not_banned()
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
    @checks.is_not_banned()
    @checks.justme() #CHANGE
    async def setwelcometext(self, ctx, *, welcometext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET welcometext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, welcometext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Welcome text set to ```" + welcometext + "```")

    @commands.command(name="setfarewelltext", aliases =['setleavetext'])
    @checks.leave_enabled()
    @checks.is_not_banned()
    @checks.justme() #CHANGE
    async def setfarewelltext(self, ctx, *, leavetext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET leavetext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, leavetext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Farewell text set to: ```" + leavetext + "```")


    @commands.command()
    async def gdpr(self, ctx):
        finished = 0
        while finished == 0:
            try:
                await ctx.author.send("Here is the data currently stored about you:")
            except:
                await ctx.channel.send("Please enable 'Allow direct messages from server members' under 'Privacy & Safety' in settings. For security reasons this information can not be posted publicly.")
                break
            embed = discord.Embed(title="Global Data:", description="", colour=self.bot.getcolour())
            query = "SELECT * FROM Users WHERE userID = $1"
            results = await ctx.bot.db.fetchrow(query, ctx.author.id)
            if results:
                embed.add_field(name="Your user ID is: ", value=("{}".format(results["userid"])))
                embed.add_field(name="You are pubquizDM settings are currently:", value=("{}".format(results["pubquizdm"])))
                embed.add_field(name="Your global banned status is currently:", value=("{}".format(results["banned"])))
            else:
                embed = discord.Embed(title="Global Data:", description="No data found!", colour=self.bot.getcolour())
            await ctx.author.send(embed=embed)
            query = "SELECT * FROM GuildUsers WHERE userID = $1"
            results = await ctx.bot.db.fetch(query, ctx.author.id)
            if results:
                embed = discord.Embed(title="Server Data:", description="", colour=self.bot.getcolour())
                for row in results:
                    currentRow = row
                    embed.add_field(name="The following information is for guild ID:", value=("{}".format(currentRow["guildid"])), inline=False)
                    embed.add_field(name="Your Total Pub Quiz Score is:", value=("{}".format(currentRow["pubquizscoretotal"])), inline=False)
                    embed.add_field(name="Last Pub Quiz your score was:", value=("{}".format(currentRow["pubquizscoreweekly"])), inline=False)
                    embed.add_field(name="Your banned status here is:", value=("{}".format(currentRow["banned"])), inline=False)
            else:
                embed = discord.Embed(title="Server Data:", description="No data found!", colour=self.bot.getcolour())
            await ctx.author.send(embed=embed)
            query = "SELECT * FROM UserGameAccounts WHERE userID = $1"
            results = await ctx.bot.db.fetch(query, ctx.author.id)
            if results:
                for row in results:
                    currentRow = row
                embed = discord.Embed(title="Im still working on this bit!", description="You should never see this! If you do, contact @Zootopia#0001 for this information.")
            else:
                embed = discord.Embed(title="Game account data:", description="No data found!")
            await ctx.author.send(embed = embed)
            finished = 1

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