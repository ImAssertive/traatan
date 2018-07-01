import discord, asyncio, sys, traceback, checks, inflect, useful
from discord.ext import commands

class rolesCog:
    def __init__(self, bot):
        self.bot = bot


    async def test(self, ctx):
        await ctx.channel.send("test")


    @commands.group(pass_context=True, aliases=["role"])
    async def roles(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(":no_entry: | Please enter a valid command. For a list of commands use: tt!roles help")

    async def rolesMainMenu(self, ctx, menu, role):
        embed = discord.Embed(title='Role Permission Main Menu', description="Options:\n0: Admin\n1: Moderation\n2: Pub Quiz\n3: Miscellaneous\n4: Set role to preset permission level\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Current role: "+ role.name +"("+ str(role.id)+")")
        await menu.edit(embed=embed)
        #options = ["1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3", "5\u20e3", "6\u20e3", "7\u20e3","8\u20e3", "9\u20e3", "\U0001f51f", "❌"]
        options = ["0\u20e3", "1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3", "❌"]
        def roles_emojis_main_menu(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=roles_emojis_main_menu, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the editrole command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the editrole command to restart the process.")
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                await self.rolesAdminMenu(ctx, menu, role)
            elif str(reaction.emoji) == "1\u20e3":
                await self.rolesModMenu(ctx, menu, role)
            elif str(reaction.emoji) == "2\u20e3":
                await self.rolesPubQuizMenu(ctx, menu, role)
            elif str(reaction.emoji) == "3\u20e3":
                await self.rolesMiscMenu(ctx, menu, role)
            elif str(reaction.emoji) == "4\u20e3":
                await self.rolesPresetMenu(ctx, menu, role)
            elif str(reaction.emoji) == "❌":
                await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()

    async def rolesAdminMenu(self, ctx, menu, role):
        embed = discord.Embed(title='Admin Permission options', description="The administrator permission allows the role to access all bot commands regardless of other permission levels.\n\nOptions:\n0: Enable\n1: Disable\n2: Back\nx: Closes Menu", colour=self.bot.getcolour())
        embed.set_footer(text="Current role: "+ role.name +"("+ str(role.id)+")")
        await menu.edit(embed=embed)
        options = ["0\u20e3", "1\u20e3", "2\u20e3", "❌"]
        def roles_emojis_admin_menu(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=roles_emojis_admin_menu, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the editrole command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the editrole command to restart the process.")
        else:
            await menu.remove_reaction(reaction.emoji, user)
            if str(reaction.emoji) == "0\u20e3":
                print("mew")
            elif str(reaction.emoji) == "1\u20e3":
                toeditTrue = []
                toeditFalse = ["administrator"]
                await editRolePermissions(ctx, menu, role, toeditTrue, toeditFalse)
                confirmation = await ctx.channel.send(':white_check_mark | Administrator permission removed from "'+role.name+'"')
                await self.rolesAdminMenu(ctx, menu, role)
                await asyncio.sleep(1)
                await confirmation.delete()
            elif str(reaction.emoji) == "2\u20e3":
                await self.rolesMainMenu(ctx, menu, role)
            elif str(reaction.emoji) == "❌":
                await ctx.channel.send(":white_check_mark: | Menu closed!")
                await menu.delete()



    async def rolesModMenu(self, ctx, menu, role):
        print("wew")

    async def rolesPubQuizMenu(self, ctx, menu, role):
        print("wew")

    async def rolesMiscMenu(self, ctx, menu, role):
        print("wew")

    async def rolesPresetMenu(self, ctx, menu, role):
        print("wew")

    async def editRolePermissions(self, ctx, menu, role, toeditTrue, toeditFalse):
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

    @roles.command(name="editrole", aliases=["edit"])
    async def editrole(self, ctx, *, roleName):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.channel.send(":no_entry: | Role not found.")
        else:
            query = "SELECT * FROM Roles WHERE roleID = $1"
            result = await ctx.bot.db.fetchrow(query, role.id)
            if result is None:
                connection = await self.bot.db.acquire()
                async with connection.transaction():
                    query = "INSERT INTO Roles (roleID, guildID) VALUES($1, $2) ON CONFLICT DO NOTHING"
                    await self.bot.db.execute(query, role.id, ctx.guild.id)
                await self.bot.db.release(connection)

            embed = discord.Embed(title="Menu Loading...", description="Please stand by.", colour=self.bot.getcolour())
            menu = await ctx.channel.send(embed = embed)
            emojis = useful.getMenuEmoji(10)
            for emoji in range(0,len(emojis)):
                await menu.add_reaction(emojis[emoji])
            await self.rolesMainMenu(ctx, menu, role)

    @roles.command()
    async def view(self, ctx, *, role):
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