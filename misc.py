import discord, asyncio, sys, traceback, checks, inflect, useful
from discord.ext import commands

class miscCog:
    def __init__(self, bot):
        self.bot = bot
        self.welcomeChannel = 0
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
    async def bluetext(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText)
        await ctx.channel.send(toOutput)
        if self.deleteBlueText:
            await ctx.message.delete()

    @commands.command(name="bluetextcode", aliases=['bluetextmarkup', 'btc', 'btmu'])
    async def bluetextcode(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText)
        await ctx.channel.send("Here's your code:")
        await ctx.channel.send("```" + toOutput + "```")
        if self.deleteBlueText:
            await ctx.message.delete()

    @commands.command()
    async def cute(self, ctx, member):
        memberID = useful.getid(member)
        try:
            toOutput = self.blueTextFunction(ctx.guild.get_member(memberID).nick +" is cute af and i wuv them")
        except TypeError:
            toOutput = self.blueTextFunction(ctx.guild.get_member(memberID).name +" is cute af and i wuv them")
        await ctx.channel.send(toOutput)
        if self.deleteBlueText:
            await ctx.message.delete()

    @commands.command(name="togglebluetextdelete", aliases=['deletebluetext', 'tbtd'])
    @checks.has_role("Admin", "Moderator")
    async def toggleBlueTextDelete(self, ctx):
        self.deleteBlueText = not self.deleteBlueText
        if self.deleteBlueText:
            await ctx.channel.send(":white_check_mark: Hiding bluetext commands!")
        else:
            await ctx.channel.send(":white_check_mark: No longer hiding bluetext commands!")


def setup(bot):
    bot.add_cog(miscCog(bot))