import discord, asyncio, sys, traceback, checks, asyncpg, useful, credentialsFile
from discord.ext import commands

def getPrefix(bot, message):
    prefixes = ["traa!"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

async def run():
    description = "/r/Traa community help bot! tt!help for commands"
    credentials = credentialsFile.getCredentials()
    db = await asyncpg.create_pool(**credentials)
    await db.execute('''CREATE TABLE IF NOT EXISTS Users(userID bigint PRIMARY KEY,
    pubquizDM boolean DEFAULT false,
    banned boolean DEFAULT false);
    
    CREATE TABLE IF NOT EXISTS Guilds(guildID bigint PRIMARY KEY,
    gamesEnabled boolean DEFAULT true,
    pubquizEnabled boolean DEFAULT true,
    bluetextEnabled boolean DEFAULT true,
    welcomeEnabled boolean DEFAULT false,
    welcomeChannel bigint,
    welcomeText text,
    leaveEnabled boolean DEFAULT false,
    leaveChannel bigint,
    leaveText text,
    adminEnabled boolean DEFAULT true,
    banned boolean DEFAULT false);
    
    
    CREATE TABLE IF NOT EXISTS Games(gameID serial PRIMARY KEY,
    gameName text,
    gameReleaseDate text,
    gamePublisher text,
    gameDescription text);
    
    CREATE TABLE IF NOT EXISTS Roles(roleID bigint PRIMARY KEY,
    guildID bigint references Guilds(guildID) ON DELETE CASCADE ON UPDATE CASCADE,
    administrator boolean DEFAULT false,
    pqStart boolean DEFAULT false,
    pqEnd boolean DEFAULT false,
    pqQuestion boolean DEFAULT false,
    pqSuperQuestion boolean DEFAULT false,
    pqOverride boolean DEFAULT false,
    pqSetTime boolean DEFAULT false,
    pqJoin boolean DEFAULT true,
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
    
    CREATE TABLE IF NOT EXISTS GuildUsers(userID bigint references Users(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    guildID bigint references Guilds(guildID) ON DELETE CASCADE ON UPDATE CASCADE,
    pubquizScoreTotal integer DEFAULT 0,
    pubquizScoreWeekly integer DEFAULT 0,
    banned boolean DEFAULT false,
    PRIMARY KEY(userID, guildID));
    
    CREATE TABLE IF NOT EXISTS UserGameAccounts(accountID serial PRIMARY KEY,
    userID bigint references Users(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    gameID serial references Games(gameID) ON DELETE CASCADE ON UPDATE CASCADE,
    accountRank text,
    accountName text,
    accountRegion text,
    accountPublic boolean DEFAULT true,
    accountInfo text,
    accountPlatform text);''')
    bot = Bot(description=description, db=db)
    bot.test = "test"
    initial_extensions = ['admin', 'setup', 'misc', 'roles2']
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print('Failed to load extension ' + extension, file=sys.stderr)
                traceback.print_exc()

    try:
        await bot.start(credentialsFile.getToken())
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
        self.currentColour = -1

    async def on_ready(self):
        print("Username: {0}\nID: {0.id}".format(self.user))

    def getcolour(self):
        colours = ["5C6BC0", "AB47BC", "EF5350", "FFA726", "FFEE58", "66BB6A", "5BCEFA", "F5A9B8", "FFFFFF", "F5A9B8", "5BCEFA"]
        self.currentColour += 1
        if self.currentColour ==  len(colours) - 1:
            self.currentColour = 0
        return discord.Colour(int(colours[self.currentColour], 16))

    def conchcolour(self, number):
        if number < 10 and number > -1:
            return discord.Colour(int("00FF00", 16))
        elif number > 9 and number < 15:
            return discord.Colour(int("FFFF00", 16))
        else:
            return discord.Colour(int("FF0000", 16))


loop = asyncio.get_event_loop()
loop.run_until_complete(run())