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
    async def mute(self, ctx, member, time=None):
        print(member)
        print(time)
        memberID = useful.getid(member)
        muteRole = discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["Muted"])
        if time:
            await self.muteFunction(ctx, memberID)
            await asyncio.sleep(int(time)*60)
            await self.unmuteFunction(ctx, memberID)
        else:
            await self.muteFunction(ctx, memberID)



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member, time=None):
        memberID = useful.getid(member)
        if time:
            await self.unmuteFunction(ctx, memberID)
            await asyncio.sleep(time*60)
            await self.muteFunction(ctx, memberID)
        else:
            await self.unmuteFunction(ctx, memberID)

    async def muteFunction(self, ctx, memberID):
        muteRole = discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["Muted"])
        if muteRole in ctx.guild.get_member(memberID).roles:
            await ctx.channel.send(":no_entry: | This user is already muted. Use the unmute command to unmute them.")
            break
        else:
            await ctx.guild.get_member(memberID).add_roles(muteRole)
            await ctx.channel.send(":white_check_mark: | Muted user **" + ctx.guild.get_member(memberID).display_name + "** `"+str(ctx.guild.get_member(memberID).id)+"`")

    async def unmuteFunction(self, ctx, memberID):
        muteRole = discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["Muted"])
        if muteRole not in ctx.guild.get_member(memberID).roles:
            await ctx.channel.send(":no_entry: | This user is unmuted.")
            break
        else:
            await ctx.guild.get_member(memberID).remove_roles(muteRole)
            await ctx.guild.get_member(memberID).add_roles(discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict["User"]))
            await ctx.channel.send(":white_check_mark: | Unmuted user **" + ctx.guild.get_member(memberID).display_name + "** `"+str(ctx.guild.get_member(memberID).id)+"`")




    @commands.command()
    @checks.has_role("Helper Powers", "Moderator Powers","Admin Powers", "Bot Tinkerer")
    async def viewrole(self, ctx, *, roleName):
        role = discord.utils.get(ctx.guild.roles, name=roleName)
        if role is None:
            await ctx.channel.send(":no_entry: | Role not found.")
        else:
            embed = discord.Embed(title="Info for role: "+roleName+"", colour = discord.Colour(role.colour.value))
            embed.add_field(name="ID", value=str(role.id), inline=False)
            embed.add_field(name="Created", value=str(role.created_at), inline=False)
            embed.add_field(name="Members", value=str(len(role.members)), inline=False)
            embed.add_field(name="Colour", value=str(hex(role.colour.value)), inline=False)
            embed.add_field(name="Displayed separately (Hoisted)", value=str(role.hoist), inline=False)
            embed.add_field(name="Externally managed", value=str(role.managed), inline=False)
            embed.add_field(name="Position", value=str(role.position)+" of "+str(len(ctx.guild.roles)-1)+" roles.", inline=False)
            embed.add_field(name="Mentionable", value=str(role.mentionable), inline=False)
            embed.add_field(name="Created at", value=str(role.created_at), inline=False)
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(rolesCog(bot))
