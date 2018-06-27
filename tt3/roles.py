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
    async def edit(self, ctx, *, roleName):
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
                            choice = msg.content.lower()
                            print(choice)
                            if choice == "admin":
                                connection = await self.bot.db.acquire()
                                async with connection.transaction():
                                    query = "UPDATE Roles SET administrator = true WHERE roleID = $1"
                                    await self.bot.db.execute(query, role.id)
                                await self.bot.db.release(connection)
                                await ctx.channel.send("Got it! This role has been set as an administrator. (All commands enabled)")
                            elif choice == "moderator":
                                connection = await self.bot.db.acquire()
                                async with connection.transaction():
                                    query = "UPDATE Roles SET (toggleraid, mute) = true WHERE roleID = $1"
                                    await self.bot.db.execute(query, role.id)
                                await self.bot.db.release(connection)
                                await ctx.channel.send("Got it! This role has been set as a moderator. Moderators can mute people and toggle serverwide raid mode.")
                            elif choice == "quizmaster" or choice == "quiz master":
                                connection = await self.bot.db.acquire()
                                async with connection.transaction():
                                    query = "UPDATE Roles SET (pqstart, pqend, pqquestion, pqsuperquestion, pqoverride, pqsettime, pqqmhelp) = true WHERE roleID = $1"
                                    await self.bot.db.execute(query, role.id)
                                    query = "UPDATE Roles SET (pqjoin) = false WHERE roleID = $1"
                                    await self.bot.db.execute(query, role.id)
                                await self.bot.db.release(connection)
                                await ctx.channel.send("Got it! This role has been set as a quizmaster. Quizmasters can use every pub quiz command and are not considered when answers are been recorded.")

                            elif choice == "close":
                                await ctx.channel.send(":white_check_mark: | Menu closed!")

                            elif choice == "custom":
                                await ctx.channel.send("blep")



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