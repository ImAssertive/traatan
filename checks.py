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

def owner_or_rolepermission():
    async def predicate(ctx):
        if ctx.author.id == ctx.guild.owner_id:
            return True
         elif ctx.author.id == 163691476788838401 or ctx.author.id == 447089705691906048:
             return True
        else:
            rolesData = await getRolePerms(ctx)
            for role in rolesData:
                if role[2] == True:
                    return True
                elif role[3] == True:
                    return False
                elif role[23] == True:
                    return True
            return False
    return commands.check(predicate)

async def getRolePerms(ctx):
    roleIDs = []
    rolesdata = []
    for role in ctx.author.roles:
        roleIDs.append(role.id)
    for i in range(0, len(roleIDs)):
        query = "SELECT * FROM Roles WHERE roleID = $1"
        result = await ctx.bot.db.fetchrow(query, int(roleIDs[i]))
        rolesdata.append(result)
    return rolesdata


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

def rolescheck(command):
    async def predicate(ctx):
         if ctx.author.id == 163691476788838401:
             return True
        else:
            rolesData = await getRolePerms(ctx)
            print(role.index(command))
            for role in rolesData:
                if role[2] == True:
                    return True
                elif role[3] == True:
                    return False
                elif role[23] == True:
                    return True
            return False
    return commands.check(predicate)