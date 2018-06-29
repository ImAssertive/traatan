import discord, asyncio, sys, traceback, checks, inflect, useful, emoji
from discord.ext import commands

class rolesCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=["role"])
    async def roles(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send(":no_entry: | Please enter a valid command. For a list of commands use: tt!roles help")


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
            embed = discord.Embed(title="Role "+ roleName + " loaded! Which Permissions would you like to edit?", description="Options:\n1: Admin\n2: Moderation\n3: Pub Quiz\n4: Miscellaneous\n5: Set role to preset permission level", colour=self.bot.getcolour())
            menu = await ctx.channel.send(embed = embed)
            emojis = useful.getMenuEmoji()
            for emoji in emojis:
                self.bot.add_reaction(menu, emoji=emojis[emoji])

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