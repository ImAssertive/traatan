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
        if ctx.author.id == 163691476788838401:
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

def owner_or_admin():
    async def predicate(ctx):
        if ctx.author.id == ctx.guild.owner_id:
            return True
        elif ctx.author.id == 163691476788838401:
            return True
        else:
            rolesData = await getRolePerms(ctx)
            for role in rolesData:
                if role["administrator"] == True:
                    return True
                elif role["muted"] == True:
                    return False

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



def module_enabled(module):
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401:
            return True
        else:
            query = "SELECT * FROM Guilds WHERE guildID = $1 AND "+module+" = true"
            result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
            if result:
                return True
        return False
    return commands.check(predicate)

def module_enabled_not_check(ctx, module):
    if ctx.author.id == 163691476788838401:
        return True
    else:
        query = "SELECT * FROM Guilds WHERE guildID = $1 AND " + module + " = true"
        result = await
        ctx.bot.db.fetchrow(query, ctx.guild.id)
        if result:
            return True
    return False

async def rolescheck_not_check(ctx, module):
    if ctx.author.id == 163691476788838401:
        return True
    else:
        rolesData = await getRolePerms(ctx)
        for role in rolesData:
            if role["administrator"] == True:
                return True
            elif role["muted"] == True:
                return False
            elif role[command] == True:
                return True
        return False

def rolescheck(command):
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401:
            return True
        else:
            rolesData = await getRolePerms(ctx)
            for role in rolesData:
                if role["administrator"] == True:
                    return True
                elif role["muted"] == True:
                    return False
                elif role[command] == True:
                    return True
            return False
    return commands.check(predicate)

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