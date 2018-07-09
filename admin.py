import discord, asyncio, sys, traceback, checks, useful, asyncpg
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup', aliases=['botsetup', 'guildsettings', 'modules','modulesettings'])
    @checks.owner_or_admin()
    async def setup(self, ctx):
        embed = discord.Embed(title="Menu Loading...", description="Please stand by.", colour=self.bot.getcolour())
        menu = await ctx.channel.send(embed = embed)
        emojis = useful.getMenuEmoji(10)
        for emoji in range(0,len(emojis)):
            await menu.add_reaction(emojis[emoji])
        await self.setupMainMenu(ctx, menu)


    async def setupMainMenu(self, ctx, menu):
        embed = discord.Embed(title='Modules main menu', description="Here you can select which modules are enabled on this server.\n\nOptions:\n0: Administrator\n1: Miscellaneous\n2: Pub Quiz\n3: Bluetext\n4: Welcome\n5: Leave\n6: Games\n7: NSFW\n8: Next Page\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Current guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(9)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.setupAdminMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.setupMiscMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupPubQuizMenu(ctx, menu)

            elif str(reaction.emoji) == "3\u20e3":
                await self.setupBluetextMenu(ctx, menu)


            elif str(reaction.emoji) == "4\u20e3":
                await self.setupWelcomeMenu(ctx, menu)

            elif str(reaction.emoji) == "5\u20e3":
                await self.setupLeaveMenu(ctx, menu)


            elif str(reaction.emoji) == "6\u20e3":
                await self.setupGamesMenu(ctx, menu)


            elif str(reaction.emoji) == "7\u20e3":
                await self.setupNSFWMenu(ctx, menu)


            elif str(reaction.emoji) == "8\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()

    async def setupAdminMenu(self, ctx, menu):
        embed = discord.Embed(title='Administrator Module', description="This module contains the following commands.\n\nLIST COMING SOON\n\nOptions:\n0: Enable\n1: Disable\n2: Back to main menu\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Modules for guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(3)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.enableModule(ctx, "administrator")
                await self.setupAdminMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.disableModule(ctx, "administrator")
                await self.setupAdminMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()

    async def setupMiscMenu(self, ctx, menu):
        embed = discord.Embed(title='Miscellaneous Module', description="This module contains the following commands.\n\nLIST COMING SOON\n\nOptions:\n0: Enable\n1: Disable\n2: Back to main menu\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Modules for guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(3)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.enableModule(ctx, "misc")
                await self.setupMiscMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.disableModule(ctx, "misc")
                await self.setupMiscMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()

    async def setupPubQuizMenu(self, ctx, menu):
        embed = discord.Embed(title='Pub Quiz Module', description="This module contains the following commands.\n\nLIST COMING SOON\n\nOptions:\n0: Enable\n1: Disable\n2: Back to main menu\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Modules for guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(3)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.enableModule(ctx, "pubquiz")
                await self.setupPubQuizMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.disableModule(ctx, "pubquiz")
                await self.setupPubQuizMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()

    async def setupBluetextMenu(self, ctx, menu):
        embed = discord.Embed(title='Bluetext Module', description="This module contains the following commands.\n\nLIST COMING SOON\n\nOptions:\n0: Enable\n1: Disable\n2: Back to main menu\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Modules for guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(3)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.enableModule(ctx, "bluetext")
                await self.setupBluetextMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.disableModule(ctx, "bluetext")
                await self.setupBluetextMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()

    async def setupWelcomeMenu(self, ctx, menu):
        embed = discord.Embed(title='Welcome Module', description="This module contains the following commands.\n\nLIST COMING SOON\n\nOptions:\n0: Enable\n1: Disable\n2: Back to main menu\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Modules for guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(3)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.enableModule(ctx, "welcome")
                await self.setupWelcomeMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.disableModule(ctx, "welcome")
                await self.setupWelcomeMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()

    async def setupLeaveMenu(self, ctx, menu):
        embed = discord.Embed(title='Leave/Farewell Module', description="This module contains the following commands.\n\nLIST COMING SOON\n\nOptions:\n0: Enable\n1: Disable\n2: Back to main menu\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Modules for guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(3)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.enableModule(ctx, "leave")
                await self.setupLeaveMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.disableModule(ctx, "leave")
                await self.setupLeaveMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()

    async def setupGamesMenu(self, ctx, menu):
        embed = discord.Embed(title='Games Module', description="This module contains the following commands.\n\nLIST COMING SOON\n\nOptions:\n0: Enable\n1: Disable\n2: Back to main menu\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Modules for guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(3)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.enableModule(ctx, "games")
                await self.setupGamesMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.disableModule(ctx, "games")
                await self.setupGamesMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()

    async def setupNSFWMenu(self, ctx, menu):
        embed = discord.Embed(title='NSFW Module', description="This module contains the following commands.\n\nLIST COMING SOON\n\nOptions:\n0: Enable\n1: Disable\n2: Back to main menu\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Modules for guild: "+ ctx.guild.name +"("+ str(ctx.guild.id)+")")
        await menu.edit(embed=embed)
        options = useful.getMenuEmoji(3)
        def emojiCheck(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=emojiCheck, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the modules command to restart the process.")
            await menu.delete()
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.enableModule(ctx, "nsfw")
                await self.setupNSFWMenu(ctx, menu)

            elif str(reaction.emoji) == "1\u20e3":
                await self.disableModule(ctx, "nsfw")
                await self.setupNSFWMenu(ctx, menu)

            elif str(reaction.emoji) == "2\u20e3":
                await self.setupMainMenu(ctx, menu)

            elif str(reaction.emoji) == "❌":
                closed = await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()
                await asyncio.sleep(1)
                await closed.delete()


    async def enableModule(self, ctx, module):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET " + module + " = true WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.guild.id)
            await ctx.channel.send(":white_check_mark: | **'"+module+"'** module enabled.")
        await self.bot.db.release(connection)

    async def disableModule(self, ctx, module):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET " + module + " = false WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.guild.id)
            await ctx.channel.send(":white_check_mark: | **'"+module+"'** module disabled.")
        await self.bot.db.release(connection)

    # @commands.command(name='setup', aliases=['botsetup', 'su'])
    # @checks.is_not_banned()
    # @checks.owner_or_admin()
    # async def setup(self, ctx):
    #     if not ctx.guild:
    #         await ctx.author.send(":no_good: | This command can not be used in DM!")
    #     else:
    #         timeout = False
    #         choice = "choice"
    #         settings = [["Firstly", "Pub Quiz", "pubquizEnabled", "Allows the guild to run a weekly pub quiz complete with custom scoring! For full rules visit NOT DONE YET"],
    #                     ["Secondly", "Video Game", "gamesEnabled", "Allows users to attatch video game accounts to the bot to help with matchmaking."],
    #                     ["Next", "bluetext", "bluetextEnabled", "Enables a series of commands allowing members to use blue text emotes to construct sentences."],
    #                     ["Next", "welcome messages", "welcomeEnabled", "Enables a welcome message when users join the server. This can be set with tt!setwelcome and tt!setwelcometext commands"],
    #                     ["Next", "farewell messages", "leaveEnabled", "Enables a farewell message when the user leaves the server. This can be set with tt!setleave and tt!setleavetext commands"],
    #                     ["Finally", "admin", "adminEnabled", "Enables the bots administrator commands. For a list of commands please use UNDEFINED"]]
    #         options = ["info", "yes", "no", "skip"]
    #         embed = discord.Embed(title="Welcome to the TraaTan setup menu!", description="This menu allows you to decide which commands will work on this server. If you would like to grant or remove permissions from a specific role please use the UNDEFINED command!", colour=self.bot.getcolour())
    #         await ctx.channel.send(embed=embed)
    #         for setting in settings:
    #             print(setting)
    #             choice = "choice"
    #             while choice.lower() not in options and timeout == False:
    #                 embed = discord.Embed(title=(setting[0] + " - would you like to have " + setting[1] + " commands enabled?"), description="Options: `Yes`, `No`, `Info`, `Skip`",colour=self.bot.getcolour())
    #                 await ctx.channel.send(embed = embed)
    #                 try:
    #                     msg = await self.bot.wait_for('message', check=checks.setup_options1, timeout = 60.0)
    #                 except asyncio.TimeoutError:
    #                     try:
    #                         await ctx.channel.send(":no_entry: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
    #                     except TypeError:
    #                         await ctx.channel.send(":no_entry: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
    #                     timeout = True
    #                 else:
    #                     choice = msg.content
    #                     if choice.lower() == "yes":
    #                         connection = await self.bot.db.acquire()
    #                         async with connection.transaction():
    #                             query = "UPDATE Guilds SET "+ setting[2]+ " = true WHERE guildID = $1"
    #                             await self.bot.db.execute(query, ctx.guild.id)
    #                         await self.bot.db.release(connection)
    #                         await ctx.channel.send("Got it! "+ setting[1] +" commands have been enabled.")
    #                     elif choice.lower() == "no":
    #                         connection = await self.bot.db.acquire()
    #                         async with connection.transaction():
    #                             query = "UPDATE Guilds SET "+ setting[2] +" = false WHERE guildID = $1"
    #                             await self.bot.db.execute(query, ctx.guild.id)
    #                         await self.bot.db.release(connection)
    #                         await ctx.channel.send("Got it! "+ setting[1]+" commands have been disabled.")
    #                     elif choice.lower() == "info":
    #                         await ctx.channel.send(setting[3])
    #                         choice = "choice"
    #                     elif choice.lower() == "skip":
    #                         await ctx.channel.send("Got it! I've left your " + setting[1] + " settings as is!")
    #         if timeout == False:
    #             await ctx.channel.send("Thanks! You are all set up.")

    @commands.command(name = "exit", aliases =['quit'], hidden = True)
    @checks.justme()
    async def exit(self, ctx):
        await ctx.channel.send(":wave: Goodbye.")
        await self.bot.db.close()
        await self.bot.logout()
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

    @commands.command(name="setfarewell", aliases=['setleave', 'setleavechannel', 'setfarewellchannel'])
    @checks.leave_enabled()
    @checks.is_not_banned()
    @checks.rolescheck("setleavechannel")
    async def setfarewell(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET leavechannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Farewell channel set here.")

    @commands.command(name="setwelcome", aliases=['setwelcomechannel'])
    @checks.is_not_banned()
    @checks.welcome_enabled()
    @checks.rolescheck("setwelcomechannel")
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
    @checks.rolescheck("setwelcometext")
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
    @checks.rolescheck("setleavetext")
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
        successful = True
        while finished == 0:
            try:
                await ctx.author.send("Here is the data currently stored about you:")
            except:
                await ctx.channel.send("Please enable 'Allow direct messages from server members' under 'Privacy & Safety' in settings. For security reasons this information can not be posted publicly.")
                successful = False
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
        if successful:
            await ctx.channel.send(":white_check_mark: | Information sent to DM!")

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