import discord, asyncio, sys, traceback, checks, inflect, useful, math, random
from discord.ext import commands
from operator import itemgetter

class pubquizCog:
    def __init__(self, bot):
        self.quizActive = False
        self.questionActive = False
        self.bot = bot
        self.questionTime = 10
        self.pubquizMembers = [["","",""]]
        self.lastQuestionSuper = False
        self.questionNumber = 0
        self.awaitingAnswer = []
        self.answers = []
        self.pubquizChannelID = 0
        self.currentColour = -1
        self.firstMember = True

    @commands.group(pass_context=True, aliases=["pq", "pubq"])
    async def pubquiz(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(":no_good: Please enter a valid command. ,pq help for a list of commands.")

    @pubquiz.command(name='join', aliases=['dm', 'stopdm', 'leave'])
    async def join(self, ctx):
        if self.quizActive:
            found = False
            for counter in range (0,len(self.pubquizMembers)):
                if self.pubquizMembers[counter][0] == ctx.message.author:
                    found = True
                    self.pubquizMembers[counter][2] = not self.pubquizMembers[counter][2]
                    if self.pubquizMembers[counter][2] == True:
                        await ctx.channel.send(":white_check_mark: " + ctx.message.author.mention + " I'll start DMing you questions!")
                        embed = discord.Embed(title="Questions will appear here.", description="Once they are sent you will have " + str(self.questionTime) + " seconds to answer. Please send answers to me in DM. Best of luck!", colour=self.getcolour())
                        embed.add_field(name="To return to the pubquiz chat click here.", value="<#" + str(self.pubquizChannelID) + ">" + " " + "<#" + str(self.pubquizChannelID) + ">" + " " + "<#" + str(self.pubquizChannelID) + ">" + " " + "<#" + str(self.pubquizChannelID) + ">")
                        await ctx.message.author.send(embed = embed)
                    else:
                        await ctx.channel.send(":white_check_mark: " + ctx.message.author.mention + " I'll stop DMing you questions!")
            if found == False:
                if self.firstMember == True:
                    self.firstMember = False
                    self.pubquizMembers.pop(0)
                toappend = [ctx.message.author, 0, False]
                self.pubquizMembers.append(toappend)
                await ctx.channel.send(":white_check_mark: " + ctx.message.author.mention + " successfully joined this weeks pub quiz!")
            await ctx.message.delete()
        else:
            await ctx.channel.send(":no_entry: There is not currently an ongoing pub quiz!")

    @pubquiz.command(name='start', aliases=['begin', 'go'])
    @checks.has_role("Quizmaster")
    async def start(self, ctx):
        if self.quizActive:
            await ctx.channel.send(":no_entry: A quiz is already active!")
        else:
            self.quizActive = True
            self.pubquizChannelID = ctx.channel.id
            await ctx.channel.send(discord.utils.get(ctx.guild.roles, name="Pub Quiz").mention +" This weeks Pub Quiz is starting now! Type `,pubquiz join` in #bot to join! You can also make me DM you questions with `,pubquiz dm`")

    @pubquiz.command()
    async def test(self, ctx):
        print(self.pubquizMembers)

    @pubquiz.command(name='stop', aliases =['end', 'halt'])
    @checks.has_role("Quizmaster")
    async def stop(self, ctx):
        if self.quizActive:
            await ctx.channel.send("That was the pub quiz! I hope you enjoyed. :)")
            resultsEmbed = discord.Embed(title="Final Leaderboard:", colour=self.getcolour())
            self.pubquizMembers.sort(key=lambda x: x[1])
            self.pubquizMembers.reverse()
            for counter in range (0,len(self.pubquizMembers)):
                resultsEmbed.add_field(name=(self.pubquizMembers[counter][0].display_name+" ("+self.pubquizMembers[counter][0].name+"#"+self.pubquizMembers[counter][0].discriminator)+")", value = "gained a total of " + str(self.pubquizMembers[counter][1]) + " points, placing them " + inflect.engine().ordinal(counter+1)+".")
            await ctx.channel.send(embed = resultsEmbed)
            self.pubquizMembers = [["","",""]]
            self.quizActive = False
            self.questionNumber = 0
            self.firstMember = True
            self.pubquizChannelID = 0
        else:
            await ctx.channel.send(":no_entry: There is not currently an ongoing pub quiz!")

    @pubquiz.command(name='settime', aliases=['time'])
    @checks.has_role("Quizmaster")
    async def settime(self, ctx, time):
        self.questionTime = int(time)
        await ctx.channel.send(":clock8: Default time set to " + str(self.questionTime) + " seconds.")

    @pubquiz.command(name='setquizmaster', aliases=['sqm', 'quizmaster', 'setqm'])
    @checks.has_role("Admin")
    async def setquizmaster(self, ctx, member):
        memberid = useful.getid(member)
        if discord.utils.get(ctx.guild.roles, name= "Quizmaster") in ctx.guild.get_member(memberid).roles:
            await ctx.guild.get_member(memberid).remove_roles(discord.utils.get(ctx.guild.roles, name="Quizmaster"))
            await ctx.channel.send(":white_check_mark: Removed Quizmaster from " + ctx.guild.get_member(memberid).mention + ".")
        else:
            await ctx.guild.get_member(memberid).add_roles(discord.utils.get(ctx.guild.roles, name="Quizmaster"))
            await ctx.channel.send(":white_check_mark: Granted " + ctx.guild.get_member(memberid).mention + " the Quizmaster role.")


    @pubquiz.command()
    @checks.has_role("Quizmaster")
    async def correct(self, ctx, *, correctMembers):
        if self.lastQuestionSuper and len(correctMembers) == 1:
            correctEmbed = discord.Embed(title="The following user was closest:", colour=self.getcolour())
        elif self.lastQuestionSuper:
            correctEmbed = discord.Embed(title="The following users were joint closest:", colour=self.getcolour())
        elif self.lastQuestionSuper == False and len(correctMembers) == 1:
            correctEmbed = discord.Embed(title="The following user was correct:", colour=self.getcolour())
        else:
            correctEmbed = discord.Embed(title="The following users were correct:", colour=self.getcolour())

        correctMembers = correctMembers.split(" ")
        while not all(isinstance(item, int) for item in correctMembers):
            toPop = []
            for counter in range (0,len(correctMembers)):
                if correctMembers[counter] == '':
                    toPop.append(counter-len(toPop))
                correctMembers[counter] = "".join(each for each in correctMembers[counter] if each.isdigit())
            if toPop == []:
                break
            print(toPop, len(toPop), len(correctMembers), correctMembers)
            for each in toPop:
                correctMembers.pop(toPop[each])
        for j in range (0,len(correctMembers)):
            if self.lastQuestionSuper:
                toAdd = int(math.ceil(25/len(correctMembers)))
            elif self.lastQuestionSuper == False and len(correctMembers) == 1:
                toAdd = 16
            else:
                toAdd = 13 - j
                if toAdd < 10:
                    toAdd = 10
            for i in range (0,len(self.pubquizMembers)):
                if self.pubquizMembers[i][0] == ctx.guild.get_member(int(correctMembers[j])):
                    self.pubquizMembers[i][1] = self.pubquizMembers[i][1] + toAdd
                    correctEmbed.add_field(name=(self.pubquizMembers[i][0].display_name+" ("+self.pubquizMembers[i][0].name+"#"+self.pubquizMembers[i][0].discriminator)+")  ", value="gained " + str(toAdd) + " points.")
        await ctx.channel.send(embed = correctEmbed)
        print(self.pubquizMembers)

    @pubquiz.command(name='question', aliases=['q'])
    @checks.has_role("Quizmaster")
    async def question(self, ctx, *, question):
        if self.questionActive == False and self.quizActive:
            self.lastQuestionSuper = False
            self.answers = []
            self.questionActive = True
            self.questionNumber = self.questionNumber + 1
            questionEmbed = discord.Embed(title="**Question " + str(self.questionNumber) + "!**", description=question, colour=self.getcolour())
            questionEmbed.add_field(name="Please type your answers now.", value =(self.bot.user.mention + " " +self.bot.user.mention + " " + self.bot.user.mention + " " +self.bot.user.mention))
            await ctx.channel.send(embed = questionEmbed)

            questionEmbedDM = discord.Embed(title="**Question " + str(self.questionNumber) + "!**", description=question, colour=self.getcolour())
            questionEmbedDM.add_field(name="To return to the pubquiz chat click here.", value = "<#"+str(ctx.channel.id)+">" + " " + "<#"+str(ctx.channel.id)+">" + " " +"<#"+str(ctx.channel.id)+">" + " " +"<#"+str(ctx.channel.id)+">")
            for i in range(0,len(self.pubquizMembers)):
                if self.pubquizMembers[i][2] == True:
                    await self.pubquizMembers[i][0].send(embed = questionEmbedDM)
                self.awaitingAnswer.append(self.pubquizMembers[i][0])
            await asyncio.sleep(self.questionTime)
            await ctx.channel.send("Answers are now closed!")
            answerEmbed = discord.Embed(title="Answers:", colour =self.getcolour())
            for counter in range (0, len(self.answers)):
                print(self.answers[counter])
                answerEmbed.add_field(name=self.answers[counter][0], value =self.answers[counter][1])
            await ctx.channel.send(embed = answerEmbed)
            self.questionActive = False
        elif self.quizActive == False:
            await ctx.channel.send(":no_entry: There is not a currently active pub quiz!")
        else:
            await ctx.channel.send(":no_entry: There is already an active question!")

    @pubquiz.command(name='superquestion', aliases=['sq', 'spq'])
    @checks.has_role("Quizmaster")
    async def superquestion(self, ctx, *, question):
        if self.questionActive == False and self.quizActive:
            self.lastQuestionSuper = True
            self.answers = []
            self.questionActive = True
            self.questionNumber = self.questionNumber + 1
            questionEmbed = discord.Embed(title="**SUPER QUESTION " + str(self.questionNumber) + "!**", description=question, colour=self.getcolour())
            questionEmbed.add_field(name="Please type your answers now.", value=(self.bot.user.mention + " " + self.bot.user.mention + " " + self.bot.user.mention + " " + self.bot.user.mention))
            await ctx.channel.send(embed=questionEmbed)
            questionEmbedDM = discord.Embed(title="**SUPER QUESTION " + str(self.questionNumber) + "!**", description=question, colour=self.getcolour())
            questionEmbedDM.add_field(name="To return to the pubquiz chat click here.", value="<#" + str(ctx.channel.id) + ">" + " " + "<#" + str(ctx.channel.id) + ">" + " " + "<#" + str(ctx.channel.id) + ">" + " " + "<#" + str(ctx.channel.id) + ">")
            for i in range(0,len(self.pubquizMembers)):
                if self.pubquizMembers[i][2] == True:
                    await self.pubquizMembers[i][0].send(embed = questionEmbedDM)
                self.awaitingAnswer.append(self.pubquizMembers[i][0])
            await asyncio.sleep(self.questionTime)
            await ctx.channel.send("Answers are now closed!")
            answerEmbed = discord.Embed(title="Answers:", colour=self.getcolour())
            for counter in range (0, len(self.answers)):
                print(self.answers[counter])
                answerEmbed.add_field(name=self.answers[counter][0], value =self.answers[counter][1])
            await ctx.channel.send(embed = answerEmbed)
            self.questionActive = False
        elif self.quizActive == False:
            await ctx.channel.send(":no_entry: There is not a currently active pub quiz!")
        else:
            await ctx.channel.send(":no_entry: There is already an active question!")

    @pubquiz.command(name='override', aliases=['or', 'over'])
    @checks.has_role("Quizmaster")
    async def override(self, ctx, member, value):
        memberid = int("".join(each for each in member if each.isdigit()))
        for counter in range(0,len(self.pubquizMembers)):
            if self.pubquizMembers[counter][0] == ctx.guild.get_member(memberid):
                self.pubquizMembers[counter][1] = self.pubquizMembers[counter][1] + int(value)
                await ctx.channel.send(":white_check_mark: Done!")

    async def on_message(self, ctx):
        if not self.questionActive:
            pass
        #elif (ctx.author in self.awaitingAnswer and ctx.guild is None) or (ctx.author in self.awaitingAnswer and ctx.channel.id == self.pubquizChannelID and (discord.utils.get(ctx.guild.roles, name="Quizmaster") in ctx.author.roles == False)):
        elif ctx.author in self.awaitingAnswer and (ctx.guild is None or ctx.channel.id == self.pubquizChannelID):
            toAppend = [ctx.author.display_name+" ("+ctx.author.name+"#"+ctx.author.discriminator+") answered:", ctx.content]
            self.answers.append(toAppend)
            if ctx.guild:
                await ctx.delete()

    async def on_reaction_remove(self, reaction, user):
        print(reaction.emoji)
        print(user.id)
        ann = guild.get_channel(348748987354054656)
        print(ann)
        msg = await ann.fetch_message(573609869454737429)
        print(msg.content)
        if user.id == 455137631718735872 or user.id == 163691476788838401 or user.id == 447089705691906048:
            msg.add_reaction(reaction.emoji)


    @pubquiz.command()
    async def help(self, ctx):
        embed = discord.Embed(title="PubQuiz Help", description="Help for the following pubquiz commands:", colour=self.getcolour())
        embed.add_field(name=",pubquiz qmhelp", value ="Help Menu for the Quizmaster!")
        embed.add_field(name=",pubquiz join", value ="Joins this weeks pub quiz. Can only be used when the pub quiz is active.")
        embed.add_field(name=",pubquiz dm/stopdm", value ="Toggles the use of DM's to send questions. ,pubquiz join will also do this after you have joined.")
        await ctx.channel.send(embed = embed)

    @pubquiz.command()
    @checks.has_role("Quizmaster")
    async def qmhelp(self, ctx):
        embed = discord.Embed(title="PubQuiz Quizmaster Help", description="Help for the following pubquiz commands:", colour=self.getcolour())
        embed.add_field(name=",pubquiz start", value ="Starts the weeks Pub Quiz! Can only be used by the QuizMaster")
        embed.add_field(name=",pubquiz stop", value ="End the weeks Pub Quiz! Can only be used by the QuizMaster")
        embed.add_field(name=",pubquiz question", value ="Sends a new question to everyone! Default time is 10. Can only be used by the QuizMaster")
        embed.add_field(name=",pubquiz superquestion", value ="Sends a new super question to everyone! Default time is 10. Can only be used by the QuizMaster.")
        embed.add_field(name=",pubquiz override", value ="Overrides a users current points, useful if mistakes are made. Can only be used by the QuizMaster")
        embed.add_field(name=",pubquiz settime", value ="Changes the default time in seconds people have to answer questions. Can only be used by the QuizMaster")
        embed.add_field(name=",pubquiz correct", value ="Updates the points gained values for these users. Fastest user should be entered first with slowest user last. Can only be used by the QuizMaster.")
        await ctx.channel.send(embed = embed)


    @pubquiz.command(name="aliases", aliases=['alias'])
    async def aliases(self, ctx):
        embed = discord.Embed(title="PubQuiz Aliases", description="Aliases for the following pubquiz commands:", colour=self.getcolour())
        embed.add_field(name=",pubquiz ", value ="pubquiz, pq, pubq")
        embed.add_field(name=",pubquiz start", value ="start, go, begin")
        embed.add_field(name=",pubquiz stop", value ="stop, end, halt")
        embed.add_field(name=",pubquiz question", value ="question, q")
        embed.add_field(name=",pubquiz superquestion", value ="superquestion, sq")
        embed.add_field(name=",pubquiz override", value ="override, or, over")
        embed.add_field(name=",pubquiz settime", value ="settime, time")
        embed.add_field(name=",pubquiz correct", value ="No aliases")
        embed.add_field(name=",pubquiz join/leave", value ="join, dm, stopdm, leave")
        await ctx.channel.send(embed = embed)

    @pubquiz.command(name="leaderboard", alias=['top','leaderboards'])
    @checks.has_role("Quizmaster")
    async def leaderboard(self, ctx):
        resultsEmbed = discord.Embed(title="Current leaderboards:", colour=self.getcolour())
        self.pubquizMembers.sort(key=lambda x: x[1])
        self.pubquizMembers.reverse()
        for counter in range(0, len(self.pubquizMembers)):
            resultsEmbed.add_field(name=(self.pubquizMembers[counter][0].display_name + " (" + self.pubquizMembers[counter][0].name + "#" + self.pubquizMembers[counter][0].discriminator) + ")", value="currently has a total of " + str(self.pubquizMembers[counter][1]) + " points, placing them " + inflect.engine().ordinal(counter + 1) + ".")
        await ctx.channel.send(embed=resultsEmbed)

    def getcolour(self):
        colours = ["5C6BC0", "AB47BC", "EF5350", "FFA726", "FFEE58", "66BB6A"]
        self.currentColour = self.currentColour + 1
        if self.currentColour == 5:
            self.currentColour = 0
        return discord.Colour(int(colours[self.currentColour], 16))



def setup(bot):
    bot.add_cog(pubquizCog(bot))
