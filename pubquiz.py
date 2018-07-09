import discord, asyncio, sys, traceback, checks
from discord.ext import commands

class pubquizCog:
    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True)
    async def pubquiz(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("Please enter a command. !help or !pubquiz help for a list of commands.")



    @pubquiz.command(name='start', aliases=['begin', 'go'])
    @checks.module_enabled("pubquiz")
    async def start(self, ctx):
        query = "SELECT * FROM guilds WHERE guildID = $1 AND ongoingpubquiz = true"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            await ctx.channel.send("A quiz is already active!")
        else:
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE Guilds SET ongoingpubquiz = true WHERE guildID = $1"
                await self.bot.db.execute(query, ctx.guild.id)
            await self.bot.db.release(connection)
            query = "SELECT * FROM guilds WHERE guildID = $1"
            results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            pubquiztext =("{}".format(result["pubquiztext"]))
            if pubquiztext:
                await ctx.guild.get_channel(int(channelID)).send(pubquiztext)
            else:
                await ctx.guild.get_channel(int(channelID)).send("A new pub quiz is starting soon!")

    @pubquiz.command()
    async def test(self, ctx):
        print(self.pubquizMembers)

    @pubquiz.command(name='stop', aliases =['end', 'halt'])
    async def stop(self, ctx):
        query = "SELECT * FROM guilds WHERE guildID = $1 AND ongoingpubquiz = false"
        result = await ctx.bot.db.fetchrow(query, ctx.author.id)
        if result:
            await ctx.channel.send("A quiz is already active!")
        else:
            print("carry on here")

    @pubquiz.command()
    @checks.module_enabled("pubquiz")
    @checks.rolescheck("pqsettime")
    async def settime(self, ctx, time):
        if time.is_integer() and time > 0 and time < 60:
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE Guilds SET pubquiztime = $1 WHERE guildID = $2"
                await self.bot.db.execute(query, time, ctx.guild.id)
            await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Default time set to **" + time + "** seconds.")



    @pubquiz.command()
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
        questionEmbed = discord.Embed(title="**SUPER QUESTION**", description="This question is worth 25 points.")

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
