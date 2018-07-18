cimport discord, asyncio, sys, traceback, checks, useful, random
from discord.ext import commands

class gamesCog:
    def __init__(self, bot):
        self.bot = bot

    #@commands.command(name="overwatch", aliases=['ow'])
    #async def overwatch(self, ctx, *, userInput):


def setup(bot):
    bot.add_cog(gamesCog(bot))