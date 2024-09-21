import discord
from discord.ext import commands

async def user_has_role(ctx, role_names):
    """
    Checks if the user in the given context has any of the specified roles.

    Args:
        ctx: The command context.
        role_names: A list of role names to check for.

    Returns:
        True if the user has at least one of the roles, False otherwise.
    """
    for role_name in role_names:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role and role in ctx.author.roles:
            return True  # User has one of the roles
    return False  # User doesn't have any of the roles

async def _check_roles(ctx, role_names, has_role=True):
    for role_name in role_names:
        role = discord.utils.get(ctx.guild.roles, name=role_name)  # Search for role by name
        if role and role in ctx.author.roles:
            return has_role
    return not has_role
def has_role(*role_names):
    async def predicate(ctx):
        return await _check_roles(ctx, role_names, has_role=True)
    return commands.check(predicate)

def does_not_have_role(*role_names):
    async def predicate(ctx):
        return await _check_roles(ctx, role_names, has_role=False)
    return commands.check(predicate)

# Included as a baseline command as of latest d.py update
def justme():
    async def predicate(ctx):
        if ctx.author.id == 163691476788838401 or ctx.author.id == 463103145845850122:
            return True
        else:
            return False
    return commands.check(predicate)

def _check_quiz_status(is_active):
    async def predicate(ctx):
        query = "SELECT quiz_in_progress FROM guilds WHERE guild_id = $1"
        result = await ctx.bot.db.fetchrow(query, ctx.guild.id)
        return result["quiz_in_progress"] == is_active
    return commands.check(predicate)

def pubquiz_active():
    return _check_quiz_status(True)  # Check if quiz is active

def pubquiz_not_active():
    return _check_quiz_status(False)  # Check if quiz is not active