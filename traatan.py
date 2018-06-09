import discord, asyncio, sys, traceback, checks
from discord.ext import commands

initial_extensions = ['pubquiz', 'misc']


def getPrefix(bot, message):
    prefixes = ["tt!", "t!"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

def gettoken():
    tokenfile = open("token.txt", "r")
    tokenstring = tokenfile.read()
    tokentoken = tokenstring.split("\n")
    token = str(tokentoken[0])
    return token
token = gettoken()

bot = commands.Bot(command_prefix=getPrefix, pm_help=False, description='/r/Traa community help bot! tt!help for commands')

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension ' + extension, file=sys.stderr)
            traceback.print_exc()



@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(token)