import discord, asyncio, sys, traceback, checks, inflect, useful
from discord.ext import commands

class miscCog:
    def __init__(self, bot):
        self.bot = bot
        self.deleteBlueText = False

    def blueTextFunction(self, userText):
        blueText = ""
        for counter in range(0,len(userText)):
            if userText[counter].isalpha():
                blueText += ":regional_indicator_" + userText[counter].lower() + ": "
            elif userText[counter].isdigit():
                blueText += ":" + inflect.engine().number_to_words(userText[counter]) + ":"
            else:
                blueText += userText[counter]
        return blueText

    @commands.command(name="bluetext", aliases=['bt'])
    @checks.is_not_banned()
    @checks.bluetext_enabled()
    async def bluetext(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText)
        await ctx.channel.send(toOutput)
        if self.deleteBlueText:
            await ctx.message.delete()

    @commands.command(name="bluetextcode", aliases=['bluetextmarkup', 'btc', 'btmu'])
    @checks.is_not_banned()
    @checks.bluetext_enabled()
    async def bluetextcode(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText)
        await ctx.channel.send("Here's your code:")
        await ctx.channel.send("```" + toOutput + "```")
        if self.deleteBlueText and ctx.author.id == 163691476788838401:
            await ctx.message.delete()

    @commands.command()
    @checks.is_not_banned()
    @checks.bluetext_enabled()
    async def cute(self, ctx, member):
        memberID = useful.getid(member)
        try:
            toOutput = self.blueTextFunction(ctx.guild.get_member(memberID).nick +" is cute and valid and i love them")
        except TypeError:
            toOutput = self.blueTextFunction(ctx.guild.get_member(memberID).name +" is cute and valid and i love them")
        await ctx.channel.send(toOutput + ":heartpulse:")
        if self.deleteBlueText and ctx.author.id == 163691476788838401:
            await ctx.message.delete()

    @commands.command(name="togglebluetextdelete", aliases=['deletebluetext', 'tbtd'])
    @checks.justme()
    async def toggleBlueTextDelete(self, ctx):
        self.deleteBlueText = not self.deleteBlueText
        if self.deleteBlueText:
            await ctx.channel.send(":white_check_mark: | Hiding bluetext commands!")
        else:
            await ctx.channel.send(":white_check_mark: | No longer hiding bluetext commands!")


def setup(bot):
    bot.add_cog(miscCog(bot))