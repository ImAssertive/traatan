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
        await ctx.channel.send(":white_check_mark: | Online status set to: ** playing "+ gameName+"**")

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

    @commands.command(name="setfarewell", aliases=['setleave', 'setleavechannel', 'setfarewellchannel'])
    @checks.justme()
    async def setfarewell(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET leavechannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done! Farewell channel set here.")

    @commands.command(name="setwelcome", aliases=['setwelcomechannel'])
    @checks.justme()
    async def setwelcome(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET welcomechannel = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done! Welcome channel set here.")

    @commands.command()
    @checks.justme()
    async def setwelcometext(self, ctx, *, welcometext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET welcometext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, welcometext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Welcome text set to ```" + welcometext + "```")

    @commands.command(name="setfarewelltext", aliases =['setleavetext'])
    @checks.justme()
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


    @commands.command(name='setbantext')
    @commands.has_permissions(ban_members=True)
    async def setbantext(self, ctx, *, banText):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET bantext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, banText,ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Ban text set to `"+banText+"`!")

    @commands.command(name='setkicktext')
    @commands.has_permissions(ban_members=True)
    async def setkicktext(self, ctx, *, kickText):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET kicktext = $1 WHERE guildID = $2"
            await self.bot.db.execute(query, kickText,ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Kick text set to `"+kickText+"`!")

    @commands.command()
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



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, memberid):
        try:
            await ctx.guild.ban(discord.Object(id=int(memberid)))
            await ctx.channel.send(":white_check_mark: | Banned ID `"+str(memberid)+"`")
        except:
            await ctx.channel.send(":no_entry: | An error occurred. Was that a valid user ID?")

def setup(bot):
    bot.add_cog(adminCog(bot))