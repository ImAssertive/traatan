import discord
from discord.ext import commands

def has_role(*arg):
    async def predicate(ctx):
        for counter in range (0,len(arg)):
            print(ctx.bot.rolesDict[arg[counter]])
            print(discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict[arg[counter]]) in ctx.author.roles)
            print(discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict[arg[counter]]))
            if discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict[arg[counter]]) in ctx.author.roles:
                return True
        return False
    return commands.check(predicate)

def justme():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 463103145845850122:
            return True
        else:
            return False
    return commands.check(predicate)

async def has_role_not_check(ctx, *arg):
    for counter in range(0, len(arg)):
        if discord.utils.get(ctx.guild.roles, id=ctx.bot.rolesDict[arg[counter]]) in ctx.author.roles:
            return True
    return False


def pubquiz_active():
    async def predicate(ctx):
        query = "SELECT * FROM Guilds WHERE guildID = $1 AND ongoingpubquiz = true"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            return True
        else:
            return False
    return commands.check(predicate)

def pubquiz_not_active():
    async def predicate(ctx):
        query = "SELECT * FROM Guilds WHERE guildID = $1 AND ongoingpubquiz = false"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            return True
        else:
            return False
    return commands.check(predicate)