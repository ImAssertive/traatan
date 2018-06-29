import discord, asyncio, sys, traceback, checks, inflect, useful, random
from discord.ext import commands

class miscCog:
    def __init__(self, bot):
        self.bot = bot
        self.deleteBlueText = False

    def blueTextFunction(self, userText, spaces):
        blueText = ""
        for counter in range(0,len(userText)):
            if userText[counter].isalpha() and spaces == True:
                blueText += ":regional_indicator_" + userText[counter].lower() + ": "
            elif userText[counter].isalpha() and spaces == False:
                blueText += ":regional_indicator_" + userText[counter].lower() + ":"
            elif userText[counter].isdigit():
                blueText += ":" + inflect.engine().number_to_words(userText[counter]) + ":"
            else:
                blueText += userText[counter]
        return blueText

    @commands.command(name="bluetext", aliases=['bt'])
    @checks.is_not_banned()
    @checks.bluetext_enabled()
    async def bluetext(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText, False)
        await ctx.channel.send(toOutput)
        if self.deleteBlueText:
            await ctx.message.delete()

    @commands.command(name="bluetextcode", aliases=['bluetextmarkup', 'btc', 'btmu'])
    @checks.is_not_banned()
    @checks.bluetext_enabled()
    async def bluetextcode(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText, True)
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
            toOutput = self.blueTextFunction((ctx.guild.get_member(memberID).nick +" is cute and valid and i love them"), False)
        except TypeError:
            toOutput = self.blueTextFunction((ctx.guild.get_member(memberID).name +" is cute and valid and i love them"), False)
        await ctx.channel.send(toOutput + ":heartpulse:")
        if self.deleteBlueText and ctx.author.id == 163691476788838401:
            await ctx.message.delete()

    @commands.command(name="togglebluetextdelete", aliases=['deletebluetext', 'tbtd'], hidden = True)
    @checks.justme()
    async def toggleBlueTextDelete(self, ctx):
        self.deleteBlueText = not self.deleteBlueText
        if self.deleteBlueText:
            await ctx.channel.send(":white_check_mark: | Hiding bluetext commands!")
        else:
            await ctx.channel.send(":white_check_mark: | No longer hiding bluetext commands!")

    @commands.command()
    async def conch(self, ctx):
        outcomes = ["It is certain", "It is decidedly so", "Without a doubt", "Yes - definitely", "You may rely on it",
                    "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes",
                    "Reply hazy, try again", "Ask again later", "Better not tell you now",
                    "Cannot predict now", "Concentrate and ask again", "Don't count on it",
                    "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]
        randomNumber = random.randint(0,19)
        toOutput = ("**" ctx.author.name + "** | The conch says:")
        embed = discord.Embed(colour=self.bot.getcolour())
        embed.add_field(name=toOutput, value = outcomes[randomNumber])
        embed.set_thumbnail("https://media1.tenor.com/images/0181e2d7787313c7de0b8acab72dde7f/tenor.gif?itemid=3541653")
        embed.set_footer(text="THE SHELL HAS SPOKEN")

def setup(bot):
    bot.add_cog(miscCog(bot))