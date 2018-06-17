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
