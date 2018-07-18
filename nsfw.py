import discord, asyncio, sys, traceback, checks, useful, asyncpg, random, yippi
from discord.ext import commands

class nsfwCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="e621")
    @checks.module_enabled("nsfw")
    @checks.rolescheck("esix")
    async def e621(self, ctx, keywordsText):
        keywords = keywordsText.split(',')
        for counter in range(0, len(keywords)):
            keywords[counter] = keywords[counter].replace(' ', '%20')
        results = yippi.search.post(keywords, limit=5000)
        if len(results) != 0:
            imageembed = discord.Embed(colour=self.bot.getcolour())
            imagetopost = random.randint(0, len(results))
            imageembed.set_image(url=results[imagetopost].file_url)
            imageembed.set_footer(text="Image "+str(imagetopost)+" of "+str(len(results))+" results with tags: "+keywordsText+".")
            await ctx.channel.send(embed=imageembed)
        else:
           await ctx.channel.send(':no_entry: | No results found!')



def setup(bot):
    bot.add_cog(nsfwCog(bot))