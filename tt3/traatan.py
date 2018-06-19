import discord, asyncio, sys, traceback, checks
from discord.ext import commands

initial_extensions = ['admin']


def getPrefix(bot, message):
    prefixes = ["tt!", "traa!"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

async def run():
    credFile = open("credentials.txt", "r")
    credString = credFile.read()
    credList = credString.split("\n")
    credentials = eval(credList[1])
    db = await asyncpg.create_pool(**credentials)
    bot = commands.Bot(command_prefix=getPrefix, pm_help=False, description='/r/Traa community help bot! tt!help for commands', db=db)
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print('Failed to load extension ' + extension, file=sys.stderr)
                traceback.print_exc()
    try:
        bot.run(str(credList[0]))
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()


@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')



bot.run(str(credList[0]))