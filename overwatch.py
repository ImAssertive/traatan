import discord, asyncio, sys, traceback, checks, useful
import sqlite3 as lite
from discord.ext import commands

class overwatchCog:
    def __init__(self, bot):
        self.bot = bot
        self.db = 'tt.db'

    @commands.command()
    @checks.has_role("Admin", "Moderator")
    async def dbtest(self, ctx):

def setup(bot):
    bot.add_cog(overwatchCog(bot))