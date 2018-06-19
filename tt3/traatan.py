import discord, asyncio, sys, traceback, checks, asyncpg, useful, credentialsFile
from discord.ext import commands

def getPrefix(bot, message):
    prefixes = ["tt!", "t!"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

async def run():
    description = "/r/Traa community help bot! tt!help for commands"
    credentials = credentialsFile.getCredentials()
    db = await asyncpg.create_pool(**credentials)
    await useful.createdb(db)
    bot = Bot(description=description, db=db)
    try:
        await bot.start(config.token)
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=getPrefix
        )

        self.db = kwargs.pop("db")

    async def on_ready(self):
        print('------')
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
loop = asyncio.get_event_loop()
loop.run_until_complete(run())