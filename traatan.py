import discord, asyncio, sys, traceback, checks, asyncpg, useful, credentialsFileDev
from discord.ext import commands

def getPrefix(bot, message):
    prefixes = ["traa!","valtarithegreat!","tt!","tt?"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

async def run():
    description = "Super Gay Bot"
    credentials = credentialsFileDev.getCredentials()
    db = await asyncpg.create_pool(**credentials) ##CAPITALS ARE NOT CARRIED OVER ON DATABASE CREATION SO ARNT INCLUDED TO REDUCE CONFUSION
    await db.execute('''CREATE TABLE IF NOT EXISTS Users(userID bigint PRIMARY KEY,
    pubquizScoreTotal integer DEFAULT 0,
    pubquizScoreWeekly integer DEFAULT 0,
    totalWarnings integer DEFAULT 0,
    verificationmessage text,
    verificationEnabled boolean DEFAULT false);
    
    CREATE TABLE IF NOT EXISTS Guilds(guildID bigint PRIMARY KEY,
    muteroleid bigint,
    kicktext text,
    bantext text,
    pubquiztime smallint DEFAULT 10, 
    ongoingpubquiz boolean DEFAULT false,
    pubquiztext text,
    pubquizendtext text,
    pubquizchannel bigint,
    pubquizquestionnumber integer DEFAULT 0,
    pubquizquestionactive boolean DEFAULT false,
    pubquizlastquestionsuper boolean DEFAULT false,
    welcome boolean DEFAULT false,
    welcomeChannel bigint,
    welcomeText text,
    leave boolean DEFAULT false,
    leaveChannel bigint,
    leaveText text);

    CREATE TABLE IF NOT EXISTS Roles(roleID bigint PRIMARY KEY,
    selfAssignable boolean DEFAULT false);''')
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
        await bot.start(credentialsFileDev.getToken())
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
        self.rolesDict = {"Admin": 348608087793467412, "Admin Powers": 406091590923321355,
                        "Helper": 395565792457916417, "Helper Powers": 395565792457916417,
                        "Owner": 348207687319683072,
                        "Moderator Powers": 388829460759052288, "Moderator": 348747695088730113,
                        "User": 348208233254617110,
                        "Quizmaster": 449941007619063828,
                        "Muted": 356529701675859990,
                        "Bot Tinkerer": 504059432238579712}
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
        query = "SELECT * FROM Guilds WHERE guildID = $1"
        serverID = 331517548636143626
        result = await self.db.fetchrow(query, serverID)
        if result["ongoingpubquiz"]:
            self.pubquizActive = True
        else:
            self.pubquizActive = False
        try:
            self.pubquizQuestionUserID = result["pubquizquestionuserid"]
        except:
            self.pubquizQuestionUserID = 1
        try:
            self.pubquizChannel = result["pubquizchannel"]
        except:
            self.pubquizChannel = 1


    def getcolour(self):
        colours = ["5C6BC0", "AB47BC", "EF5350", "FFA726", "FFEE58", "66BB6A", "5BCEFA", "F5A9B8", "FFFFFF", "F5A9B8", "5BCEFA"]
        self.currentColour += 1
        if self.currentColour ==  len(colours):
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