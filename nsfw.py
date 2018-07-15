import discord, asyncio, sys, traceback, checks, useful, asyncpg, random, yippi
from discord.ext import commands


class nsfwCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nsfw")
    @checks.module_enabled("nsfw")
    async def e621(self, ctx, keywordsText):
        keywords = keywordsText.split(',')
        for counter in range(0, len(keywords)):
            keywords[counter] = keywords[counter].replace(' ', '%20')
        results = yippi.search.post(keywords)
        if len(results) != 0:
            imagetopost = random.randint(0, len(results))
            await ctx.send(results[imagetopost].file_url)
        else:
           await ctx.channel.send(':no_entry: | No results found!')



def setup(bot):
    bot.add_cog(nsfwCog(bot))