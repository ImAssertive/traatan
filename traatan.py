import discord, asyncio, sys, traceback, checks, asyncpg, useful, credentials
from discord.ext import commands

async def get_prefix(bot, message):
    prefixes = ["traa!", "tt!", "tt?"]
    return commands.when_mentioned_or(*prefixes)(bot, message)

async def run():
    # Prints discord.py version
    print("Traatan running on d.py version: " + discord.__version__)

    # Gets bot token and database login credentials
    description = "Super Gay Bot"
    creds = credentials.get_db_creds()

    # Database creation on new systems
    db = await asyncpg.create_pool(**creds)
    await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY
    );  
    
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id BIGINT PRIMARY KEY,
        kick_message TEXT,
        ban_message TEXT,
        quiz_default_duration SMALLINT DEFAULT 10, 
        quiz_in_progress BOOLEAN DEFAULT FALSE,
        quiz_start_message TEXT,
        quiz_end_message TEXT,
        quiz_channel_id BIGINT,
        current_question_number INTEGER DEFAULT 0,
        current_season_number INTEGER DEFAULT 1,
        current_quiz_number INTEGER DEFAULT 1,
        quiz_last_question_super BOOLEAN DEFAULT FALSE,
        welcome_enabled BOOLEAN DEFAULT FALSE,
        welcome_channel_id BIGINT,
        welcome_message TEXT,
        leave_enabled BOOLEAN DEFAULT FALSE,
        leave_channel_id BIGINT,
        leave_message TEXT
    );
    
    CREATE TABLE IF NOT EXISTS guild_users ( 
        user_id BIGINT REFERENCES users(user_id),
        guild_id BIGINT REFERENCES guilds(guild_id),
        warnings INTEGER DEFAULT 0,
        pronouns TEXT, 
        PRIMARY KEY (user_id, guild_id)
    );
    
    CREATE TABLE IF NOT EXISTS roles (
        role_id BIGINT PRIMARY KEY
    ); 
    
    CREATE TABLE IF NOT EXISTS guild_roles (
        guild_id BIGINT REFERENCES guilds(guild_id),
        role_id BIGINT REFERENCES roles(role_id),
        role_name TEXT NOT NULL,
        self_assignable BOOLEAN DEFAULT FALSE, 
        PRIMARY KEY (guild_id, role_name),
        FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
    );
    
    CREATE TABLE IF NOT EXISTS user_scores (
        user_id BIGINT,
        guild_id BIGINT,
        season_number INTEGER,
        quiz_number INTEGER, 
        score INTEGER,
        PRIMARY KEY (user_id, guild_id, season_number, quiz_number),
        FOREIGN KEY (user_id, guild_id) REFERENCES guild_users(user_id, guild_id) ON DELETE CASCADE 
    );
    ''')

    # Creates bot object and attempts to load cogs
    bot = Bot(description=description, db=db, intents=discord.Intents.all())
    initial_extensions = ['admin', 'setup', 'misc', 'roles', 'pubquiz', 'eval']
    if __name__ == '__main__':
        for extension in initial_extensions:
            try:
                await bot.load_extension(extension)
                #print('Successfully loaded extension ' + extension)
            except Exception as e:
                ##Outputs exception upon failing to load a cog
                print('Failed to load extension ' + extension, file=sys.stderr)
                traceback.print_exc()

    ##Launches bot
    try:
        await bot.start(credentials.get_bot_token())
    except Exception as e:
        print("Unexpected error: ", e)
        await bot.db.close()
        await bot.close()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=get_prefix,
            intents=kwargs.pop("intents")
        )
        ##Temporary store of users pubquiz answers
        self.pubquiz_answers = {}  # {guild_id: [answer1, answer2, ...]}

        ##Store of guilds and channels that have active questions
        self.active_quiz_guilds = {}  # {guild_id: (channel_id)}

        self.active_questions = {} # {guild_id: (channel_id, question_asker_id)}


        ##Dictionary of all named roles and their corresponding ID's (note to self, make this less bad)
        #self.rolesDict = {"Admin": 348608087793467412, "Admin Powers": 406091590923321355,
        #                  "Helper": 395565792457916417, "Helper Powers": 395565792457916417,
        #                  "Owner": 348207687319683072,
        #                  "Moderator Powers": 388829460759052288, "Moderator": 348747695088730113,
        #                  "User": 348208233254617110,
        #                  "Quizmaster": 449941007619063828,
        #                  "Muted": 356529701675859990,
        #                  "Bot Tinkerer": 504059432238579712,
        #                  "Pub Quiz Senate": 663779037835165706}

        self.db = kwargs.pop("db")
        self.currentColour = -1

        ##List of all 8ball/conch phrases
        self.outcomes = ["It is certain", "It is decidedly so", "Without a doubt", "Yes - definitely",
                         "You may rely on it",
                         "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes",
                         "Reply hazy, try again", "Ask again later", "Better not tell you now",
                         "Cannot predict now", "Concentrate and ask again", "Don't count on it",
                         "My reply is no", "My sources say no", "Outlook not so good", "Very doubtful"]

    ##Run upon successful bot login
    async def on_ready(self):
        ##Outputs the username and ID of bot client on login
        print("Username: {0}\nID: {0.id}".format(self.user))

        ##Updates bots presence
        game = discord.Game("chess with Rainbow Restarter!")
        await self.change_presence(status=discord.Status.online, activity=game)

    ##Returns the next unused colour of the rainbow as a discord colour object - can be used with embeds for style
    def getcolour(self):
        colours = ["5C6BC0", "AB47BC", "EF5350", "FFA726", "FFEE58", "66BB6A", "5BCEFA", "F5A9B8", "FFFFFF", "F5A9B8",
                   "5BCEFA"]
        self.currentColour += 1
        ##Resets colour value to 0 if all colour values have been used
        if self.currentColour == len(colours):
            self.currentColour = 0
        ##Returns colour object using the assigned hex code
        return discord.Colour(int(colours[self.currentColour], 16))

    ##Returns a red/yellow/green discord colour object equating to the statement shown when using the magic conch command
    def conchcolour(self, number):
        if number < 10 and number > -1:
            return discord.Colour(int("00FF00", 16))
        elif number > 9 and number < 15:
            return discord.Colour(int("FFFF00", 16))
        else:
            return discord.Colour(int("FF0000", 16))


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
