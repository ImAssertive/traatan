import discord, asyncio, sys, traceback, checks, useful, asyncpg, random
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.justme()
    async def setgame(self, ctx, *, gameName):
        game = discord.Game(gameName)
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.channel.send(":white_check_mark: | Online status set to: ** playing: "+ gameName+"**")

    @commands.command(name='setup', aliases=['botsetup', 'guildsettings', 'modules','modulesettings', 'module','settings'])
    @checks.owner_or_admin()
    @checks.is_not_banned()
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

    @commands.command()
    @checks.justme()
    async def evalquery(self, ctx, *, query):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            try:
                await self.bot.db.execute(query)
                await ctx.channel.send(":white_check_mark: | Done!")
            except:
                await ctx.channel.send(":no_entry: | An error occurred.")
        await self.bot.db.release(connection)

    @commands.command()
    @checks.justme()
    async def printevalquery(self, ctx, *, query):
        result = await ctx.bot.db.fetch(query)
        await ctx.channel.send(str(result))



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
    @checks.module_enabled("leave")
    @checks.is_not_banned()
    @checks.rolescheck("setleavechannel")
    async def setfarewell(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET leavechannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done! Farewell channel set here.")

    @commands.command(name="setwelcome", aliases=['setwelcomechannel'])
    @checks.is_not_banned()
    @checks.module_enabled("welcome")
    @checks.rolescheck("setwelcomechannel")
    async def setwelcome(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET welcomechannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done! Welcome channel set here.")

    @commands.command()
    @checks.module_enabled("welcome")
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
    @checks.module_enabled("leave")
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

    @commands.command(name='setbantext')
    @checks.module_enabled("administrator")
    @checks.is_not_banned()
    @checks.rolescheck("setbantext")
    async def setbantext(self, ctx, *, banText):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET bantext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, banText,ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Ban text set to `"+banText+"`!")

    @commands.command(name='setkicktext')
    @checks.module_enabled("administrator")
    @checks.is_not_banned()
    @checks.rolescheck("setkicktext")
    async def setkicktext(self, ctx, *, kickText):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET kicktext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, kickText,ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Kick text set to `"+kickText+"`!")

    @commands.command()
    @checks.module_enabled("administrator")
    @checks.is_not_banned()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, *, reason):
        memberid = int(useful.getid(member))
        confirmationnumber = random.randint(1000, 9999)
        embed = discord.Embed(title="You are about to kick user: "+ctx.guild.get_member(memberid).display_name, description="This action is irreversable. To continue please type `" + str(confirmationnumber)+"` or to cancel, please type `cancel`.", colour=self.bot.getcolour())
        embed.add_field(name='User ID: ', value=str(ctx.guild.get_member(memberid).id), inline=False)
        embed.add_field(name='User discord name: ', value=ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator, inline=False)
        embed.add_field(name='Reason: ', value=reason, inline=False)
        kickinfo = await ctx.channel.send(embed=embed)
        def confirmationcheck(msg):
            return (msg.content == str(confirmationnumber) or msg.content.lower() == "cancel") and ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id
        try:
            msg = await self.bot.wait_for('message', check=confirmationcheck, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The reset command has closed due to inactivity.")
        else:
            if msg.content == str(confirmationnumber):
                embed = discord.Embed(title=":exclamation: | You have been kicked from " + ctx.guild.name, description="You have been kicked from "+ ctx.guild.name+ ". Details of this kick including reason and user are listed below.", colour=self.bot.getcolour())
                embed.add_field(name="User (You):", value=ctx.guild.get_member(memberid).mention + " " + ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator + " `" + str(ctx.guild.get_member(memberid).id)+"`", inline=False)
                embed.add_field(name="Issued by:", value=ctx.author.mention + " " + ctx.author.name +"#" +ctx.author.discriminator + " `" + str(ctx.author.id)+"`", inline=False)
                embed.add_field(name="Reason:", value=reason, inline=False)
                query = "SELECT * FROM guilds WHERE guildID = $1 AND kicktext IS NOT NULL"
                results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
                if results:
                    embed.add_field(name="Message from server:", value=results["kicktext"])
                await ctx.channel.send(":white_check_mark: | Kicking user...")
                await ctx.guild.get_member(memberid).send(embed=embed)
                await ctx.guild.get_member(memberid).kick(reason=reason)

            elif msg.content.lower() == "cancel":
                await ctx.channel.send(":white_check_mark: | Canceled!")
                await kickinfo.delete()

    @commands.command()
    @checks.module_enabled("administrator")
    @checks.is_not_banned()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, *, reason):
        memberid = int(useful.getid(member))
        confirmationnumber = random.randint(1000, 9999)
        embed = discord.Embed(title="You are about to ban user: " + ctx.guild.get_member(memberid).display_name, description="This action is irreversable. To continue please type `" + str(confirmationnumber) + "` or to cancel, please type `cancel`.",colour=self.bot.getcolour())
        embed.add_field(name='User ID: ', value=str(ctx.guild.get_member(memberid).id), inline=False)
        embed.add_field(name='User discord name: ',value=ctx.guild.get_member(memberid).name + "#" + ctx.guild.get_member(memberid).discriminator,inline=False)
        embed.add_field(name='Reason: ', value=reason, inline=False)
        baninfo = await ctx.channel.send(embed=embed)
        def confirmationcheck(msg):
            return (msg.content == str(confirmationnumber) or msg.content.lower() == "cancel") and ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id
        try:
            msg = await self.bot.wait_for('message', check=confirmationcheck, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The reset command has closed due to inactivity.")
        else:
            if msg.content == str(confirmationnumber):
                embed = discord.Embed(title=":exclamation: | You have been banned from " + ctx.guild.name,description="You have been banned from " + ctx.guild.name + ". Details of this ban including reason and user are listed below.",colour=self.bot.getcolour())
                embed.add_field(name="User (You):", value=ctx.guild.get_member(memberid).mention + " " + ctx.guild.get_member(memberid).name + "#" + ctx.guild.get_member(memberid).discriminator + " `" + str(ctx.guild.get_member(memberid).id) + "`", inline=False)
                embed.add_field(name="Issued by:", value=ctx.author.mention + " " + ctx.author.name + "#" + ctx.author.discriminator + " `" + str(ctx.author.id) + "`", inline=False)
                embed.add_field(name="Reason:", value=reason, inline=False)
                query = "SELECT * FROM guilds WHERE guildID = $1 AND bantext IS NOT NULL"
                results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
                if results:
                    embed.add_field(name="Message from server:", value=results["bantext"])
                await ctx.channel.send(":white_check_mark: | Banning user...")
                await ctx.guild.get_member(memberid).send(embed=embed)
                await ctx.guild.get_member(memberid).ban(reason=reason)

            elif msg.content.lower() == "cancel":
                await ctx.channel.send(":white_check_mark: | Canceled!")
                await baninfo.delete()
def setup(bot):
    bot.add_cog(adminCog(bot))