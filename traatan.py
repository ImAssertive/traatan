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
    banned boolean DEFAULT false);
    
    CREATE TABLE IF NOT EXISTS Guilds(guildID bigint PRIMARY KEY,
    prefix text,
    games boolean DEFAULT true,
    pubquiz boolean DEFAULT true,
    pubquiztime smallint DEFAULT 10, 
    ongoingpubquiz boolean DEFAULT false,
    pubquiztext text,
    pubquizendtext text,
    pubquizchannel bigint,
    pubquizquestionuserid bigint,
    pubquizquestionnumber integer DEFAULT 0,
    pubquizquestionactive boolean DEFAULT false,
    pubquizlastquestionsuper boolean DEFAULT false,
    bluetext boolean DEFAULT true,
    misc boolean DEFAULT true,
    NSFW boolean DEFAULT false,
    welcome boolean DEFAULT false,
    welcomeChannel bigint,
    welcomeText text,
    leave boolean DEFAULT false,
    leaveChannel bigint,
    leaveText text,
    administrator boolean DEFAULT true,
    banned boolean DEFAULT false);
    
    
    CREATE TABLE IF NOT EXISTS Games(gameID serial PRIMARY KEY,
    gameName text,
    gameReleaseDate text,
    gamePublisher text,
    gameDescription text);
    
    CREATE TABLE IF NOT EXISTS Roles(roleID bigint PRIMARY KEY,
    guildID bigint references Guilds(guildID) ON DELETE CASCADE ON UPDATE CASCADE,
    administrator boolean DEFAULT false,
    muted boolean DEFAULT false,
    pqStart boolean DEFAULT false,
    pqEnd boolean DEFAULT false,
    pqQuestion boolean DEFAULT false,
    pqSuperQuestion boolean DEFAULT false,
    pqOverride boolean DEFAULT false,
    pqSetTime boolean DEFAULT false,
    pqJoin boolean DEFAULT true,
    pqQMHelp boolean DEFAULT false,
    pqsettext boolean DEFAULT false,
    pqleaderboard boolean DEFAULT false,
    pqcorrect boolean DEFAULT false,
    pqanswer boolean DEFAULT false,
    bluetext boolean DEFAULT true,
    bluetextcode boolean DEFAULT true,
    setWelcomeChannel boolean DEFAULT false,
    setWelcomeText boolean DEFAULT false,
    setLeaveChannel boolean DEFAULT false,
    setLeaveText boolean DEFAULT false,
    toggleRaid boolean DEFAULT false,
    setRaidRole boolean DEFAULT false,
    setRaidText boolean DEFAULT false,
    mute boolean DEFAULT false,
    cute boolean DEFAULT true,
    conch boolean DEFAULT true,
    eightball boolean DEFAULT true, 
    setMuteRole boolean DEFAULT false,
    selfAssignable boolean DEFAULT false);
    
    CREATE TABLE IF NOT EXISTS GuildUsers(userID bigint references Users(userID) ON DELETE CASCADE ON UPDATE CASCADE,
    guildID bigint references Guilds(guildID) ON DELETE CASCADE ON UPDATE CASCADE,
    pubquizScoreTotal integer DEFAULT 0,
    pubquizScoreWeekly integer DEFAULT 0,
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
    initial_extensions = ['admin', 'setup', 'misc', 'roles', 'pubquiz']
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

        self.pubquizAnswers = []
        self.db = kwargs.pop("db")
        self.currentColour = -1
        self.outcomes = ["It is certain", "It is decidedly so", "Without a doubt", "Yes - definitely",
                    "You may rely on it",
                    "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes",
                    "Reply hazy, try again", "Ask again later", "Better not tell you now",
                    "Cannot predict now", "Concentrate and ask again", "Don't count on it",
                    "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

    async def on_ready(self):
        print("Username: {0}\nID: {0.id}".format(self.user))
        game = discord.Game("chess with Rainbow Restarter!")
        await self.change_presence(status=discord.Status.online, activity=game)

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