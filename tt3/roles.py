import discord, asyncio, sys, traceback, checks, inflect, useful
from discord.ext import commands

class rolesCog:
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(rolesCog(bot))