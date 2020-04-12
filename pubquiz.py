import discord, asyncio, sys, traceback, checks, random, useful, inflect, random, re, math
from discord.ext import commands

class pubquizCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##Defines a pub quiz command group
    @commands.group(pass_context=True, name='pubquiz', aliases=['pq','pubq'])
    async def pubquiz(self, ctx):
        ##Replies to users when no pubquiz subcommand is called (IE user only types tt!pubquiz)
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("Please enter a command. tt!help or tt!pubquiz help for a list of commands.")

    ##Command that users to update the introduction text for pub quiz
    @pubquiz.command(name='settext', aliases=['stext'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Bot Tinkerer")
    @checks.has_role("User")
    async def settext(self, ctx, *, pubquiztext):
        ##Creates new connection to database
        connection = await self.bot.db.acquire()
        ##Updates appropriate section in database
        async with connection.transaction():
            query = "UPDATE Guilds SET pubquiztext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, pubquiztext,ctx.guild.id)
        ##Closes open connection to database
        await self.bot.db.release(connection)

        ##Confirms message change with the user
        await ctx.channel.send(":white_check_mark: | Pub quiz text set to `"+pubquiztext+"`!")

    ##Command that outputs the current state of the pub quiz
    @pubquiz.command(name='isactive', aliases=['active'])
    @commands.has_permissions(kick_members=True)
    async def isactive(self, ctx):
        ##Queries database using guild ID
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)

        ##Returns message to the user depending on the results of the ongoingpubquiz bool
        if result["ongoingpubquiz"]:
            await ctx.channel.send(":exclamation: | The pub quiz is currently active in channel: **" + ctx.guild.get_channel(int(result["pubquizchannel"])).name + "** with host: **"+ctx.guild.get_member(int(result["pubquizquestionuserid"])).name+"**")
        else:
            await ctx.channel.send(":no_entry: | The pub quiz is not currently active.")

    ##Command that allows users to update the end text for the pubquiz
    @pubquiz.command(name='setendtext', aliases=['sendtext'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Helper Powers", "Moderator Powers","Admin Powers", "Bot Tinkerer")
    @checks.has_role("User")
    async def setendtext(self, ctx, *, pubquizendtext):
        ##Creates new connection to database
        connection = await self.bot.db.acquire()
        ##Updates appropriate field in database
        async with connection.transaction():
            query = "UPDATE Guilds SET pubquizendtext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, pubquizendtext,ctx.guild.id)
        ##Closes open connection to datansae
        await self.bot.db.release(connection)

        ##Confirms message change to the user
        await ctx.channel.send(":white_check_mark: | Pub quiz end text set to `"+pubquizendtext+"`!")

    ##Command that allows for all scores to be reset to 0
    @pubquiz.command(name="resetguildscoreboard", aliases=['resetscore', 'reset', 'resetall'])
    @checks.justme()
    async def resetguildscoreboard(self, ctx):
        ##Queries database to determine if the pub quiz is active
        query = "SELECT * FROM guilds WHERE guildID = $1 AND ongoingpubquiz = true"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)

        #If the quiz is currently active outputs an error message message to the user
        if result:
            await ctx.channel.send(":no_entry: | **"+ctx.author.display_name+"** a pub quiz is already active! Please end the current pub quiz to continue.")
        else:
            ##If the quiz is not active, display the randomly generated confirmation to the user to confirm their choice
            confirmationNumber = random.randint(1000, 9999)
            await ctx.channel.send(":clock1: | **"+ctx.author.display_name+"** are you sure? This will completely reset the pub quiz scores for the entire guild. To continue please type `"+ str(confirmationNumber) +"`")
            def confirmationcheck(msg):
                return msg.content == str(confirmationNumber) and ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id
            try:
                ##Checks for the user to reply with the confirmation number as the content
                msg = await self.bot.wait_for('message', check=confirmationcheck, timeout=60.0)
            except asyncio.TimeoutError:
                ##If the user does not reply in time, output appropriate error message
                await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The reset command has closed due to inactivity.")
            else:
                ##If the user replies and the contents is equal to the generated confirmation number
                if msg.content == str(confirmationNumber):
                    ##Creates new connection to the database, update the users table so all scores are 0
                    connection = await self.bot.db.acquire()
                    async with connection.transaction():
                        query = "UPDATE Users SET pubquizscoretotal = 0"
                        await self.bot.db.execute(query)
                    ##Closes connection to the database
                    await self.bot.db.release(connection)
                    ##Sends message to user confirming that the scores have been reset
                    await ctx.channel.send(":white_check_mark: | Pub quiz scores reset!")

    ##Command that allows users to start a new pub quiz
    @pubquiz.command(name='start', aliases=['begin', 'go'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Bot Tinkerer")
    @checks.has_role("User")
    async def start(self, ctx):
        ##Calls the addmembers command from the setup cog, ensures that no errors arise from users not being registered
        await ctx.bot.get_cog('setupCog').addmembers.invoke(ctx)

        ##Queries the database to determine if a pubquiz is currently active
        query = "SELECT * FROM guilds WHERE guildID = $1 AND ongoingpubquiz = true"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        ##Returns a message to the user if a quiz is currently active
        if result:
            await ctx.channel.send(":no_entry: | A quiz is already active!")
        else:
            ##Creates new roll so that the bot can determine who to DM questions too
            dmRole = await ctx.guild.create_role(name = "Pub Quiz DM", reason="Traatan Automatic Pubquiz DM Role Creation")
            ##Adds new entry into the bots rolls dictionary for the pub quiz DM roll
            ctx.bot.rolesDict["Pub Quiz DM"] = int(dmRole.id)

            ##Creates new connection to the database
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                ##Updates relevant tables in the database
                query = "UPDATE Guilds SET ongoingpubquiz = true WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
                query = "UPDATE Guilds SET pubquizchannel = $1 WHERE guildID = $2"
                await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
                query = "UPDATE Users SET pubquizscoreweekly = 0"
                await self.bot.db.execute(query)
                query = "UPDATE Guilds SET pubquizquestionnumber = 0 WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
                query = "UPDATE Guilds SET dmroleid = $1 WHERE guildID = $2"
                await self.bot.db.execute(query, dmRole.id, ctx.guild.id)
            ##Closes connection to the database
            await self.bot.db.release(connection)
            ##Updates flags attatched to the bot object
            self.bot.pubquizActive = True
            self.bot.pubquizChannel = ctx.channel.id

            ##Queries the database to determine to determine if any text for the pub quiz has been set
            query = "SELECT * FROM guilds WHERE guildID = $1 AND pubquiztext IS NOT NULL"
            results = await ctx.bot.db.fetchrow(query, ctx.guild.id)

            ##If the guild has set custom text then it is formatted, else a default statement is added instead.
            if results:
                pubquiztext = ("{}".format(results["pubquiztext"]))
            else:
                pubquiztext = "Pub Quiz Started!"

            ##Creates a discord.Embed object using the previously created text variable
            resultsEmbed = discord.Embed(title=pubquiztext, description="Use the `tt!pq dm` command to enable receiving questions via DM's!", colour=self.bot.getcolour())
            ##Outputs embed to channel invoking the start command
            await ctx.channel.send(embed=resultsEmbed)

    ##Command to toggle a user receiving pub quiz questions as direct messages
    @pubquiz.command(name='dm', aliases=['dmme', 'toggledms', 'toggledm'])
    @checks.pubquiz_active()
    @checks.has_role("User")
    async def dm(self, ctx):
        ##Checks if the user invoking the command is someone that is running the quiz
        quizmasterCheck = await checks.has_role_not_check(ctx, "Quizmaster", "Pub Quiz Senate")
        if not quizmasterCheck or ctx.author.id == 163691476788838401:
            ##If not then attempts to obtain the correct role that signifies a user to DM
            try:
                dmRole = discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["Pub Quiz DM"])
            except:
                ##Outputs error message to console
                print("DM Role Not Found (Something has gone very wrong)")
            ##Checks if the user invoking the command already has the DM role or not
            rolecheck = await checks.has_role_not_check(ctx, dmRole.name)
            if rolecheck:
                ##Creates appropriate embed with link back to the channel where the command was originally invoked
                embed = discord.Embed(title="I will no longer DM you questions.", description=ctx.channel.mention+ctx.channel.mention+ctx.channel.mention+ctx.channel.mention+ctx.channel.mention, colour=self.bot.getcolour())
                ##Remove users DM role
                await ctx.author.remove_roles(dmRole, reason="User requested role removal.")
                ##Sends embed to user
                await ctx.author.send(embed=embed)
            else:
                ##Creates appropriate embed with link back to the channel where the command was originally invoked
                embed = discord.Embed(title="Got it! I'll DM you questions.", description = ctx.channel.mention+ctx.channel.mention+ctx.channel.mention+ctx.channel.mention+ctx.channel.mention, colour=self.bot.getcolour())
                ##Gives user DM role
                await ctx.author.add_roles(dmRole, reason="User requested role addition.")
                ##Sends embed to user
                await ctx.author.send(embed=embed)
            ##Adds a white check mark reaction to the users original command
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @pubquiz.command(name='stop', aliases =['end', 'halt'])
    @checks.pubquiz_active()
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Bot Tinkerer")
    @checks.has_role("User")
    async def stop(self, ctx):
        ##Queries database to determine if the guild in which this command has been called has any saved text for the end of a pub quiz
        query = "SELECT * FROM guilds WHERE guildID = $1 AND pubquizendtext IS NOT NULL"
        results = await ctx.bot.db.fetchrow(query, ctx.guild.id)

        ##If there are results then send them to the channel where this command was invoked
        if results:
            pubquizendtext = ("{}".format(results["pubquizendtext"]))
            await ctx.channel.send(pubquizendtext)
        else:
            #If there is no saved message under the guild ID, sends a  default message
            await ctx.channel.send("That was the pub quiz! I hope you enjoyed. :)")

        #Obtains discord embed objects from the getLeaderboards function
        leaderboardEmbeds = await self.getLeaderboard(ctx)
        for embed in leaderboardEmbeds:
            ##Outputs final leaderboard in channel where end command was invoked
            await ctx.channel.send(embed=embed)

        ##Gets current saved data on guild from database
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)

        ##Attempts to delete whichever role is being used as the pub quiz DM role so users are not sent questions from
        #next weeks quiz
        try:
            await discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["Pub Quiz DM"]).delete()
        except:
            print("DM Role not found.")
        #Deletes pub quiz role key from the bots role dictionary
        try:
            del ctx.bot.rolesDict["Pub Quiz DM"]
        except KeyError:
            print("DM Role not found in rolesDict.")
            pass

        ##Creates new connection to DB
        connection = await self.bot.db.acquire()
        ##Updates relevant sections of the database so flags are not kept if the bot crashes
        async with connection.transaction():
            query = "UPDATE Guilds SET ongoingpubquiz = false WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.guild.id)
            query = "UPDATE Guilds SET pubquizchannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, None, ctx.guild.id)
            query = "UPDATE Guilds SET pubquizquestionnumber = 0 WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.guild.id)
            query = "UPDATE Guilds SET dmroleid = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, None, ctx.guild.id)
        #Closes DB connection
        await self.bot.db.release(connection)
        ##Updates pubquiz bool stored on bot object
        self.bot.pubquizActive = False

    #Returns an array of embeds containing information on the weekly leaderboard for a pub quiz
    async def getLeaderboard(self, ctx, total=False):
        ##Checks if the function should be returning the weekly or total leaderboards, queries database for appropriate results
        if total:
            ##Queries database for all users with a total score above 0, orders results in decending order
            query = "SELECT * FROM users WHERE pubquizscoretotal != 0 ORDER BY pubquizscoretotal DESC"
            result = await ctx.bot.db.fetch(query)
        else:
            ##Queries database for all users with a weekly score above 0, orders results in decending order
            query = "SELECT * FROM users WHERE pubquizscoreweekly != 0 ORDER BY pubquizscoreweekly DESC"
            result = await ctx.bot.db.fetch(query)

        ##Calculates how many embeds are needed to cover all users with a score above 0 & creates empty array for completed embeds
        pages = []
        totalPages = math.ceil(len(result)/25)

        for page in range(0, totalPages):
            ##Creates a new discord embed object and sets the footer to the current page number
            resultsEmbed = discord.Embed(title= ctx.guild.name + " Pub Quiz Leaderboard:", colour=self.bot.getcolour())
            resultsEmbed.set_footer(text="Current Page: (" + str(page+1) + "/" + str(totalPages) + ")")

            ##Check if the bot is on the last page of results, if so then prevent bot from iterating past end of results
            if (page+1) == totalPages:
                finalResult = len(result)
            else:
                finalResult = (page+1) * 25

            ##Iterate over appropriate results from database, adding relevant information to newly created discord embed
            for row in range (page*25,finalResult):
                try:
                    if total:
                        resultsEmbed.add_field(name=ctx.guild.get_member(
                            int(result[row]["userid"])).display_name + " (" + ctx.guild.get_member(
                            int(result[row]["userid"])).name + "#" + ctx.guild.get_member(
                            int(result[row]["userid"])).discriminator + ")", value="has a total of **" + str(
                            result[row]["pubquizscoretotal"]) + "** points. Placing them **" + inflect.engine().ordinal(
                            row + 1) + "**.", inline=False)
                    else:
                        resultsEmbed.add_field(name=ctx.guild.get_member(int(result[row]["userid"])).display_name + " ("+ctx.guild.get_member(int(result[row]["userid"])).name +"#" +ctx.guild.get_member(int(result[row]["userid"])).discriminator + ")", value="has a total of **" + str(result[row]["pubquizscoreweekly"]) + "** points. Placing them **"+ inflect.engine().ordinal(row + 1) + "**. ("+str(result[row]["pubquizscoretotal"])+" total points)", inline=False)

                except:
                    ##Prevents error if user has left the guild when attempting to retrieve results
                    resultsEmbed.add_field(name="User left guild", value="Data not found.", inline=False)

            #Adds final embed to array to be returned
            pages.append(resultsEmbed)
        return pages

    #Outputs the current total results of a pub quiz season to a user or in a channel
    @pubquiz.command(name="totalleaderboard", aliases=['total', 'totalscoreboard', 'totalscores','totalscore'])
    @checks.has_role("User")
    async def totalleaderboard(self, ctx):
        #Determines if the user invoking the command has permission to post the leaderboards publicly
        rolecheck = await checks.has_role_not_check(ctx, "Quizmaster", "Pub Quiz Senate")

        #Obtains array of leaderboard embeds from the getLeaderboards function
        embeds = await self.getLeaderboard(ctx, total=True)
        for embed in embeds:
            ##If the user has permission, send the results to the channel the command was invoked in
            if rolecheck:
                await ctx.channel.send(embed=embed)
            ##Else directly message the user with results
            else:
                await ctx.author.send(embed=embed)

    #Outputs the weekly results of a pub quiz to a user or in a channel
    @pubquiz.command(name="leaderboard", aliases=['scoreboard', 'score', 'scores'])
    @checks.pubquiz_active()
    @checks.has_role("User")
    async def leaderboard(self, ctx):
        #Determines if the user invoking the command has permission to post the leaderboards publicly
        rolecheck = await checks.has_role_not_check(ctx, "Quizmaster", "Pub Quiz Senate")

        #Obtains array of leaderboard embeds from the getLeaderboards function
        embeds = await self.getLeaderboard(ctx)

        for embed in embeds:
            if rolecheck:
                ##If the user has permission, send the results to the channel the command was invoked in
                await ctx.channel.send(embed=embed)
            else:
                ##Else directly message the user with results
                await ctx.author.send(embed=embed)

    @pubquiz.command(name="override", aliases=['or', 'oride'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    async def override(self, ctx, member, value):
        #Checks if the given value is an integer, outputting a message to the user if not
        successful = True
        try:
            value = int(value)
        except:
            await ctx.channel.send(":no_entry: | Please enter a whole number to add or subtract from the users score.")
            successful = False


        if successful and value != 0:
            #Obtains the users ID and queries database to obtain their current weekly and total scores
            memberid = useful.getid(member)
            query = "SELECT * FROM users WHERE userID = $1"
            result = await ctx.bot.db.fetchrow(query, memberid)
            currentValue = result["pubquizscoreweekly"]
            currentTotal = result["pubquizscoretotal"]

            #Creates new connection to database
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                #Updates the users weekly and total score to add the supplied value (can be negative)
                query = "UPDATE users SET pubquizscoreweekly = $1 WHERE userID = $2"
                await self.bot.db.execute(query, currentValue + value, memberid)
                query = "UPDATE users SET pubquizscoretotal = $1 WHERE userID = $2"
                await self.bot.db.execute(query, currentTotal + value, memberid)
            #Closes database connection
            await self.bot.db.release(connection)
            #Outputs message to user depending on if the targets score has increased or decreased
            if value > 0:
                await ctx.channel.send(":white_check_mark: | User **"+ctx.guild.get_member(memberid).display_name + " (" +ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator +")** has had their weekly and total score increased by **" + str(value) + "**. Their new total is **"+str(currentTotal + value)+"** overall and **"+ str(currentValue + value)+"** this week.")
            elif value < 0:
                await ctx.channel.send(":white_check_mark: | User **"+ctx.guild.get_member(memberid).display_name + " (" +ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator +")** has had their weekly and total score reduced by **" + str(value*-1) + "**. Their new total is **"+str(currentTotal + value)+"** overall and **"+ str(currentValue + value)+"** this week.")
        elif value == 0:
            #Outputs message to user if the entered value is 0
            await ctx.channel.send(":no_entry: | The score can not be modified by 0.")

    @pubquiz.command(name="settime", aliases=['st'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    @checks.has_role("User")
    async def settime(self, ctx, time):
        ##Checks if the entered number is a positive whole integer
        success = True
        try:
            time = int(time)
        except:
            success = False
        if success:
            ##Checks if the entered integer is between 1 and 60 seconds
            if time > 0 and time < 61:
                ##Creates new connection to database
                connection = await self.bot.db.acquire()
                ##Updates relevant database sections
                async with connection.transaction():
                    query = "UPDATE Guilds SET pubquiztime = $1 WHERE guildID = $2"
                    await self.bot.db.execute(query, time, ctx.guild.id)
                ##Closes open database connection
                await self.bot.db.release(connection)
                ##Outputs success message to user
                await ctx.channel.send(":white_check_mark: | Default time set to **" + str(time) + "** seconds.")
            else:
                ##Outputs message to user if entered number is outside of valid range
                await ctx.channel.send(":no_entry: | Time must be between 1 and 60 seconds.")
        else:
            ##Outputs message to user if a valid time number was supplied
            await ctx.channel.send(":no_entry: | Please enter a positive whole time number.")

    ##Literally just the correct command but with will subtract points instead of add them, used for debugging.
    @pubquiz.command(name="undo")
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    async def undo(self, ctx):
        ##Uses regex to find the ID of all correct members if mentions have been used
        correctMembers = re.findall("<@.*?>", ctx.message.content)
        ##Iterates over correct members
        for i in range(0,len(correctMembers)):
            correctMembers[i] = useful.getid(correctMembers[i])
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        embed = discord.Embed(title="Reduced the following users scores:", colour = self.bot.getcolour())
        connection = await self.bot.db.acquire()
        for i in range (0, len(correctMembers)): ##<------------------------------------------
            memberid = correctMembers[i]
            if result["pubquizlastquestionsuper"] == True:
                toAdd = round(25/len(correctMembers))
            elif len(correctMembers) == 1 and result["pubquizlastquestionsuper"] == False:
                toAdd = 16
            else:
                toAdd = 13-i
                if toAdd < 10:
                    toAdd = 10
            query = "SELECT * FROM users WHERE userID = $1"
            results = await ctx.bot.db.fetchrow(query, memberid)
            currentValue = results["pubquizscoreweekly"]
            currentTotal = results["pubquizscoretotal"]
            async with connection.transaction():
                query = "UPDATE users SET pubquizscoreweekly = $1 WHERE userID = $2"
                await self.bot.db.execute(query, currentValue - toAdd, memberid)
                query = "UPDATE users SET pubquizscoretotal = $1 WHERE userID = $2"
                await self.bot.db.execute(query, currentTotal - toAdd, memberid)
            embed.add_field(name=ctx.guild.get_member(memberid).display_name + " (" +ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator+")", inline=False, value="lost **"+ str(toAdd) + "** points.")
        await self.bot.db.release(connection)
        await ctx.channel.send(embed=embed)


    @pubquiz.command(name="correct")
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    async def correct(self, ctx):
        ##Uses regex to find the ID of all correct members if mentions have been used
        correctMembers = re.findall("<@.*?>", ctx.message.content)

        ##Iterates over mentions of correct members, obtaining their ID
        for i in range(0,len(correctMembers)):
            correctMembers[i] = useful.getid(correctMembers[i])

        ##Queries database for current pub quiz settings
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)

        ##Creates an empty array to be filled with discord embeds
        pages = []
        totalPages = math.ceil(len(correctMembers)/25)

        #Creates an appropriate number of embeds to add users too
        for j in range(0, totalPages):
            toAppend = discord.Embed(title="The following users were correct:", colour = self.bot.getcolour())
            #Sets the footer of each page to the correct page number
            toAppend.set_footer(text="Current Page: (" + str(j+1) +"/" + str(totalPages)+")")
            #Appends newly created embed to a list
            pages.append(toAppend)

        #Creates new database connection
        connection = await self.bot.db.acquire()
        for i in range (0, len(correctMembers)):
            memberid = correctMembers[i]
            #Calculates the correct amount of points to award each member depending on if the last question was a SQ or not
            if result["pubquizlastquestionsuper"] == True:
                toAdd = round(25/len(correctMembers))
                if toAdd == 12:
                    toAdd = 13
            elif len(correctMembers) == 1 and result["pubquizlastquestionsuper"] == False:
                toAdd = 16
            else:
                toAdd = 13-i
                if toAdd < 10:
                    toAdd = 10

            #Queries database to find users current points
            query = "SELECT * FROM users WHERE userID = $1"
            results = await ctx.bot.db.fetchrow(query, memberid)
            currentValue = results["pubquizscoreweekly"]
            currentTotal = results["pubquizscoretotal"]

            #Connects to database and updates users weekly and total scores
            async with connection.transaction():
                query = "UPDATE users SET pubquizscoreweekly = $1 WHERE userID = $2"
                await self.bot.db.execute(query, currentValue + toAdd, memberid)
                query = "UPDATE users SET pubquizscoretotal = $1 WHERE userID = $2"
                await self.bot.db.execute(query, currentTotal + toAdd, memberid)

            ##Adds the appropriate confirmation text to one of the embeds
            pages[math.ceil(i/25)-1].add_field(name=ctx.guild.get_member(memberid).display_name + " (" +ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator+")", inline=False, value="gained **"+ str(toAdd) + "** points.")
        #Closes database connection
        await self.bot.db.release(connection)

        #Sends all embeds to context object channel
        for embed in pages:
            await ctx.channel.send(embed=embed)

    #Help command
    @pubquiz.command()
    @checks.has_role("User")
    async def help(self, ctx):
        #Creates an embed filled with useful information on commands and returns it to the user
        embed = discord.Embed(title="PubQuiz Help", description="Help for the following tt!pubquiz commands:", colour=self.bot.getcolour())
        embed.add_field(name="total", value ="DM's the user the total scoreboard for the pub quiz.")
        embed.add_field(name="leaderboard", value ="DM's the user the weekly scoreboard. Can only be used when a pub quiz is active.")
        await ctx.channel.send(embed = embed)



    #Quizmasters Help Command
    @pubquiz.command()
    @checks.has_role("User")
    @checks.has_role("Quizmaster", "Pub Quiz Senate")
    async def qmhelp(self, ctx):
        #Creates an embed filled with useful information on commands and returns it to the user
        embed = discord.Embed(title="PubQuiz Quizmaster Help", description="Help for the following tt!pubquiz commands:", colour=self.bot.getcolour())
        embed.add_field(name="settext", value ="Changes the text the bot sends when a new pub quiz is started.")
        embed.add_field(name="setendtext", value ="Changes the text the bot sends when a pub quiz ends.")
        embed.add_field(name="reset", value ="Resets the total leaderboard for the guild. Use with caution.")
        embed.add_field(name="leaderboard", value ="Posts the weekly leaderboard in the channel where the pubquiz was started. If the user does not have permission the leaderboard will instead be DM'ed to them.")
        embed.add_field(name="total", value ="Posts the total leaderboard. If the user does not have permission the leaderboard will instead be DM'ed to them.")
        embed.add_field(name="start", value ="Starts the weeks Pub Quiz!")
        embed.add_field(name="stop", value ="End the weeks Pub Quiz!")
        embed.add_field(name="question", value ="Sends a new question to everyone! Default time is 10.")
        embed.add_field(name="superquestion", value ="Sends a new super question to everyone! Default time is 10.")
        embed.add_field(name="settime", value ="Changes the default time in seconds people have to answer questions.")
        embed.add_field(name="correct", value ="Updates the points gained values for these users. Fastest user should be entered first with slowest user last.")
        embed.add_field(name="undo", value ="Reduces the points gained values for these users. Fastest user should be entered first with slowest user last.")
        embed.add_field(name="override", value ="Overrides the mentioned users score, this allows for mistakes to be quickly corrected. Correct usage is tt!pq or @user (amount of points)")
        embed.add_field(name="answer", value ="Gets the bot to echo the answer. Correct usage is tt!pq answer (Answer)")
        await ctx.channel.send(embed = embed)

    #Command to allow a quizmaster to start a new question
    @pubquiz.command(name='question', aliases=['q'])
    @checks.pubquiz_active()
    @checks.has_role("Quizmaster", "Pub Quiz Senate")
    @checks.has_role("User")
    async def question(self, ctx, *, question):
        #Calls the question function, setting the superQuestion bool to false
        superQuestion = False
        await self.questionFunction(ctx, question, superQuestion)

    #Command to allow a quizmaster to start a new super question (awarding bonus points)
    @pubquiz.command(name='superquestion', aliases=['sq', 'spq'])
    @checks.pubquiz_active()
    @checks.has_role("Quizmaster", "Pub Quiz Senate")
    @checks.has_role("User")
    async def superquestion(self, ctx, *, question):
        #Calls the question function, setting the superQuestion bool to false
        superQuestion = True
        await self.questionFunction(ctx, question, superQuestion)

    #Allows a quizmaster to display the answer in an easy to read embed
    @pubquiz.command(name="answer")
    @checks.has_role("Quizmaster", "Pub Quiz Senate")
    @checks.has_role("User")
    @checks.pubquiz_active()
    async def answer(self, ctx, *, answer):
        #Creates a discord embed object before sending it to the channel where the command was invoked
        embed = discord.Embed(title="The answer is...", description = answer, colour=self.bot.getcolour())
        await ctx.channel.send(embed=embed)

        #Deletes the original invoke message
        await ctx.message.delete()

    async def questionFunction(self, ctx, question, superQuestion):
        #Gets current status of guild from database
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)

        #Checks if there is currently a question active
        if result["pubquizquestionactive"] == False:
            #Clears any saved answers the bot may have
            self.bot.pubquizAnswers = []
            #Obtains current question number from results and increments it by 1
            currentquestion = result["pubquizquestionnumber"]
            currentquestion += 1

            #Updates databases store on if a question is active/who asked the last question.
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE Guilds SET pubquizquestionnumber = $1 WHERE guildID = $2"
                await self.bot.db.execute(query, currentquestion, ctx.guild.id)
                query = "UPDATE Guilds SET pubquizquestionactive = true WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
                query = "UPDATE Guilds SET pubquizquestionuserid = $1 WHERE guildID = $2"
                await self.bot.db.execute(query, ctx.author.id, ctx.guild.id)
            #Updates bots local store on if a question is active/who asked the last question
            self.bot.pubquizQuestionUserID = ctx.author.id
            self.bot.pubquizQuestionActive = True

            #Creates relevant embeds for questions and superquestions to be sent to users in the channel and in direct messages
            if superQuestion:
                questionEmbed = discord.Embed(title="**SUPER QUESTION " + str(currentquestion) + "!**", description=question, colour=self.bot.getcolour())
                questionDMEmbed = discord.Embed(title="**SUPER QUESTION " + str(currentquestion) + "!**", description=question, colour=self.bot.getcolour())
                questionEmbed.add_field(name="Please type your answers now.", value = ctx.bot.user.mention +" "+ctx.bot.user.mention +" "+ctx.bot.user.mention +" "+ctx.bot.user.mention +" "+ctx.bot.user.mention +" ")
                questionDMEmbed.add_field(name="Please type your answers now.", value = ctx.channel.mention+ctx.channel.mention+ctx.channel.mention+ctx.channel.mention+ctx.channel.mention)
                #Flags the last question as being a super question so that points can be determined correctly
                async with connection.transaction():
                    query = "UPDATE Guilds SET pubquizlastquestionsuper = true WHERE guildID = $1"
                    await self.bot.db.execute(query, ctx.guild.id)
            else:
                questionEmbed = discord.Embed(title="**Question " + str(currentquestion) + "!**", description=question, colour=self.bot.getcolour())
                questionEmbed.add_field(name="Please type your answers now.", value =ctx.bot.user.mention +" "+ctx.bot.user.mention +" "+ctx.bot.user.mention +" "+ctx.bot.user.mention +" "+ctx.bot.user.mention +" ")
                questionDMEmbed = discord.Embed(title="**Question " + str(currentquestion) + "!**", description=question, colour=self.bot.getcolour())
                questionDMEmbed.add_field(name="Please type your answers now.", value = ctx.channel.mention+ctx.channel.mention+ctx.channel.mention+ctx.channel.mention+ctx.channel.mention)
                async with connection.transaction():
                    #Flags the last question as not being a super question so points can be determined correctly
                    query = "UPDATE Guilds SET pubquizlastquestionsuper = false WHERE guildID = $1"
                    await self.bot.db.execute(query, ctx.guild.id)
            await self.bot.db.release(connection)

            #DM's all members on the server that have the pubquiz DM role
            dmRole = discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["Pub Quiz DM"])
            for member in ctx.guild.members:
                if dmRole in member.roles:
                    await member.send(embed=questionDMEmbed)
            #Sends the question embed to the channel where the question command was invoked
            await ctx.channel.send(embed=questionEmbed)

            #Waits for answers before closing answers for submission
            await asyncio.sleep(result["pubquiztime"])
            await ctx.channel.send("Answers are now closed!")
            print(self.bot.pubquizAnswers)

            #Updates database/client flags so that the question is no longer active
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE Guilds SET pubquizquestionactive = false WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
            await self.bot.db.release(connection)
            self.bot.pubquizQuestionActive = False

            pages = []
            totalPages = math.ceil(len(self.bot.pubquizAnswers)/25)

            # Creates an appropriate number of embeds to add users too
            for i in range(0, totalPages):
                toAppend = discord.Embed(title="Answers:", colour=self.bot.getcolour())
                # Sets the footer of each page to the correct page number
                toAppend.set_footer(text="Current Page: (" + str(i + 1) + "/" + str(totalPages) + ")")
                # Appends newly created embed to a list
                pages.append(toAppend)

            #Loops over answers provided, adding them to the correct embed
            for answer in range(0, len(self.bot.pubquizAnswers)):
                if self.bot.pubquizAnswers[answer][1] == ctx.guild.id:
                    pages[math.ceil(answer/25)].add_field(
                        name=self.bot.pubquizAnswers[answer][0].display_name + " (" + self.bot.pubquizAnswers[answer][
                            0].name + "#" + self.bot.pubquizAnswers[answer][0].discriminator + ") answered:",
                        value=self.bot.pubquizAnswers[answer][2], inline=False)

            #Outputs final results embeds
            for embed in pages:
                await ctx.channel.send(embed=embed)
            #Clears bot saved answers
            self.bot.pubquizAnswers = []
        else:
            #Outputs message to user that a question is currently active
            await ctx.channel.send(":no_entry: | There is already an active question!")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild is not None:
            if ctx.author == self.bot.user or str(ctx.author.id) == str(self.bot.pubquizQuestionUserID) or ctx.channel.id != self.bot.pubquizChannel or self.bot.pubquizActive == False:
                pass
            else:
                guild = 1
                try:
                    ctx.guild
                except:
                    guild = 0
                if guild == 1:
                    if self.bot.pubquizQuestionActive == True and ctx.content is not None:
                        toadd = []
                        toadd.append(ctx.author)
                        toadd.append(ctx.guild.id)
                        toadd.append(ctx.content)
                        self.bot.pubquizAnswers.append(toadd)
                        await ctx.delete()
                else:
                    pass
        else:
            if ctx.author == self.bot.user or self.bot.pubquizActive == False or str(ctx.author.id) == str(self.bot.pubquizQuestionUserID) or ctx.content == None:
                pass
            elif self.bot.pubquizQuestionActive == True:
                self.bot.pubquizAnswers.append([ctx.author, 331517548636143626, ctx.content])
                await ctx.add_reaction("\N{WHITE HEAVY CHECK MARK}")




def setup(bot):
    bot.add_cog(pubquizCog(bot))
