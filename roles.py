import discord, asyncio, sys, traceback, checks, inflect, useful
from discord.ext import commands

class rolesCog:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @checks.has_role("User")
    async def iam(self, ctx, *, roleName):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.channel.send(":no_entry: | Role not found.")
        else:
            query = "SELECT * FROM Roles WHERE roleID = $1"
            result = await ctx.bot.db.fetchrow(query, role.id)
            if result["selfassignable"] == True:
                if role in ctx.author.roles:
                    await ctx.channel.send(":no_entry: | You already have this role!")
                else:
                    await ctx.author.add_roles(role)
                    await ctx.channel.send(":white_check_mark: | **"+ctx.author.display_name+"** You now have the **" + role.name + "** role.")
            else:
                await ctx.channel.send(":no_entry: | This role is not self assignable!")

    @commands.command()
    @checks.has_role("User")
    async def iamnot(self, ctx, *, roleName):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.channel.send(":no_entry: | Role not found.")
        else:
            query = "SELECT * FROM Roles WHERE roleID = $1"
            result = await ctx.bot.db.fetchrow(query, role.id)
            if result["selfassignable"] == True:
                if role not in ctx.author.roles:
                    await ctx.channel.send(":no_entry: | You don't have this role!")
                else:
                    await ctx.author.remove_roles(role)
                    await ctx.channel.send(":white_check_mark: | **"+ctx.author.display_name+"** You no longer have the **" + role.name + "** role.")
            else:
                await ctx.channel.send(":no_entry: | This role is not self assignable!")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, *, member):
        muteRole = discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["Muted"])
        if muteRole in ctx.guild.get_member(memberID).roles:
            await ctx.channel.send(":no_entry: | This user is already muted. Use the unmute command to unmute them.")
        else:
            await ctx.guild.get_member(memberID).add_roles(muteRole)
            await ctx.channel.send(":white_check_mark: | Muted user **"+ctx.guild.get_member(memberID).display_name+"**.")
            await ctx.guild.get_member(memberID).remove_roles(discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["User"]))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, *, member):
        muteRole = discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["Muted"])
        if muteRole not in ctx.guild.get_member(memberID).roles:
            await ctx.channel.send(":no_entry: | This user is not muted. Use the mute command to mute them.")
        else:
            await ctx.guild.get_member(memberID).remove_roles(muteRole)
            await ctx.guild.get_member(memberID).add_roles(discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["User"]))
            await ctx.channel.send(":white_check_mark: | Unmuted user **" + ctx.guild.get_member(memberID).display_name + "**.")


def setup(bot):
    bot.add_cog(rolesCog(bot))
