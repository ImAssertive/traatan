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

    async def rolesMainMenu(self, ctx, menu, roleName):
        embed = discord.Embed(title='Role "' + roleName + '"loaded. Which Permissions would you like to edit?', description="Options:\n1: Admin\n2: Moderation\n3: Pub Quiz\n4: Miscellaneous\n5: Set role to preset permission level\nx: Closes Menu", colour=self.bot.getcolour())
        await menu.edit(embed=embed)
        options = ["1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3", "5\u20e3", "6\u20e3", "7\u20e3","8\u20e3", "9\u20e3", "\U0001f51f"]
        def roles_emojis1(reaction, user):
            return (user == ctx.author) and (str(reaction.emoji) in options)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=roles_emojis1, timeout=60.0)
        except asyncio.TimeoutError:
            try:
                await ctx.channel.send(":no_entry: | **" + ctx.author.nick + "** The command menu has closed due to inactivity. Please reuse the editrole command to restart the process.")
            except TypeError:
                await ctx.channel.send(":no_entry: | **" + ctx.author.name + "** The command menu has closed due to inactivity. Please reuse the editrole command to restart the process.")
        else:
            if str(reaction.emoji) == "1\u20e3":
                menu.remove_reaction(reaction.emoji, user)
                print("test")
            elif str(reaction.emoji) == "2\u20e3":
                print("te")
            elif str(reaction.emoji) == "3\u20e3":
                print("q")
            elif str(reaction.emoji) == "4\u20e3":
                print("q")
            elif str(reaction.emoji) == "5\u20e3":
                print("q")
            elif str(reaction.emoji) == "\U0001f51f":
                print("q")



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
            emojis = useful.getMenuEmoji(5)
            for emoji in range(0,len(emojis)):
                await menu.add_reaction(emojis[emoji])
            await self.rolesMainMenu(ctx, menu, roleName)

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