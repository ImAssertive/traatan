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
        if ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
            return True
        else:
            await ctx.channel.send(":no_good: You do not have permission for that!")
            return False
    return commands.check(predicate)

def is_not_banned():
    async def predicate(ctx, bot):
        print(bot.test)
        query = "SELECT * FROM Users WHERE userID = $1 AND banned = 0"
        result = await bot.db.fetchrow(query, ctx.author.id)
        if result:
            query = "SELECT * FROM GuildUsers WHERE guildID = $1 AND userID = $2 AND banned = 0"
            result = await bot.db.fetchrow(query, ctx.guild.id, ctx.author.id)
            if result:
                query = "SELECT * FROM Guilds WHERE guildID = $1 AND banned = 0"
                result = await bot.db.fetchrow(query, ctx.guild.id)
                if result:
                    return True

        return False
    return commands.check(predicate)
