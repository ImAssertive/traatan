import discord, asyncio, sys, traceback, checks, random, useful, inflect, random, re, math
from discord.ext import commands
from discord import app_commands

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
    async def settext(self, ctx, *, quiz_start_message):
        ##Creates new connection to database
        connection = await self.bot.db.acquire()
        ##Updates appropriate section in database
        async with connection.transaction():
            query = "UPDATE Guilds SET quiz_start_message = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, quiz_start_message,ctx.guild.id)
        ##Closes open connection to database
        await self.bot.db.release(connection)

        ##Confirms message change with the user
        await ctx.channel.send(":white_check_mark: | Pub quiz text set to `"+quiz_start_message+"`!")

    ##Command that outputs the current state of the pub quiz
    @pubquiz.command(name='isactive', aliases=['active'])
    @commands.has_permissions(kick_members=True)
    async def isactive(self, ctx):
        ##Queries database using guild ID
        query = "SELECT * FROM guilds WHERE guild_id = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)

        ##Returns message to the user depending on the results of the quiz_in_progress bool
        if result["quiz_in_progress"]:
            await ctx.channel.send(":exclamation: | The pub quiz is currently active in channel: **" + ctx.guild.get_channel(int(result["quiz_channel_id"])).name + "** with host: **"+ctx.guild.get_member(int(result["pubquizquestionuserid"])).name+"**")
        else:
            await ctx.channel.send(":no_entry: | The pub quiz is not currently active.")

    ##Command that allows users to update the end text for the pubquiz
    @pubquiz.command(name='setendtext', aliases=['sendtext'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Helper Powers", "Moderator Powers","Admin Powers", "Bot Tinkerer")
    async def setendtext(self, ctx, *, quiz_end_message):
        ##Creates new connection to database
        connection = await self.bot.db.acquire()
        ##Updates appropriate field in database
        async with connection.transaction():
            query = "UPDATE Guilds SET quiz_end_message = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, quiz_end_message,ctx.guild.id)
        ##Closes open connection to datansae
        await self.bot.db.release(connection)

        ##Confirms message change to the user
        await ctx.channel.send(":white_check_mark: | Pub quiz end text set to `"+quiz_end_message+"`!")

    ##Command that allows for all scores to be reset to 0
    @pubquiz.command(name="resetguildscoreboard", aliases=['resetscore', 'reset', 'resetall'])
    @checks.justme()
    async def resetguildscoreboard(self, ctx, season_number: int = None):
        """Resets the pub quiz scores for the entire guild for a specific season.

        If no season number is provided, it resets scores for the current season.
        """

        # Get the current season number if not provided
        if season_number is None:
            query = "SELECT current_season_number FROM guilds WHERE guild_id = $1"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            season_number = result["current_season_number"]

        # Check if a quiz is in progress
        query = "SELECT quiz_in_progress FROM guilds WHERE guild_id = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result["quiz_in_progress"]:
            await ctx.send(":no_entry: | A pub quiz is currently active! Please end the current pub quiz to continue.")
            return

        # Confirmation prompt
        confirmation_number = random.randint(1000, 9999)
        await ctx.send(
            f":clock1: | {ctx.author.display_name}, are you sure? This will reset the pub quiz scores for season {season_number} for the entire guild. To continue please type `{confirmation_number}`")

        def confirmation_check(msg):
            return msg.content == str(
                confirmation_number) and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id

        try:
            msg = await self.bot.wait_for('message', check=confirmation_check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send(f":no_entry: | {ctx.author.display_name}, the reset command has closed due to inactivity.")
        else:
            if msg.content == str(confirmation_number):
                connection = await self.bot.db.acquire()
                async with connection.transaction():
                    # Delete scores for the specified season and guild
                    query = "DELETE FROM user_scores WHERE guild_id = $1 AND season_number = $2"
                    await self.bot.db.execute(query, ctx.guild.id, season_number)
                await self.bot.db.release(connection)
                await ctx.send(f":white_check_mark: | Pub quiz scores for season {season_number} reset!")


    ##Command that allows users to start a new pub quiz
    @pubquiz.command(name='start', aliases=['begin', 'go'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Bot Tinkerer")
    async def start(self, ctx):
        # 1. Ensure all guild members are in the 'guild_users' table
        await ctx.bot.get_cog('setupCog').addmembers.invoke(ctx)

        # 2. Check if a quiz is already active
        query = "SELECT quiz_in_progress FROM guilds WHERE guild_id = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result["quiz_in_progress"]:
            await ctx.channel.send(":no_entry: | A quiz is already active!")
            return

        # 3. Create the "Pub Quiz DM" role
        #dm_role = discord.utils.get(ctx.guild.roles, name="Pub Quiz DM")
        #if not dm_role:
        #    dm_role = await ctx.guild.create_role(name="Pub Quiz DM", reason="Traatan Automatic Pubquiz DM Role Creation")

        # 4. Update the database
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            # 4.1 Set quiz_in_progress to True
            query = "UPDATE guilds SET quiz_in_progress = TRUE WHERE guild_id = $1"
            await self.bot.db.execute(query, ctx.guild.id)

            # 4.2 Set quiz_channel_id
            query = "UPDATE guilds SET quiz_channel_id = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, ctx.channel.id, ctx.guild.id)

            # 4.3 Reset current_question_number
            query = "UPDATE guilds SET current_question_number = 0 WHERE guild_id = $1"
            await self.bot.db.execute(query, ctx.guild.id)

            # 4.4  Increment quiz number (no season update here)
            query = """
                UPDATE guilds 
                SET current_quiz_number = current_quiz_number + 1
                WHERE guild_id = $1
            """
            await self.bot.db.execute(query, ctx.guild.id)
        await self.bot.db.release(connection)

        # 5. Get the quiz start message
        query = "SELECT quiz_start_message FROM guilds WHERE guild_id = $1"
        results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        quiz_start_message = results["quiz_start_message"] or "Pub Quiz Started!"

        # 6. Send the start message
        results_embed = discord.Embed(
            title=quiz_start_message,
            description="Answer questions by typing your answers in this channel, or using the /a command!",
            color=self.bot.getcolour()
        )
        await ctx.channel.send(embed=results_embed)

    ##Command to toggle a user receiving pub quiz questions as direct messages
    @pubquiz.command(name='dm', aliases=['dmme', 'toggledms', 'toggledm'])
    @checks.pubquiz_active()
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
            #await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @pubquiz.command(name='stop', aliases =['end', 'halt'])
    @checks.pubquiz_active()
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Bot Tinkerer")
    async def stop(self, ctx):
        # 1. Send the quiz end message
        query = "SELECT quiz_end_message FROM guilds WHERE guild_id = $1"
        results = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        quiz_end_message = results["quiz_end_message"] or "That was the pub quiz! I hope you enjoyed. :)"
        await ctx.channel.send(quiz_end_message)

        # 2. Display the leaderboards
        leaderboard_embeds = await self.getLeaderboard(ctx)
        for embed in leaderboard_embeds:
            await ctx.channel.send(embed=embed)
        # 3. Update the database to mark the quiz as inactive
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = """
                UPDATE guilds 
                SET quiz_in_progress = FALSE, 
                    quiz_channel_id = NULL, 
                    current_question_number = 1
                WHERE guild_id = $1
            """
            await self.bot.db.execute(query, ctx.guild.id)
        await self.bot.db.release(connection)

    #Returns an array of embeds containing information on the weekly leaderboard for a pub quiz
    async def getLeaderboard(self, ctx, total=False):
        # 1. Get current season and quiz numbers from the 'guilds' table
        query = "SELECT current_season_number, current_quiz_number FROM guilds WHERE guild_id = $1"
        guild_data = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        current_season = guild_data["current_season_number"]
        current_quiz = guild_data["current_quiz_number"]

        if total:
            # 2. Query for total scores for the current season
            query = """
                SELECT user_id, SUM(score) as total_score
                FROM user_scores
                WHERE guild_id = $1 AND season_number = $2
                GROUP BY user_id
                HAVING SUM(score) != 0
                ORDER BY total_score DESC
            """
            result = await ctx.bot.db.fetch(query, ctx.guild.id, current_season)
        else:
            # 3. Query for scores for the current season and quiz (no changes here)
            query = """
                SELECT user_id, score
                FROM user_scores
                WHERE guild_id = $1 
                AND season_number = $2 
                AND quiz_number = $3
                AND score != 0
                ORDER BY score DESC
            """
            result = await ctx.bot.db.fetch(query, ctx.guild.id, current_season, current_quiz)

        # 4. Calculate total pages and create embed pages
        pages = []
        total_pages = math.ceil(len(result) / 25)

        for page in range(0, total_pages):
            # Update embed title to reflect the type of leaderboard
            if total:
                title = f"{ctx.guild.name} Pub Quiz Leaderboard (Total for Season {current_season})"
            else:
                title = f"{ctx.guild.name} Pub Quiz Leaderboard (Season {current_season}, Quiz {current_quiz})"

            results_embed = discord.Embed(title=title, color=self.bot.getcolour())
            results_embed.set_footer(text=f"Current Page: ({page + 1}/{total_pages})")

            if (page + 1) == total_pages:
                final_result = len(result)
            else:
                final_result = (page + 1) * 25


            # 5. Iterate over results and add fields to embeds
            for row in range(page * 25, final_result):
                try:
                    user_id = int(result[row]["user_id"])
                    member = ctx.guild.get_member(user_id)

                    # Fetch pronouns from guild_users table
                    pronoun_query = """
                        SELECT pronouns FROM guild_users
                        WHERE user_id = $1 AND guild_id = $2
                    """
                    pronoun_result = await ctx.bot.db.fetchrow(pronoun_query, user_id, ctx.guild.id)
                    pronouns = pronoun_result["pronouns"] if pronoun_result["pronouns"] else "they/them"  # Default to they/them
                    object_pronoun = useful.extract_object_pronoun(pronouns)

                    if total:
                        total_score = result[row]["total_score"]
                        results_embed.add_field(
                            name=f"{member.display_name} ({member.name})",
                            value=f"has a total of **{total_score}** points. Placing {object_pronoun} **{inflect.engine().ordinal(row + 1)}**.",
                            inline=False
                        )
                    else:
                        score = result[row]["score"]
                        # You might need to adjust this query to get the total score for the user across all seasons
                        query_total = """
                            SELECT SUM(score) as total_score
                            FROM user_scores
                            WHERE guild_id = $1 AND user_id = $2
                        """
                        total_score_result = await ctx.bot.db.fetchrow(query_total, ctx.guild.id, user_id)
                        total_score = total_score_result["total_score"] if total_score_result else 0

                        results_embed.add_field(
                            name=f"{member.display_name} ({member.name})",
                            value=f"has **{score}** points this week. Placing {object_pronoun} **{inflect.engine().ordinal(row + 1)}**. ({total_score} total points)",
                            inline=False
                        )
                except AttributeError as e:
                    results_embed.add_field(name="User left guild", value="Data not found.", inline=False)
                    traceback_str = traceback.format_exc()
                    print(e)
                    print(traceback_str)
            pages.append(results_embed)
        return pages

    #Outputs the current total results of a pub quiz season to a user or in a channel
    @pubquiz.command(name="totalleaderboard", aliases=['total', 'totalscoreboard', 'totalscores','totalscore'])
    async def totalleaderboard(self, ctx):
        # Determines if the user invoking the command has permission to post the leaderboards publicly
        has_permission = await checks.user_has_role(ctx, ["Quizmaster", "Pub Quiz Senate"])
        # Obtains array of leaderboard embeds from the getLeaderboards function
        embeds = await self.getLeaderboard(ctx, total=True)
        for embed in embeds:
            # If the user has permission, send the results to the channel the command was invoked in
            if has_permission:
                await ctx.channel.send(embed=embed)
                return
            # Else directly message the user with results
            else:
                await ctx.author.send(embed=embed)
                return
        # This should almost never be reached
        await ctx.channel.send(":no_entry: | Oh dear... it appears there is no leaderboard to post.")

    #Outputs the weekly results of a pub quiz to a user or in a channel
    @pubquiz.command(name="leaderboard", aliases=['scoreboard', 'score', 'scores'])
    @checks.pubquiz_active()
    async def leaderboard(self, ctx):
        # Determines if the user invoking the command has permission to post the leaderboards publicly
        has_permission = await checks.user_has_role(ctx, ["Quizmaster", "Pub Quiz Senate"])  # Use the updated has_role check

        # Obtains array of leaderboard embeds from the getLeaderboards function
        embeds = await self.getLeaderboard(ctx)  # total=False by default

        for embed in embeds:
            if has_permission:
                # If the user has permission, send the results to the channel the command was invoked in
                await ctx.channel.send(embed=embed)
                return
            else:
                # Else directly message the user with results
                await ctx.author.send(embed=embed)
                return
        await ctx.channel.send(":no_entry: | Oh dear... it appears there is no leaderboard to post. Oops.")


    @pubquiz.command(name="override", aliases=['or', 'oride'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    async def override(self, ctx, member: discord.Member, value: int):
        """Overrides the mentioned user's score for the current quiz and season.

        This allows for mistakes to be quickly corrected.
        Usage: !pq override @user 5 (adds 5 points)
               !pq override @user -3 (subtracts 3 points)
        """

        if value == 0:
            await ctx.channel.send(":no_entry: | The score cannot be modified by 0.")
            return

        # Get current season and quiz numbers
        query = "SELECT current_season_number, current_quiz_number FROM guilds WHERE guild_id = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        current_season = result["current_season_number"]
        current_quiz = result["current_quiz_number"]

        connection = await self.bot.db.acquire()
        async with connection.transaction():
            # Update the user's score for the current quiz and season
            query = """
                INSERT INTO user_scores (user_id, guild_id, season_number, quiz_number, score)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (user_id, guild_id, season_number, quiz_number) DO UPDATE
                SET score = $5;
            """
            await self.bot.db.execute(query, member.id, ctx.guild.id, current_season, current_quiz, value)
        await self.bot.db.release(connection)

        action = "increased" if value > 0 else "decreased"
        abs_value = abs(value)

        await ctx.channel.send(
            f":white_check_mark: | User **{member.display_name} ({member.name})** has had their score for this quiz {action} by **{abs_value}**.")


    @pubquiz.command(name="settime", aliases=['st'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
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
                    query = "UPDATE Guilds SET quiz_default_duration = $1  WHERE guild_id = $2"
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

    async def update_scores(self, ctx, correct_members, to_add, exact=False):
        connection = await ctx.bot.db.acquire()
        embed = discord.Embed(
            title="Reduced the following users' scores:" if to_add < 0 else "Increased the following users' scores:",
            color=ctx.bot.getcolour()
        )

        # Get current season, quiz number, and super question flag from 'guilds'
        query = """
            SELECT current_season_number, current_quiz_number, quiz_last_question_super 
            FROM guilds 
            WHERE guild_id = $1
        """
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        current_season = result["current_season_number"]
        current_quiz = result["current_quiz_number"]
        last_question_was_super = result["quiz_last_question_super"]

        scores = [12, 10, 10, 8, 8, 8, 8, 8, 7]
        for i, member_id in enumerate(correct_members):
            points = self._calculate_points(len(correct_members), last_question_was_super, exact, i, scores)

            async with connection.transaction():
                # Update or insert score in 'user_scores' table
                query = """
                    INSERT INTO user_scores (user_id, guild_id, season_number, quiz_number, score)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (user_id, guild_id, season_number, quiz_number) DO UPDATE
                    SET score = user_scores.score + $5;
                """
                await ctx.bot.db.execute(query, member_id, ctx.guild.id, current_season, current_quiz, to_add * points)

            member = ctx.guild.get_member(member_id)
            embed.add_field(
                name=f"{member.display_name} ({member.name})",
                inline=False,
                value=("gained" if to_add > 0 else "lost") + f" **{abs(to_add * points)}** points."
            )

        await ctx.bot.db.release(connection)
        await ctx.channel.send(embed=embed)

    def _calculate_points(self, num_correct_members, last_question_was_super, exact, i, scores):
        if last_question_was_super:
            return 23 if exact else 18
        elif num_correct_members == 1 and not last_question_was_super:
            return 16
        elif num_correct_members == 4 and not last_question_was_super:
            return [12, 10, 10, 9][i]
        else:
            return scores[i] if i < len(scores) else scores[-1]

    @pubquiz.command(name="undo")
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    async def undo(self, ctx):
        correctMembers = [useful.getid(member) for member in re.findall("<@.*?>", ctx.message.content)]
        await self.update_scores(ctx, correctMembers, -1)

    @pubquiz.command(name="exactundo", aliases=['undo_exact', 'exact_undo'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    async def exactundo(self, ctx):
        correctMembers = [useful.getid(member) for member in re.findall("<@.*?>", ctx.message.content)]
        await self.update_scores(ctx, correctMembers, -1, True)

    @pubquiz.command(name="correct")
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    async def correct(self, ctx):
        ##Uses regex to find the ID of all correct members if mentions have been used
        correctMembers = [useful.getid(member) for member in re.findall("<@.*?>", ctx.message.content)]
        await self.update_scores(ctx, correctMembers, 1)

    @pubquiz.command(name="exactcorrect", aliases=['correct_exact', 'exact_correct'])
    @checks.has_role("Quizmaster", "Pub Quiz Senate", "Moderator Powers", "Admin Powers", "Bot Tinkerer")
    async def exactcorrect(self, ctx):
        correctMembers = [useful.getid(member) for member in re.findall("<@.*?>", ctx.message.content)]
        await self.update_scores(ctx, correctMembers, 1, True)


    #Help command
    @pubquiz.command()
    async def help(self, ctx):
        #Creates an embed filled with useful information on commands and returns it to the user
        embed = discord.Embed(title="PubQuiz Help", description="Help for the following tt!pubquiz commands:", colour=self.bot.getcolour())
        embed.add_field(name="total", value ="DM's the user the total scoreboard for the pub quiz.")
        embed.add_field(name="leaderboard", value ="DM's the user the weekly scoreboard. Can only be used when a pub quiz is active.")
        await ctx.channel.send(embed = embed)

    #Quizmasters Help Command
    @pubquiz.command()
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
    async def question(self, ctx, *, question):
        #Calls the question function, setting the superQuestion bool to false
        superQuestion = False
        await ctx.message.delete()
        await self.questionFunction(ctx, question, superQuestion)

    @pubquiz.command(name="setseason", aliases=['ss'])
    @checks.has_role("Staff", "Ghost")
    async def set_season(self, ctx, season_number: int):
        """
        Sets the current quiz season number for this server.

        Usage: tt!pq setseason 3
        """

        if season_number <= 0:
            await ctx.send(":no_entry: | Season number must be a positive integer.")
            return

        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE guilds SET current_season_number = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, season_number, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.send(f":white_check_mark: | Current quiz season set to {season_number}!")

    @pubquiz.command(name="setquestion", aliases=['sqn'])
    @checks.has_role("Staff", "Ghost", "Quizmaster", "Pub Quiz Senate")
    @checks.pubquiz_active()
    async def set_question_number(self, ctx, question_number: int):
        """
        Sets the current quiz question number for this server.

        Usage: tt!pq setquestion 5
        """

        if question_number <= 0:
            await ctx.send(":no_entry: | Question number must be a positive integer.")
            return

        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE guilds SET current_question_number = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, question_number, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.send(f":white_check_mark: | Current quiz question number set to {question_number}!")

    @pubquiz.command(name="setquiz", aliases=['sqz'])
    @checks.has_role("Staff", "Ghost")
    async def set_quiz_number(self, ctx, quiz_number: int):
        """
        Sets the current quiz number within the current season for this server.

        Usage: !pq setquiz 3
        """

        if quiz_number <= 0:
            await ctx.send(":no_entry: | Quiz number must be a positive integer.")
            return

        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE guilds SET current_quiz_number = $1 WHERE guild_id = $2"
            await self.bot.db.execute(query, quiz_number, ctx.guild.id)
        await self.bot.db.release(connection)

        await ctx.send(f":white_check_mark: | Current quiz number set to {quiz_number}!")

    #Command to allow a quizmaster to start a new super question (awarding bonus points)
    @pubquiz.command(name='superquestion', aliases=['sq', 'spq'])
    @checks.pubquiz_active()
    @checks.has_role("Quizmaster", "Pub Quiz Senate")
    async def superquestion(self, ctx, *, question):
        #Calls the question function, setting the superQuestion bool to false
        superQuestion = True
        await ctx.message.delete()
        await self.questionFunction(ctx, question, superQuestion)
        

    #Allows a quizmaster to display the answer in an easy to read embed
    @pubquiz.command(name="post_answer", aliases=["postanswer", "pa"])
    @checks.has_role("Quizmaster", "Pub Quiz Senate")
    @checks.pubquiz_active()
    async def post_answer(self, ctx, *, answer):
        #Creates a discord embed object before sending it to the channel where the command was invoked
        embed = discord.Embed(title="The answer is...", description = answer, colour=self.bot.getcolour())
        await ctx.channel.send(embed=embed)

        #Deletes the original invoke message
        #await ctx.message.delete()

    async def questionFunction(self, ctx, question, super_question):
        # Obscure question from Google
        question = '\u2060'.join(question[i:i + 1] for i in range(0, len(question), 1))

        # Get current quiz status and question number
        query = "SELECT quiz_in_progress, current_question_number, quiz_default_duration FROM guilds WHERE guild_id = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)

        # Validate there is a quiz active
        if not result["quiz_in_progress"]:
            await ctx.channel.send(":no_entry: | There is no quiz in progress!")
            return

        # Check if a question is already active in this guild
        if ctx.guild.id in self.bot.active_quiz_guilds:
            await ctx.channel.send(":no_entry: | There is already an active question in this server!")
            return

        # Add guild and channel ID to the active quiz dictionary
        self.bot.active_quiz_guilds[ctx.guild.id] = ctx.channel.id

        try:
            # Clear saved answers for the current guild only
            self.bot.pubquiz_answers[ctx.guild.id] = []

            # Increment the current question number
            current_question = result["current_question_number"] + 1

            # Update the database
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                # Update the current question number and super question flag
                query = """
                    UPDATE guilds 
                    SET current_question_number = $1, 
                        quiz_last_question_super = $2
                    WHERE guild_id = $3
                """
                await self.bot.db.execute(query, current_question, super_question, ctx.guild.id)
            await self.bot.db.release(connection)

            # Store the question asker's ID in memory
            self.bot.active_questions[ctx.guild.id] = (ctx.channel.id, ctx.author.id)

            # Create embeds for questions
            if super_question:
                question_embed = discord.Embed(title=f"**SUPER QUESTION {current_question}!**", description=question,
                                               color=self.bot.getcolour())
                question_dm_embed = discord.Embed(title=f"**SUPER QUESTION {current_question}!**", description=question,
                                                  color=self.bot.getcolour())
            else:
                question_embed = discord.Embed(title=f"**Question {current_question}!**", description=question,
                                               color=self.bot.getcolour())
                question_dm_embed = discord.Embed(title=f"**Question {current_question}!**", description=question,
                                                  color=self.bot.getcolour())

            question_embed.add_field(name="Please type your answers now.", value=" ".join([ctx.bot.user.mention] * 5))
            question_dm_embed.add_field(name="Please type your answers now.", value=" ".join([ctx.channel.mention] * 5))

            # DM all members with the "Pub Quiz DM" role
            dm_role = discord.utils.get(ctx.guild.roles, name="Pub Quiz DM")
            for member in ctx.guild.members:
                if dm_role in member.roles:
                    await member.send(embed=question_dm_embed)

            # Send the question embed to the channel
            await ctx.channel.send(embed=question_embed)

            # Wait for answers and close submissions
            await asyncio.sleep(result["quiz_default_duration"])
            await ctx.channel.send("Answers are now closed!")

            # Display answers for the current guild
            pages = []
            total_pages = math.ceil(len(self.bot.pubquiz_answers[ctx.guild.id]) / 25)
            for i in range(0, total_pages):
                to_append = discord.Embed(title="Answers:", color=self.bot.getcolour())
                to_append.set_footer(text=f"Current Page: ({i + 1}/{total_pages})")
                pages.append(to_append)

            # Loops over answers provided, adding them to the correct embed
            for index, answer in enumerate(self.bot.pubquiz_answers[ctx.guild.id]):  # Use enumerate to get the index
                if answer[1] == ctx.guild.id:  # This check might be redundant now
                    print("Current answer index: " + str(math.ceil(index + 1 / 25) - 1))
                    print("Current answer number: " + str(index + 1))  # Use index + 1 for answer number
                    pages[math.ceil((index + 1) / 25) - 1].add_field(
                        name=answer[0].display_name + " (" + answer[0].name+ ") answered:",
                        value=answer[2],
                        inline=False
                    )
            # Output final results embeds
            for embed in pages:
                await ctx.channel.send(embed=embed)

            # Clear answers for the current guild
            del self.bot.pubquiz_answers[ctx.guild.id]

        except Exception as e:
            print(e)
            traceback_str = traceback.format_exc()
            print(traceback_str)
            await ctx.channel.send("An error occurred:\n```"+str(e)+"```")
            await ctx.channel.send("Traceback:\n```"+traceback_str+"```")

        finally:
            # Remove guild from the active quiz set
            del self.bot.active_quiz_guilds[ctx.guild.id]
            del self.bot.active_questions[ctx.guild.id]

    @app_commands.command(name="a", description="Add an answer to the current pub quiz question.")
    @app_commands.guild_only()  # Ensure this command can only be used in guilds
    async def add_answer(self, interaction: discord.Interaction, answer: str):
        if interaction.guild.id in self.bot.active_quiz_guilds:
            _, question_asker_id = self.bot.active_questions[interaction.guild.id]

            # Ignore the question asker's answers
            if str(interaction.user.id) == str(question_asker_id):
                await interaction.response.send_message(":no_entry: | You can't answer your own question!", ephemeral=True)
                return

            # Append the answer to the guild's list in pubquiz_answers
            self.bot.pubquiz_answers.setdefault(interaction.guild.id, []).append([interaction.user, interaction.guild.id, answer])
            await interaction.response.send_message(":white_check_mark: | Answer added!", ephemeral=True)
        else:
            await interaction.response.send_message(":no_entry: | There is no active question in this server!", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild is not None:  # Message is in a guild (server)
            if ctx.author == self.bot.user:
                return  # Ignore bot's own messages

            # Check if there's an active question in this guild
            if ctx.guild.id in self.bot.active_questions:
                _, question_asker_id = self.bot.active_questions[ctx.guild.id]

                # Ignore the question asker's messages
                if str(ctx.author.id) == str(question_asker_id):
                    return

                # Check if the message is in the quiz channel
                if ctx.channel.id == self.bot.active_quiz_guilds[ctx.guild.id]:
                    # Append the answer to the guild's list in pubquiz_answers
                    self.bot.pubquiz_answers.setdefault(ctx.guild.id, []).append(
                        [ctx.author, ctx.guild.id, ctx.content])
                    await ctx.delete()

    ''''@commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild is not None:
            if ctx.author == self.bot.user or str(ctx.author.id) == str(self.bot.pubquizQuestionUserID) or ctx.channel.id != self.bot.quiz_channel_id or self.bot.pubquizActive == False:
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
                await ctx.add_reaction("\N{WHITE HEAVY CHECK MARK}")'''


async def setup(bot):
    await bot.add_cog(pubquizCog(bot))
    return
