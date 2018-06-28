import discord, asyncio, sys, traceback, checks, inflect, useful
from discord.ext import commands

class rolesCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=["role"])
    async def roles(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(":no_good: | Please enter a valid command. For a list of commands use: tt!roles help")

    @roles.command()
    async def add(self, ctx, *, roleName):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.channel.send("Role not found. Did you make an error?")
        else:
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "INSERT INTO Roles (roleID, guildID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, role.id, ctx.guild.id)
            await self.bot.db.release(connection)
            await ctx.channel.send(":white_check_mark: | Role added!")

    @roles.command(aliases=["delete"])
    async def remove(self, ctx, *, roleName):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.channel.send("Role not found. Did you make an error?")
        else:
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "DELETE FROM Roles WHERE roleID = $1"
                await self.bot.db.execute(query, role.id)
            await self.bot.db.release(connection)
            await ctx.channel.send(":white_check_mark: | Role deleted!")

    @roles.command()
    async def reset(self, ctx, *, roleName):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.channel.send("Role not found. Did you make an error?")
        else:
            connection = await self.bot.db.acquire()
            async with connection.transaction():
                query = "DELETE FROM Roles WHERE roleID = $1"
                await self.bot.db.execute(query, role.id)
                query = "INSERT INTO Roles (roleID, guildID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                await self.bot.db.execute(query, role.id)
            await self.bot.db.release(connection)
            await ctx.channel.send(":white_check_mark: | Role reset to default permissions!")

    @roles.command()
    async def setup(self, ctx, *, roleName):
        if not ctx.guild:
            await ctx.author.send(":no_good: | This command can not be used in DM!")
        else:
            role = discord.utils.get(ctx.guild.roles, name=roleName)
            if role is None:
                await ctx.channel.send("Role not found. Did you make an error?")
            else:
                query = "SELECT * FROM Roles WHERE roleID = $1"
                result = await ctx.bot.db.fetchrow(query, role.id)
                if result is None:
                    await ctx.channel.send("Role not found. Have you added it with `tt!role add`?")
                else:
                    choice = "choice"
                    options = ["admin", "moderator", "quizmaster", "muted", "custom", "close"]
                    timeout = False
                    while choice.lower() not in options and timeout == False:
                        embed = discord.Embed(title="Role loaded! Would you like to use a preset value?", description="Options: Admin, Moderator, Quizmaster, Muted, Custom, Close, Info", colour=self.bot.getcolour())
                        await ctx.channel.send(embed = embed)
                        try:
                            msg = await self.bot.wait_for('message', check=checks.roles_options1, timeout = 60.0)
                        except asyncio.TimeoutError:
                            try:
                                await ctx.channel.send(":no_entry: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!role edit again to restart the process.")
                            except TypeError:
                                await ctx.channel.send(":no_entry: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!role edit again to restart the process.")
                            timeout = True
                        else:
                            toeditTrue = []
                            toeditFalse = []
                            choice = msg.content.lower()
                            embedRole = discord.Embed(title="Role saved with the following permissions", description = "", colour = self.bot.getcolour())
                            if choice == "admin":
                                connection = await self.bot.db.acquire()
                                async with connection.transaction():
                                    query = "UPDATE Roles SET administrator = true WHERE roleID = $1"
                                    await self.bot.db.execute(query, role.id)
                                await self.bot.db.release(connection)
                                await ctx.channel.send("Got it! This role has been set as an administrator. (All commands enabled regardless of other settings)")
                            elif choice == "moderator":
                                toeditTrue = ["toggleraid, mute"]
                                await ctx.channel.send("Got it! This role has been set as a moderator. Moderators can mute people and toggle serverwide raid mode.")
                            elif choice == "quizmaster" or choice == "quiz master":
                                toeditTrue = ["pqstart", "pqend", "pqquestion", "pqsuperquestion", "pqoverride", "pqsettime", "pqqmhelp"]
                                toeditFalse = ["pqjoin"]
                                await ctx.channel.send("Got it! This role has been set as a quizmaster. Quizmasters can use every pub quiz command and are not considered when answers are been recorded.")
                            elif choice == "close":
                                await ctx.channel.send(":white_check_mark: | Menu closed!")
                                break
                            elif choice == "custom":
                                settings = [["Firstly", "pq start", "pqstart", "This command starts the pub quiz section of the bot"],
                                           ["Next", "pq end", "pqend", "This command ends any active pub quiz on the guild."],
                                           ["Next", "pq question", "pqquestion", "This command asks a question for everyone when a pub quiz is active."],
                                           ["Next", "pq superquestion", "pqsuperquestion", "This command asks a super question for everyone when a pub quiz is active."],
                                           ["Next", "pq override", "pqoverride", "This command allows a user to update other users scores during the pub quiz. This is used in case scores are incorrectly added."],
                                           ["Next", "pq settime", "pqsettime", "This command allows the user to change the amount of time the bot is open for answers during a pub quiz."],
                                           ["Next", "pq join", "pqjoin", "This means that users with this role can partake in the pub quiz section of the bot."],
                                           ["Next", "pq qmhelp", "pqqmhelp", "This command allows user to view the help commands for quizmasters."],
                                           ["Next", "bluetext", "bt", "This command causes the bot to echo text made of blue emojis."],
                                           ["Next", "bluetextcode", "btc", "This command makes the bot post the code of text made out of blue emojis."],
                                           ["Next", "setwelcome", "setwelcomechannel", "This command allows the user to set which channel the bot will post a welcome message too (if enabled)"],
                                           ["Next", "setwelcometext", "setwelcometext", "This commands allows the user to set the message sent upon a new user joining."],
                                           ["Next", "setfarewell", "setleavechannel", "This command allows the user to set which channel the bot will post a farewell message too (if enabled)"],
                                           ["Next", "setfarewelltext", "setleavetext", "This command allows the user to set the message sent upon a user leaving the server."],
                                           ["Next", "toggleraid", "toggleraid", "This command allows the user to toggle a server wide raid mode (new users are automatically assigned a role and sent a message)"],
                                           ["Next", "setraidrole", "setraidrole", "Allows the user to set the role that is assigned to new members during raidmode."],
                                           ["Next", "setraidtext", "setraidtext", "Allows the user to set the text sent to new members during raid mode."],
                                           ["Next", "mute", "mute", "Allows the user to assign the 'mute' role to the mentioned user."],
                                           ["Next", "cute", "cute", "Allows the user to call other users cute using bluetext command."],
                                           ["Finally", "setmuterole", "setmuterole", "Allows the user to set which role should be given to users when the mute command is invoked."]]
                                options2 = ["enabled", "disabled", "enable", "disable", "true", "false", "info", "skip", "yes", "no", "close"]
                                timeout2 = False
                                displayMessage = False
                                for counter in range (0,len(settings)):
                                    setting = settings[counter]
                                    choice2 = "choice"
                                    while choice2.lower() not in options2 and timeout2 == False:
                                        embed = discord.Embed(title=(setting[0] + " - would you like this role to be able to use the " + setting[1] + " command?"), description="Options: `Yes`, `No`, `Info`, `Skip`, `Close`", colour=self.bot.getcolour())
                                        await ctx.channel.send(embed=embed)
                                        try:
                                            msg2 = await self.bot.wait_for('message', check=checks.roles_options2, timeout=60.0)
                                        except asyncio.TimeoutError:
                                            try:
                                                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process. Settings **have not** been saved.")
                                            except TypeError:
                                                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process. Settings **have not** been saved.")
                                            timeout2 = True
                                        else:
                                            choice2 = msg2.content.lower()
                                            print(choice2)
                                            print(msg2.content)
                                            print("i made it here")
                                            if choice2 == "enabled" or choice2 == "enable" or choice2 == "true" or choice2 == "yes":
                                                print(choice)
                                                toeditTrue.append(setting[2])
                                                embedRole.add_field(name=setting[1], value="enabled")
                                                await ctx.channel.send(":white_check_mark: | This role can now use the " + setting[1] + " command.")
                                            elif choice2 == "disabled" or choice2 == "disable" or choice2 == "false" or choice2 == "no":
                                                print(choice)
                                                toeditFalse.append(setting[2])
                                                embedRole.add_field(name=setting[1], value="disabled")
                                                await ctx.channel.send(":white_check_mark: | This role can no longer use the " + setting[1] + " command.")
                                            elif choice2 == "info":
                                                print(choice)
                                                await ctx.channel.send(setting[3])
                                                choice2 = "choice"
                                            elif choice2 == "skip":
                                                print(choice)
                                                embedRole.add_field(name=setting[1], value="skipped")
                                                await ctx.channel.send(":white_check_mark: | Setting skipped!")
                                            elif choice2 == "close":
                                                print(choice)
                                                await ctx.channel.send(":white_check_mark: | Menu closed!")
                                                timeout2 = True
                                                displayMessage = True
                                                break

                            connection = await self.bot.db.acquire()
                            async with connection.transaction():
                                if toeditTrue != []:
                                    for column in toeditTrue:
                                        query = "UPDATE Roles SET " + column + " = true WHERE roleID = $1"
                                        await self.bot.db.execute(query, role.id)
                                if toeditFalse != []:
                                    for column in toeditFalse:
                                        query = "UPDATE Roles SET " + column + " = false WHERE roleID = $1"
                                        await self.bot.db.execute(query, role.id)
                            await self.bot.db.release(connection)
                            if timeout2 == False or displayMessage == True:
                                embedRole.add_field(name="For a full list of this roles permissions please use tt!role view rolename.", value="", inline=Truez)
                                await ctx.channel.send(embed = embedRole)
    @roles.command()
    async def view(self, ctx, *, roleName):
        await ctx.channel.send("coming soon")


    @roles.command()
    @checks.is_not_banned()
    async def help(self, ctx):
        embed = discord.Embed(title="Roles Help Menu", description="", colour=self.bot.getcolour())
        embed.add_field(name="Add", value="Adds a role to have customised bot permission levels.", inline=False)
        embed.add_field(name="Remove/Delete", value="Removes a roles custom permission levels.", inline=False)
        embed.add_field(name="Reset", value="Resets a roles permissions to default values.", inline=False)
        embed.add_field(name="Edit", value="Edits the custom permissions for the specified role.", inline=False)
        await ctx.channel.send(embed=embed)




def setup(bot):
    bot.add_cog(rolesCog(bot))