import discord
from discord.ext import commands

def has_role(*arg):
    async def predicate(ctx):
        for counter in range (0,len(arg)):
            if discord.utils.get(ctx.guild.roles, name=str(arg[counter])) in ctx.author.roles:
                return True
        return False
    return commands.check(predicate)

def justme():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
            return True
        else:
            return False
    return commands.check(predicate)

def is_not_banned():
    async def predicate(ctx):
        query = "SELECT * FROM Users WHERE userID = $1 AND banned = false"
        result = await ctx.bot.db.fetchrow(query, ctx.author.id)
        if result:
            query = "SELECT * FROM GuildUsers WHERE guildID = $1 AND userID = $2 AND banned = false"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id, ctx.author.id)
            if result:
                query = "SELECT * FROM Guilds WHERE guildID = $1 AND banned = false"
                result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
                if result:
                    return True
        return False
    return commands.check(predicate)

def bluetext_enabled():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
            return True
        else:
            query = "SELECT * FROM Guilds WHERE guildID = $1 AND blueTextEnabled = true"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            if result:
                return True
        return False
    return commands.check(predicate)

def pubquiz_enabled():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
            return True
        else:
            query = "SELECT * FROM Guilds WHERE guildID = $1 AND pubquizEnabled = true"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            if result:
                return True
        return False
    return commands.check(predicate)

def welcome_enabled():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
            return True
        else:
            query = "SELECT * FROM Guilds WHERE guildID = $1 AND welcomeEnabled = true"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            if result:
                return True
        return False
    return commands.check(predicate)

def leave_enabled():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
            return True
        else:
            query = "SELECT * FROM Guilds WHERE guildID = $1 AND leaveEnabled = true"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            if result:
                return True
        return False
    return commands.check(predicate)

def admin_enabled():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
            return True
        else:
            query = "SELECT * FROM Guilds WHERE guildID = $1 AND adminEnabled = true"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            if result:
                return True
        return False
    return commands.check(predicate)

def games_enabled():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
            return True
        else:
            query = "SELECT * FROM Guilds WHERE guildID = $1 AND gamesEnabled = true"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            if result:
                return True
        return False
    return commands.check(predicate)

