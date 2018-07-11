import discord, asyncio, sys, traceback, checks, random, useful, inflect
from discord.ext import commands

class pubquizCog:
    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True, name='pubquiz', aliases=['pq','pubq'])
    async def pubquiz(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("Please enter a command. !help or !pubquiz help for a list of commands.")

    @pubquiz.command(name='settext', aliases=['stext'])
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqsettext")
    async def settext(self, ctx, *, pubquiztext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET pubquiztext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, pubquiztext,ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Pub quiz text set to `"+pubquiztext+"`!")

    @pubquiz.command(name='setendtext', aliases=['sendtext'])
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqsettext")
    async def setendtext(self, ctx, *, pubquizendtext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET pubquizendtext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, pubquizendtext,ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Pub quiz end text set to `"+pubquizendtext+"`!")


    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.owner_or_admin()
    async def resetguildscoreboard(self, ctx):
        confirmationnumber = random.randint(1000,9999)
        query = "SELECT * FROM guilds WHERE guildID = $1 AND ongoingpubquiz = true"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            await ctx.channel.send(":no_entry: | A pub quiz is already active! Please end the current pub quiz to continue.")
        else:
            await ctx.channel.send(":clock1: | Are you sure? This will completely reset the pub quiz scores for the entire guild. To continue please type `"+ str(confirmationnumber) +"`")
            def confirmationcheck(msg):
                return msg.content == str(confirmationnumber) and ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id
            try:
                msg = await self.bot.wait_for('message', check=confirmationcheck, timeout=60.0)
            except asyncio.TimeoutError:
                try:
                    await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The reset command has closed due to inactivity.")
                except TypeError:
                    await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The reset command has closed due to inactivity.")
            else:
                if msg.content == str(confirmationnumber):
                    connection = await self.bot.db.acquire()
                    async with connection.transaction():
                        query = "UPDATE GuildUsers SET pubquizscoretotal = 0 WHERE guildID = $1"
                        await self.bot.db.execute(query, ctx.guild.id)
                    await self.bot.db.release(connection)
                    await ctx.channel.send(":white_check_mark: | Pub quiz scores reset!")

    @pubquiz.command(name='start', aliases=['begin', 'go'])
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqstart")
    @checks.pubquiz_not_active()
    async def start(self, ctx):
        query = "SELECT * FROM guilds WHERE guildID = $1 AND ongoingpubquiz = true"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            await ctx.channel.send(":no_entry: | A quiz is already active!")
        else:
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE Guilds SET ongoingpubquiz = true WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
                query = "UPDATE Guilds SET pubquizchannel = $1 WHERE guildID = $2"
                await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
                query = "UPDATE GuildUsers SET pubquizscoreweekly = 0 WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
                query = "UPDATE Guilds SET pubquizquestionnumber = 0 WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
            await self.bot.db.release(connection)
            query = "SELECT * FROM guilds WHERE guildID = $1 AND pubquiztext IS NOT NULL"
            results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            if results:
                pubquiztext = ("{}".format(results["pubquiztext"]))
                await ctx.channel.send(pubquiztext)
            else:
                await ctx.channel.send("Pub quiz started!")

    @pubquiz.command(name='stop', aliases =['end', 'halt'])
    @checks.pubquiz_active()
    async def stop(self, ctx):
        query = "SELECT * FROM guilds WHERE guildID = $1 AND pubquizendtext IS NOT NULL"
        results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if results:
            pubquizendtext = ("{}".format(results["pubquizendtext"]))
            await ctx.channel.send(pubquizendtext)
        else:
            await ctx.channel.send("That was the pub quiz! I hope you enjoyed. :)")
        embed = await self.leaderboardFunction(ctx)
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        await ctx.guild.get_channel(int(result["pubquizchannel"])).send(embed=embed)
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET ongoingpubquiz = false WHERE guildID = $1"
            await self.bot.db.execute(query, ctx.guild.id)
        await self.bot.db.release(connection)

    async def leaderboardFunction(self, ctx):
        query = "SELECT * FROM guildusers WHERE guildID = $1 AND pubquizscoreweekly != 0 ORDER BY pubquizscoreweekly DESC"
        result = await ctx.bot.db.fetch(query, ctx.guild.id)
        print(result)
        resultsEmbed = discord.Embed(title= ctx.guild.name + " Pub Quiz Leaderboard:", colour=self.bot.getcolour())
        for row in range (0,len(result)):
            resultsEmbed.add_field(name=ctx.guild.get_member(int(result[row]["userid"])).display_name + " (" +ctx.guild.get_member(int(result[row]["userid"])).name +"#" +ctx.guild.get_member(int(result[row]["userid"])).discriminator + ")", value="has a total of **" + str(result[row]["pubquizscoreweekly"]) + "** points. Placing them **"+ inflect.engine().ordinal(row + 1) + "**. ("+str(result[row]["pubquizscoretotal"])+" total points)", inline=False)
        return resultsEmbed

    async def totalleaderboardFunction(self, ctx):
        query = "SELECT * FROM guildusers WHERE guildID = $1 AND pubquizscoretotal != 0 ORDER BY pubquizscoreweekly DESC"
        result = await ctx.bot.db.fetch(query, ctx.guild.id)
        resultsEmbed = discord.Embed(title=ctx.guild.name + " Pub Quiz Leaderboard:", colour=self.bot.getcolour())
        for row in range(0, len(result)):
            resultsEmbed.add_field(name=ctx.guild.get_member(int(result[row]["userid"])).display_name + " (" + ctx.guild.get_member(int(result[row]["userid"])).name + "#" + ctx.guild.get_member(int(result[row]["userid"])).discriminator + ")", value="has a total of **" + str(result[row]["pubquizscoretotal"]) + "** points. Placing them **" + inflect.engine().ordinal(row + 1) + "**.", inline=False)
        return resultsEmbed

    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    async def totalleaderboard(self, ctx):
        embed = await self.totalleaderboardFunction(ctx)
        if checks.rolescheck_not_check(ctx, "pqleaderboard"):
            await ctx.channel.send(embed=embed)
        else:
            await ctx.author.send(embed=embed)

    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.pubquiz_active()
    async def leaderboard(self, ctx):
        embed = await self.leaderboardFunction(ctx)
        if checks.rolescheck_not_check(ctx, "pqleaderboard"):
            query = "SELECT * FROM guilds WHERE guildID = $1"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            await ctx.guild.get_channel(int(result["pubquizchannel"])).send(embed=embed)
        else:
            await ctx.author.send(embed=embed)

    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqoverride")
    async def override(self, ctx, member, value):
        successful = 1
        try:
            value = int(value)
        except:
            await ctx.channel.send("Please enter a whole number to add or subtract from the users score.")
            successful = 0
        if successful == 1 and value != 0:
            memberid = useful.getid(member)
            query = "SELECT * FROM guildusers WHERE guildID = $1 AND userID = $2"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id, memberid)
            currentvalue = result["pubquizscoreweekly"]
            currenttotal = result["pubquizscoretotal"]
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE guildusers SET pubquizscoreweekly = $1 WHERE guildID = $2 AND userID = $3"
                await self.bot.db.execute(query, currentvalue + value, ctx.guild.id, memberid)
                query = "UPDATE guildusers SET pubquizscoretotal = $1 WHERE guildID = $2 AND userID = $3"
                await self.bot.db.execute(query, currenttotal + value, ctx.guild.id, memberid)
            await self.bot.db.release(connection)
            if value > 0:
                await ctx.channel.send(":white_check_mark: | User **"+ctx.guild.get_member(memberid).display_name + " (" +ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator +")** has had their weekly and total score increased by **" + str(value) + "**. Their new total is **"+str(currenttotal + value)+"** overall and **"+ str(currentvalue + value)+"** this week.")
            elif value < 0:
                await ctx.channel.send(":white_check_mark: | User **"+ctx.guild.get_member(memberid).display_name + " (" +ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator +")** has had their weekly and total score reduced by **" + str(value*-1) + "**. Their new total is **"+str(currenttotal + value)+"** overall and **"+ str(currentvalue + value)+"** this week.")
        elif value == 0:
            await ctx.channel.send(":no_entry: | The score can not be modified by 0.")

    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqsettime")
    async def settime(self, ctx, time):
        success = 1
        try:
            time = int(time)
        except:
            success = 0
        if success == 1:
            if time > 0 and time < 61:
                connection = await self.bot.db.acquire()
                async with connection.transaction():
                    query = "UPDATE Guilds SET pubquiztime = $1 WHERE guildID = $2"
                    await self.bot.db.execute(query, time, ctx.guild.id)
                await self.bot.db.release(connection)
                await ctx.channel.send(":white_check_mark: | Default time set to **" + str(time) + "** seconds.")
            else:
                await ctx.channel.send(":no_entry: | Time must be between 1 and 60 seconds.")
        else:
            await ctx.channel.send(":no_entry: | Please enter a positive whole time number.")



    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqcorrect")
    async def correct(self, ctx, *, correctMembers):
        correctMembers = correctMembers.split(" ")
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        embed = discord.Embed(title="The following users were correct:")
        connection = await self.bot.db.acquire()
        for i in range (0, len(correctMembers)):
            memberid = (useful.getid(correctMembers[i]))
            if result["pubquizlastquestionsuper"] == True:
                toAdd = round(25/len(correctMembers))
            elif len(correctMembers) == 1 and result["pubquizlastquestionsuper"] == False:
                toAdd = 16
            else:
                toAdd = 14-i
                if toAdd < 10:
                    toAdd = 10
            query = "SELECT * FROM guildusers WHERE guildID = $1 AND userID = $2"
            results = await ctx.bot.db.fetchrow(query, ctx.guild.id, memberid)
            currentvalue = results["pubquizscoreweekly"]
            currenttotal = results["pubquizscoretotal"]
            async with connection.transaction():
                query = "UPDATE guildusers SET pubquizscoreweekly = $1 WHERE guildID = $2 AND userID = $3"
                await self.bot.db.execute(query, currentvalue + toAdd, ctx.guild.id, memberid)
                query = "UPDATE guildusers SET pubquizscoretotal = $1 WHERE guildID = $2 AND userID = $3"
                await self.bot.db.execute(query, currenttotal + toAdd, ctx.guild.id, memberid)
            embed.add_field(name=ctx.guild.get_member(memberid).display_name + " (" +ctx.guild.get_member(memberid).name +"#" +ctx.guild.get_member(memberid).discriminator+")", inline=False, value="gained **"+ str(toAdd) + "** points.")
        await self.bot.db.release(connection)
        await ctx.guild.get_channel(int(result["pubquizchannel"])).send(embed=embed)


    @pubquiz.command()
    async def help(self, ctx):
        embed = discord.Embed(title="PubQuiz Help", description="Help for the following !pubquiz commands:", colour=self.bot.getcolour())
        embed.add_field(name="!pubquiz start", value ="Starts the weeks Pub Quiz! Can only be used by the QuizMaster")
        embed.add_field(name="!pubquiz stop", value ="End the weeks Pub Quiz! Can only be used by the QuizMaster")
        embed.add_field(name="!pubquiz question", value ="Sends a new question to everyone! Default time is 10. Can only be used by the QuizMaster")
        embed.add_field(name="!pubquiz settime", value ="Changes the default time in seconds people have to answer questions. Can only be used by the QuizMaster")
        embed.add_field(name="!pubquiz correct", value ="Updates the points gained values for these users. Fastest user should be entered first with slowest user last. Can only be used by the QuizMaster.")
        embed.add_field(name="!pubquiz join/leave", value ="Joins or leaves this weeks pub quiz. Can only be used during a pub quiz.")
        await ctx.channel.send(embed = embed)

    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqquestion")
    @checks.pubquiz_active()
    async def question(self, ctx, *, question):
        superQuestion = False
        await self.questionFunction(ctx, question, superQuestion)

    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqsuperquestion")
    @checks.pubquiz_active()
    async def superquestion(self, ctx, *, question):
        superQuestion = True
        await self.questionFunction(ctx, question, superQuestion)

    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqanswer")
    @checks.module_enabled("pubquiz")
    @checks.pubquiz_active()
    async def answer(self, ctx, *, answer):
        embed = discord.Embed(title="The answer was...", description = answer, colour=self.bot.getcolour())
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        await ctx.guild.get_channel(int(result["pubquizchannel"])).send(embed=embed)

    async def questionFunction(self, ctx, question, superQuestion):
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result["pubquizquestionactive"] == False:
            currentquestion = result["pubquizquestionnumber"]
            currentquestion += 1
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE Guilds SET pubquizquestionnumber = $1 WHERE guildID = $2"
                await self.bot.db.execute(query, currentquestion, ctx.guild.id)
                query = "UPDATE Guilds SET pubquizquestionactive = true WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
                query = "UPDATE Guilds SET pubquizquestionuserid = $1 WHERE guildID = $2"
                await self.bot.db.execute(query, ctx.author.id, ctx.guild.id)
            if superQuestion:
                questionEmbed = discord.Embed(title="**SUPER QUESTION " + str(currentquestion) + "!**", description=question, colour=self.bot.getcolour())
                questionEmbed.add_field(name="Please type your answers now.", value=(self.bot.user.mention + " " + self.bot.user.mention + " " + self.bot.user.mention + " " + self.bot.user.mention))
                async with connection.transaction():
                    query = "UPDATE Guilds SET pubquizlastquestionsuper = true WHERE guildID = $1"
                    await self.bot.db.execute(query, ctx.guild.id)
            else:
                questionEmbed = discord.Embed(title="**Question " + str(currentquestion) + "!**", description=question, colour=self.bot.getcolour())
                questionEmbed.add_field(name="Please type your answers now.", value =(self.bot.user.mention + " " +self.bot.user.mention + " " + self.bot.user.mention + " " +self.bot.user.mention))
                async with connection.transaction():
                    query = "UPDATE Guilds SET pubquizlastquestionsuper = false WHERE guildID = $1"
                    await self.bot.db.execute(query, ctx.guild.id)
            await self.bot.db.release(connection)
            await ctx.guild.get_channel(int(result["pubquizchannel"])).send(embed=questionEmbed)
            await asyncio.sleep(result["pubquiztime"])
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE Guilds SET pubquizquestionactive = false WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
            await self.bot.db.release(connection)
            await ctx.guild.get_channel(int(result["pubquizchannel"])).send("Answers are now closed!")
            answerEmbed = discord.Embed(title="Answers:", colour=self.bot.getcolour())
            for answer in range(0,len(self.bot.pubquizAnswers)):
                if self.bot.pubquizAnswers[answer][1] == ctx.guild.id:
                    answerEmbed.add_field(name=self.bot.pubquizAnswers[answer][0].display_name+" (" +self.bot.pubquizAnswers[answer][0].name+"#"+self.bot.pubquizAnswers[answer][0].discriminator+") answered:", value=self.bot.pubquizAnswers[answer][0][2])
                    self.bot.pubquizAnswers.remove(answer)
                    ##ctx.author.display_name + " (" + ctx.author.name + "#" + ctx.author.discriminator + ") answered:", ctx.content
            await ctx.guild.get_channel(int(result["pubquizchannel"])).send(embed=answerEmbed)
        else:
            await ctx.channel.send(":no_entry: | There is already an active question!")


    # @pubquiz.command()
    # @checks.module_enabled("pubquiz")
    # async def dm(self, ctx):
    #     toadd = []
    #     toadd.append(ctx.author.id)
    #     toadd.append(ctx.guild.id)
    #     working = 0
    #     try:
    #         self.bot.pubquizDMList.index(toadd)
    #     except ValueError:
    #         working = 1
    #     if working == 1:
    #         self.bot.pubquizDMList.append(toadd)
    #         await ctx.channel.send(":white_check_mark: | Ill start DMing you questions!")
    #     else:
    #         await ctx.channel.send(":no_entry: | I am already DMing you questions!")
    #
    # @pubquiz.command()
    # @checks.module_enabled("pubquiz")
    # async def stopdm(self, ctx):
    #     toadd = []
    #     toadd.append(ctx.author.id)
    #     toadd.append(ctx.guild.id)
    #     working = 1
    #     try:
    #         self.bot.pubquizDMList.index(toadd)
    #     except ValueError:
    #         working = 0
    #     if working == 1:
    #         self.bot.pubquizDMList.remove(self.bot.pubquizDMList.index(toadd))
    #         await ctx.channel.send(":white_check_mark: | Ill stop DMing you questions!")
    #     else:
    #         await ctx.channel.send(":no_entry: | I am not currently DMing you questions!")

    async def on_message(self, ctx):
        query = "SELECT * FROM guilds WHERE guildID = $1"
        result = await self.bot.db.fetchrow(query, ctx.guild.id)
        if ctx.author == bot.user or str(ctx.author.id) == str(result["pubquizquestionuserid"]):
            pass
        else:
            guild = 1
            try:
                ctx.guild
            except:
                guild = 0
            if guild == 1:
                if result["pubquizquestionactive"] == True:
                    toadd = []
                    toadd.append(ctx.author)
                    toadd.append(ctx.guild.id)
                    toadd.append(ctx.content)
                    self.bot.pubquizAnswers.append(toadd)
                    await ctx.delete()
            else:
                pass

def setup(bot):
    bot.add_cog(pubquizCog(bot))
