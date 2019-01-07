import discord, asyncio, sys, traceback, checks, useful, asyncpg, random, ast
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

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, toSay):
        print(toSay)
        await ctx.guild.get_channel(528673771062689812).send(toSay)

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

    def insert_returns(body):
        # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].body)
            insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)

    @commands.command()
    @checks.justme()
    async def eval(ctx, *, cmd):
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

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
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, *, reason = None):
        kickban = "ban"
        await self.bankickFunction(ctx, member, kickban, reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, memberid):
        try:
            await ctx.guild.ban(discord.Object(id=int(memberid)))
            await ctx.channel.send(":white_check_mark: | Banned ID `"+str(memberid)+"`")
        except:
            await ctx.channel.send(":no_entry: | An error occurred. Was that a valid user ID?")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, *, reason = None):
        kickban = "kick"
        await self.bankickFunction(ctx, member, kickban, reason)

    async def bankickFunction(self, ctx, member, kickban, reason = None):
        memberid = ctx.message.mentions[0].id
        if kickban == "kick":
            kickedbanned = "kicked"
            kickingbanning = "kicking"
            texttosend = "kicktext"
        elif kickban == "ban":
            kickedbanned = "banned"
            kickingbanning = "banning"
            texttosend = "bantext"
        confirmationnumber = random.randint(1000, 9999)
        embed = discord.Embed(title="You are about to "+kickban+" user: " + ctx.message.mentions[0].display_name, description="This action is irreversable. To continue please type `" + str(confirmationnumber) + "` or to cancel, please type `cancel`.",colour=self.bot.getcolour())
        embed.add_field(name='User ID: ', value=str(ctx.message.mentions[0].id), inline=False)
        embed.add_field(name='User discord name: ',value=ctx.message.mentions[0].name + "#" + ctx.message.mentions[0].discriminator,inline=False)
        if reason:
            embed.add_field(name='Reason: ', value=reason, inline=False)
        else:
            embed.add_field(name='Reason: ', value="None given.", inline=False)
        baninfo = await ctx.channel.send(embed=embed)
        def confirmationcheck(msg):
            return (msg.content == str(confirmationnumber) or msg.content.lower() == "cancel") and ctx.channel.id == msg.channel.id and msg.author.id == ctx.author.id
        try:
            msg = await self.bot.wait_for('message', check=confirmationcheck, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.channel.send(":no_entry: | **" + ctx.author.display_name + "** The menu has closed due to inactivity.")
        else:
            if msg.content == str(confirmationnumber):
                embed = discord.Embed(title=":exclamation: | You have been "+ kickedbanned +" from " + ctx.guild.name,description="You have been "+ kickedbanned +" from " + ctx.guild.name + ". Details of this "+kickban+" are listed below.",colour=self.bot.getcolour())
                embed.add_field(name="User (You):", value=ctx.message.mentions[0].mention + " " + ctx.message.mentions[0].name + "#" + ctx.message.mentions[0].discriminator + " `" + str(ctx.message.mentions[0].id) + "`", inline=False)
                embed.add_field(name="Issued by:", value=ctx.author.mention + " " + ctx.author.name + "#" + ctx.author.discriminator + " `" + str(ctx.author.id) + "`", inline=False)
                if reason:
                    embed.add_field(name='Reason: ', value=reason, inline=False)
                else:
                    embed.add_field(name='Reason: ', value="None given.", inline=False)
                query = "SELECT * FROM guilds WHERE guildID = $1 AND "+texttosend+" IS NOT NULL"
                results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
                if results:
                    embed.add_field(name="Message from server:", value=results[texttosend])
                await ctx.channel.send(":white_check_mark: | "+kickingbanning.title()+" user...")
                await ctx.message.mentions[0].send(embed=embed)
                if reason:
                    if kickban == "kick":
                        await ctx.message.mentions[0].kick(reason=reason)
                    elif kickban == "ban":
                        await ctx.message.mentions[0].ban(reason=reason)
                else:
                    if kickban == "kick":
                        await ctx.message.mentions[0].kick(reason="None given.")
                    elif kickban == "ban":
                        await ctx.message.mentions[0].ban(reason="None given.")
            elif msg.content.lower() == "cancel":
                canceledtext = await ctx.channel.send(":white_check_mark: | Canceled!")
                await baninfo.delete()
                await asyncio.sleep(2)
                await canceledtext.delete()



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