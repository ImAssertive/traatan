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
        results = yippi.search.post(keywords)
        if len(results) != 0:
            imageembed = discord.Embed(description="Tags: "+keywordsText,colour=self.bot.getcolour())
            imagetopost = random.randint(0, len(results))
            imageembed.set_image(url=results[imagetopost].file_url)
            embed.set_footer(text="Image "+imagetopost+" on e621 of "+str(len(results))+" results.")
            await ctx.channel.send(embed=imageembed)
        else:
           await ctx.channel.send(':no_entry: | No results found!')



def setup(bot):
    bot.add_cog(nsfwCog(bot))