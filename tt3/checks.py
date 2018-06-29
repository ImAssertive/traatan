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
        await ctx.channel.send(":no_good: Bluetext commands are not enabled here!")
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
        await ctx.channel.send(":no_good: Pubquiz commands are not enabled here!")
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
        await ctx.channel.send(":no_good: Welcome commands are not enabled here!")
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
        await ctx.channel.send(":no_good: Farewell commands are not enabled here!")
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
        await ctx.channel.send(":no_good: Admin commands are not enabled here!")
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
        await ctx.channel.send(":no_good: Games commands are not enabled here!")
        return False
    return commands.check(predicate)

def setup_options1(ctx):
    return (ctx.content.lower() in ["info", "yes", "no", "skip"]) and ctx.guild != None

def roles_options1(ctx):
    return (ctx.content.lower() in ["admin", "moderator", "quizmaster", "muted", "custom", "close", "quiz master"]) and ctx.guild != None

def roles_options2(ctx):
    print (ctx.content.lower() in ["enabled", "disabled", "enable", "disable", "true", "false", "info", "skip", "yes", "no", "close"]) and ctx.guild != None
    return (ctx.content.lower() in ["enabled", "disabled", "enable", "disable", "true", "false", "info", "skip", "yes", "no", "close"]) and ctx.guild != None

def roles_emojis1(ctx, reaction):
    return str(ctx.emoji) in ["1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3", "5\u20e3", "6\u20e3", "7\u20e3", "8\u20e3", "9\u20e3", "\U0001f51f"]
