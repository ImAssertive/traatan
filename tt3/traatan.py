import discord, asyncio, sys, traceback, checks, asyncpg, useful, credentialsFile
from discord.ext import commands

def getPrefix(bot, message):
    prefixes = ["tt!", "t!"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

async def run():
    description = "/r/Traa community help bot! tt!help for commands"
    credentials = credentialsFile.getCredentials()
    db = await asyncpg.create_pool(**credentials)
    await db.execute('''CREATE TABLE IF NOT EXISTS Users(userID bigint PRIMARY KEY,
    pubquizDM boolean DEFAULT false,
    banned boolean DEFAULT false);''') #Users

    await db.execute('''CREATE TABLE IF NOT EXISTS Guilds(guildID bigint PRIMARY KEY,
    overwatchEnabled boolean DEFAULT true,
    pubquizEnabled boolean DEFAULT true,
    bluetextEnabled boolean DEFAULT true,
    welcomeEnabled boolean DEFAULT false,
    welcomeChannel bigint,
    welcomeText text,
    leaveEnabled boolean DEFAULT false,
    leaveChannel bigint,
    leaveText text,
    adminEnabled boolean DEFAULT true,
    banned boolean DEFAULT false);''') #Guild

    await db.execute('''CREATE TABLE IF NOT EXISTS Games(gameID serial PRIMARY KEY,
    gameName text,
    gameReleaseDate text,
    gamePublisher text,
    gameDescription text);''')#Games

    await db.execute('''CREATE TABLE IF NOT EXISTS Roles(roleID bigint PRIMARY KEY,
    guildID bigint references Guilds(guildID),
    administrator boolean DEFAULT false,
    pqStart boolean DEFAULT false,
    pqEnd boolean DEFAULT false,
    pqQuestion boolean DEFAULT false,
    pqSuperQuestion boolean DEFAULT false,
    pqOverride boolean DEFAULT false,
    pqSetTime boolean DEFAULT false,
    pqJoin boolean DEFAULT true,
    pqHelp boolean DEFAULT true,
    pqQMHelp boolean DEFAULT false,
    bt boolean DEFAULT true,
    btc boolean DEFAULT true,
    setWelcomeChannel boolean DEFAULT false,
    setWelcomeText boolean DEFAULT false,
    setLeaveChannel boolean DEFAULT false,
    setLeaveText boolean DEFAULT false,
    toggleRaid boolean DEFAULT false,
    setRaidRole boolean DEFAULT false,
    setRaidText boolean DEFAULT false,
    mute boolean DEFAULT false,
    cute boolean DEFAULT true, 
    setMuteRole boolean DEFAULT false);
    ''')#Roles

    await db.execute('''CREATE TABLE IF NOT EXISTS GuildUsers(userID bigint references Users(userID),
    guildID bigint references Guilds(guildID),
    pubquizScoreTotal integer DEFAULT 0,
    pubquizScoreWeekly integer DEFAULT 0,
    banned boolean DEFAULT false,
    PRIMARY KEY(userID, guildID));''')

    await db.execute('''CREATE TABLE IF NOT EXISTS UserGameAccounts(accountID serial PRIMARY KEY,
    userID bigint references Users(userID),
    gameID serial references Games(gameID),
    accountRank text,
    accountName text,
    accountRegion text,
    accountPublic boolean DEFAULT true,
    accountInfo text,
    accountPlatform text);''') #UserGameAccounts    bot = Bot(description=description, db=db)
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