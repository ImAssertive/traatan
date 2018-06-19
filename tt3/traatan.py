import discord, asyncio, sys, traceback, checks, useful, asyncpg
from discord.ext import commands


def getPrefix(bot, message):
    prefixes = ["tt!", "traa!"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = ['admin']
credFile = open("credentials.txt", "r")
credString = credFile.read()
credList = credString.split("\n")
credentials = credList[1]
db = await asyncpg.create_pool(**credentials)
useful.createdb(db)
bot = commands.Bot(command_prefix=getPrefix, description='/r/Traa community help bot! tt!help for more info')
bot.db = db

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension ' + extension, file=sys.stderr)
            traceback.print_exc()

bot.run(str(credList[0]))