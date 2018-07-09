import discord, asyncio, sys, traceback, checks
from discord.ext import commands

class pubquizCog:
    def __init__(self, bot):
        self.quizActive = False
        self.questionActive = False
        self.bot = bot
        self.questionTime = 10
        self.pubquizMembers = [["","",""]]
        self.lastQuestionSuper = False


    @commands.group(pass_context=True)
    async def pubquiz(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("Please enter a command. !help or !pubquiz help for a list of commands.")

    @pubquiz.command(name='join', aliases=['quit', 'leave'])
    async def join(self, ctx):
        if self.quizActive:
            found = False
            for counter in range (0,len(self.pubquizMembers)):
                if self.pubquizMembers[counter][0] == ctx.message.author:
                    found = True
                    self.pubquizMembers[counter][2] = not self.pubquizMembers[counter][2]
                    if self.pubquizMembers[counter][2] == True:
                        await ctx.channel.send(ctx.message.author.mention + " successfully joined this weeks pub quiz!")
                    else:
                        await ctx.channel.send(ctx.message.author.mention + " successfully left this weeks pub quiz!")

            if found == False:
                toappend = [ctx.message.author, 0, True]
                self.pubquizMembers.append(toappend)
                await ctx.message.author.send("Questions will appear here. Once they are sent you will have " + str(self.questionTime) + " seconds to answer. Please send answers to me in DM and only the last sent message will be counted. Best of luck!")
                await ctx.channel.send(ctx.message.author.mention + " successfully joined this weeks pub quiz!")

            ctx.message.delete()
        else:
            await ctx.channel.send("There is not currently an ongoing pub quiz!")

    @pubquiz.command(name='start', aliases=['begin', 'go'])
    @checks.has_role("Quizmaster")
    async def start(self, ctx):
        if self.quizActive:
            await ctx.channel.send("A quiz is already active!")
        else:
            self.quizActive = True
            await ctx.channel.send("@Pubquiz This weeks Pub Quiz is starting now! Type `!pubquiz join` in #bot to join! You can also leave at any time with `!pubquiz leave`")

    @pubquiz.command()
    async def test(self, ctx):
        print(self.pubquizMembers)

    @pubquiz.command(name='stop', aliases =['end', 'halt'])
    @checks.has_role("Quizmaster")
    async def stop(self, ctx):
        if self.quizActive:
            self.pubquizMembers = [["","",""]]
            self.quizActive = False
            await ctx.channel.send("That was the pub quiz! I hope you enjoyed. :) (I could probably also post results here but thats ghosts thing :3)")
        else:
            await ctx.channel.send("There is not currently a pub quiz!")

    @pubquiz.command()
    @checks.has_role("Quizmaster")
    async def settime(self, ctx, time):
        if time.is_integer():
            self.questionTime = time
            await ctx.channel.send("Default time set to " + self.questionTime + " seconds.")

    @pubquiz.command()
    @checks.has_role("Quizmaster")
    async def correct(self, ctx, *, correctMembers):
        loops = 0
        correctMembers = correctMembers.split(" ")
        while not all(isinstance(item, int) for item in correctMembers):
            toPop = []
            for counter in range (0,len(correctMembers)):
                if correctMembers[counter] == '':
                    toPop.append(counter-len(toPop))
                correctMembers[counter] = "".join(each for each in correctMembers[counter] if each.isdigit())
            if toPop == []:
                break
            for each in toPop:
                correctMembers.pop(toPop[each])
        print(correctMembers)
        for j in range (0,len(correctMembers)):
            if self.lastQuestionSuper:
                toAdd = round(25/len(correctMembers), 0)
            else:
                toAdd = 14 - j
                if toAdd < 10:
                    toAdd = 10
            for i in range (0,len(self.pubquizMembers)):
                if self.pubquizMembers[i][0] == ctx.guild.get_member(int(correctMembers[j])):
                    self.pubquizMembers[i][1] = self.pubquizMembers[i][1] + toAdd
        print(self.pubquizMembers)

    @pubquiz.command()
    async def question(self, ctx, *, question):
        self.lastQuestionSuper = False
        questionEmbed = discord.Embed(title="**SUPER QUESTION**", description="Whoever gets the closest gets 25 points")

    @pubquiz.command()
    async def help(self, ctx):
        embed = discord.Embed(title="PubQuiz Help", description="Help for the following !pubquiz commands:", colour=0xDEADBF)
        embed.add_field(name="!pubquiz start", value ="Starts the weeks Pub Quiz! Can only be used by the QuizMaster")
        embed.add_field(name="!pubquiz stop", value ="End the weeks Pub Quiz! Can only be used by the QuizMaster")
        embed.add_field(name="!pubquiz question", value ="Sends a new question to everyone! Default time is 10. Can only be used by the QuizMaster")
        embed.add_field(name="!pubquiz settime", value ="Changes the default time in seconds people have to answer questions. Can only be used by the QuizMaster")
        embed.add_field(name="!pubquiz correct", value ="Updates the points gained values for these users. Fastest user should be entered first with slowest user last. Can only be used by the QuizMaster.")
        embed.add_field(name="!pubquiz join/leave", value ="Joins or leaves this weeks pub quiz. Can only be used during a pub quiz.")
        await ctx.channel.send(embed = embed)

def setup(bot):
    bot.add_cog(pubquizCog(bot))
