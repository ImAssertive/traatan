import discord, asyncio, sys, traceback, checks, useful, asyncpg, random, ast, re
from discord.ext import commands


class adminCog(commands.Cog):
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
    async def say(self, ctx, channel: discord.TextChannel, *, message):
        """
        Sends a message to the specified channel.
        Usage: !say #channel-name This is the message to send
        """
        try:
            await channel.send(message)
            await ctx.message.add_reaction('✅')  # Add a checkmark reaction on success
        except discord.Forbidden:
            await ctx.send("I don't have permission to send messages in that channel.")
        except discord.NotFound:
            await ctx.send("I couldn't find that channel. Make sure you're using the correct channel mention or ID.")

    @commands.command(name="setfarewell", aliases=['setleave', 'setleavechannel', 'setfarewellchannel'])
    @checks.justme()
    async def setfarewell(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE guilds SET leave_enabled = TRUE, leave_channel_id = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done! Farewell channel set here.")

    @commands.command(name="setwelcome", aliases=['setwelcomechannel'])
    @checks.justme()
    async def setwelcome(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE guilds SET welcome_enabled = TRUE, welcome_channel_id = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done! Welcome channel set here.")

    @commands.command()
    @checks.justme()
    async def setwelcometext(self, ctx, *, welcometext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE guilds SET welcome_message = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, welcometext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Welcome text set to ```" + welcometext + "```")

    @commands.command(name="setfarewelltext", aliases =['setleavetext'])
    @checks.justme()
    async def setfarewelltext(self, ctx, *, leavetext):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE guilds SET leave_message = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, leavetext, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send("Done! Farewell text set to: ```" + leavetext + "```")

        @commands.command()
        @checks.justme()
        async def enable_welcome(self, ctx):
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE guilds SET welcome_enabled = TRUE WHERE guild_id = $1"
                await self.bot.db.execute(query, ctx.guild.id)
            await self.bot.db.release(connection)
            await ctx.send(":white_check_mark: | Welcome messages enabled!")

        @commands.command()
        @checks.justme()
        async def disable_welcome(self, ctx):
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "UPDATE guilds SET welcome_enabled = FALSE WHERE guild_id = $1"
                await self.bot.db.execute(query, ctx.guild.id)
            await self.bot.db.release(connection)
            await ctx.send(":white_check_mark: | Welcome messages disabled!")

    @commands.command(name='setbantext')
    @commands.has_permissions(ban_members=True)
    async def setbantext(self, ctx, *, banText):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE guilds SET ban_message = $1 WHERE guild_id  = $2"
            await self.bot.db.execute(query, banText, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Ban text set to `"+banText+"`!")

    # @commands.command()
    # @checks.justme()
    # async def eval(ctx, *, cmd):
    #     fn_name = "_eval_expr"
    #     cmd = cmd.strip("` ")
    #     # add a layer of indentation
    #     cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
    #     # wrap in async def body
    #     body = f"async def {fn_name}():\n{cmd}"
    #     parsed = ast.parse(body)
    #     body = parsed.body[0].body
    #     insert_returns(body)
    #     env = {
    #         'bot': ctx.bot,
    #         'discord': discord,
    #         'commands': commands,
    #         'ctx': ctx,
    #         '__import__': __import__
    #     }
    #     exec(compile(parsed, filename="<ast>", mode="exec"), env)
    #
    #     result = (await eval(f"{fn_name}()", env))
    #     await ctx.send(result)

    @commands.command(name='setkicktext')
    @commands.has_permissions(ban_members=True)
    async def setkicktext(self, ctx, *, kickText):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Guilds SET kick_message = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, kickText,ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Kick text set to `"+kickText+"`!")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await self._ban_or_kick(ctx, member, "ban", reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, member_id: int):
        try:
            await ctx.guild.ban(discord.Object(id=member_id), delete_message_days=0)
            await ctx.channel.send(f":white_check_mark: | Banned ID `{member_id}`")
        except discord.NotFound:
            await ctx.channel.send(":no_entry: | An error occurred. Was that a valid user ID?")

    @commands.command()
    async def setpronouns(self, ctx, *, pronouns: str):
        """Sets the user's pronouns for this server.

        Usage: tt!setpronouns she/her
        """

        # Basic validation - you might want to enhance this
        if not re.match(r"^[a-zA-Z]+/[a-zA-Z]+$", pronouns):
            await ctx.send("Invalid pronoun format. Please use the format 'pronoun/pronoun' (e.g., he/him, they/them). Please note this is only a requirement because my developer is bad at coding. (Sorry about that)")
            return

        connection = await self.bot.db.acquire()
        async with connection.transaction():
            # Update or insert pronouns in 'guild_users' table
            query = """
                INSERT INTO guild_users (user_id, guild_id, pronouns)
                VALUES ($1, $2, $3)
                ON CONFLICT (user_id, guild_id) DO UPDATE
                SET pronouns = $3;
            """
            await self.bot.db.execute(query, ctx.author.id, ctx.guild.id, pronouns)
        await self.bot.db.release(connection)

        await ctx.send(f":white_check_mark: | Your pronouns have been set to **{pronouns}** for this server.")


    @commands.command(name='sync')
    @checks.justme()
    async def sync(self, ctx):
        try:
            await self.bot.tree.sync()
            await ctx.send(f":white_check_mark: | Slash commands synced.")
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(e)
            print(traceback_str)

    @commands.command(name='sync_current')
    @checks.justme()
    async def sync_current(self, ctx):
        try:
            await self.bot.tree.sync(guild=ctx.guild)
            await ctx.send(f":white_check_mark: | Slash commands synced for guild ID **" + str(ctx.guild.id)+"**")
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(e)
            print(traceback_str)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await self._ban_or_kick(ctx, member, "kick", reason)

    async def _ban_or_kick(self, ctx, member, action, reason=None):
        action_past_tense = "banned" if action == "ban" else "kicked"
        action_present_participle = "banning" if action == "ban" else "kicking"
        text_to_send = "ban_message" if action == "ban" else "kick_message"

        confirmation_number = random.randint(1000, 9999)

        embed = discord.Embed(
            title=f"You are about to {action} user: {member.display_name}",
            description=f"This action is irreversible. To continue please type `{confirmation_number}` or to cancel, please type `cancel`.",
            color=self.bot.getcolour()
        )
        embed.add_field(name='User ID:', value=str(member.id), inline=False)
        embed.add_field(name='User discord name:', value=f"{member.name}#{member.discriminator}", inline=False)
        embed.add_field(name='Reason:', value=reason or "None given.", inline=False)

        ban_info = await ctx.channel.send(embed=embed)

        def confirmation_check(msg):
            return (msg.content == str(confirmation_number) or msg.content.lower() == "cancel") and \
                msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id

        try:
            msg = await self.bot.wait_for('message', check=confirmation_check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.channel.send(f":no_entry: | {ctx.author.display_name}, the menu has closed due to inactivity.")
        else:
            if msg.content == str(confirmation_number):
                embed = discord.Embed(
                    title=f":exclamation: | You have been {action_past_tense} from {ctx.guild.name}",
                    description=f"You have been {action_past_tense} from {ctx.guild.name}. Details of this {action} are listed below.",
                    color=self.bot.getcolour()
                )
                embed.add_field(name="User (You):",
                                value=f"{member.mention} {member.name}#{member.discriminator} `{member.id}`",
                                inline=False)
                embed.add_field(name="Issued by:",
                                value=f"{ctx.author.mention} {ctx.author.name}#{ctx.author.discriminator} `{ctx.author.id}`",
                                inline=False)
                embed.add_field(name='Reason:', value=reason or "None given.", inline=False)

                query = f"SELECT {text_to_send} FROM guilds WHERE guild_id = $1 AND {text_to_send} IS NOT NULL"
                results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
                if results:
                    embed.add_field(name="Message from server:", value=results[text_to_send])

                await ctx.channel.send(f":white_check_mark: | {action_present_participle.title()} user...")
                await member.send(embed=embed)

                if action == "kick":
                    await member.kick(reason=reason)
                elif action == "ban":
                    await member.ban(reason=reason, delete_message_days=0)

            elif msg.content.lower() == "cancel":
                canceled_text = await ctx.channel.send(":white_check_mark: | Canceled!")
                await ban_info.delete()
                await asyncio.sleep(2)
                await canceled_text.delete()


async def setup(bot):
    await bot.add_cog(adminCog(bot))
    return