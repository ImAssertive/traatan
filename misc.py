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
    @checks.module_enabled("bluetext")
    @checks.rolescheck("bluetext")
    async def bluetext(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText, False)
        await ctx.channel.send(toOutput)
        if self.deleteBlueText:
            await ctx.message.delete()

    @commands.command(name="bluetextcode", aliases=['bluetextmarkup', 'btc', 'btmu'])
    @checks.is_not_banned()
    @checks.module_enabled("bluetext")
    @checks.rolescheck("bluetextcode")
    async def bluetextcode(self, ctx, *, userText):
        toOutput = self.blueTextFunction(userText, True)
        await ctx.channel.send("Here's your code:")
        await ctx.channel.send("```" + toOutput + "```")
        if self.deleteBlueText and ctx.author.id == 163691476788838401:
            await ctx.message.delete()

    @commands.command()
    @checks.is_not_banned()
    @checks.module_enabled("bluetext")
    @checks.rolescheck("cute")
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

    @commands.command(name="conch", aliases=['shell'])
    @checks.rolescheck("conch")
    @checks.module_enabled("misc")
    async def conch(self, ctx):
        randomNumber = random.randint(0,19)
        conchName = ("**" +ctx.author.name + "** | The conch says:")
        conchValue = ('"'+self.bot.outcomes[randomNumber]+ '."')
        embed = discord.Embed(colour=self.bot.conchcolour(randomNumber))
        embed.add_field(name=conchName, value = conchValue)
        embed.set_image(url="https://media1.tenor.com/images/0181e2d7787313c7de0b8acab72dde7f/tenor.gif?itemid=3541653")
        embed.set_footer(text="THE SHELL HAS SPOKEN")
        await ctx.channel.send(embed = embed)

    @commands.command(name="eightball", aliases=['8ball'])
    @checks.module_enabled("misc")
    @checks.rolescheck("eightball")
    async def eightball(self, ctx):
        randomNumber = random.randint(0, 19)
        eightballName = ("**" + ctx.author.name + "** - The 8ball says:")
        eightballValue = ('"' + self.bot.outcomes[randomNumber] + '."')
        await ctx.channel.send(":8ball: | "+eightballName + " " + eightballValue)

    @commands.command(name="roll")
    @checks.module_enabled("misc")
    async def roll(self, ctx, diceCommand):
        diceCommand = diceCommand.lower()
        diceCommand = diceCommand.split("d")
        if len(diceCommand) != 2:
            await ctx.channel.send(":no_entry: | Incorrect command usage. Correct usage is `traa!roll 1d20`")
            print(diceCommand + " 1")
        else:
            succeeded = 1
            try:
                throws = int(diceCommand[0])
            except:
                await ctx.channel.send(":no_entry: | Incorrect command usage. Correct usage is `traa!roll 1d20`")
                print("2")
                succeeded = 0
            try:
                repeats = int(diceCommand[1])
            except:
                await ctx.channel.send(":no_entry: | Incorrect command usage. Correct usage is `traa!roll 1d20`")
                print("3")
                succeeded = 0
            if succeeded == 1:
                if throws > 0 and throws < 100001 and repeats > 0 and repeats < 101:
                    total = 0
                    toOutput = []
                    for counter in range (0,repeats):
                        rollresult = random.randint(0,throws)
                        total = toal + rollresult
                        toOutput.append(rollresult)
                    toOutput = ', '.join(toOutput)
                    if throws == 1:
                        await ctx.channel.send(":game_die: | Rolling **" + str(repeats)+" "+str(throws)+"**sided die... You rolled: **" + str(toOutput) + "** for a total of: **" +total+"**.")

                    else:
                        await ctx.channel.send(":game_die: | Rolling **" + str(repeats)+" "+str(throws)+"**sided dice... You rolled: **" + str(toOutput) + "** for a total of: **" +total+"**.")
                elif repeats > 0 and repeats < 101:
                    await ctx.channel.send(":no_entry: | You can only throw between 1 and 100 dice at a time.")
                elif throws > 0 and throws < 100001:
                    await ctx.channel.send(":no_entry: | You can only throw dice with between 1 and 100000 sides.")
                else:
                    await ctx.channel.send(":no_entry: | Incorrect command usage. Correct usage is `traa!roll 1d20`")
                    print("4")


def setup(bot):
    bot.add_cog(miscCog(bot))