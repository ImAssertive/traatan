import discord
from discord.ext import commands

def has_role(*arg):
    async def predicate(ctx):
        for counter in range (0,len(arg)):
            if discord.utils.get(ctx.guild.roles, name=str(arg[counter])) in ctx.author.roles:
                return True
        await ctx.channel.send(":no_good: You do not have permission for that!")
        return False
    return commands.check(predicate)

def justme():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401:
            return True
        else:
            await ctx.channel.send(":no_good: You do not have permission for that!")
            return False
    return commands.check(predicate)

def is_not_banned(bot):
    async def predicate(ctx, bot):
        bot.cur.execute("SELECT * FROM Users WHERE userID =? AND banned=0", (ctx.author.id,))
        if bot.cur.fetchone:
            return True
        return False
# def has_roleedit_permission(ctx):
#     async def predicate(ctx):
#         if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 163691476788838401 or
#
#
#     return commands.check(predicate)