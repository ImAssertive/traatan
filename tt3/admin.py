import discord, asyncio, sys, traceback, checks, useful, asyncpg, settingsFunctions
from discord.ext import commands


class adminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setup', aliases=['botsetup', 'su'])
    async def setup(self, ctx):
        if not ctx.guild:
            await ctx.author.send(":no_good: | This command can not be used in DM!")
        else:
            choice = "choice"
            options = ["info", "yes", "no", "skip"]
            while choice not in options:
                embed = discord.Embed(title="Welcome to the TraaTan setup menu!", description="This menu allows you to decide which commands will work on this server. If you would like to grant or remove permissions from a specific role please use the UNDEFINED command!",colour=self.bot.getcolour())
                embed.add_field(name="Firstly - would you like to have pubquiz commands enabled?",value="Options: `Yes`, `No`, `Info`, `Skip`")
                await ctx.channel.send(embed = embed)
                try:
                    choice = await self.bot.wait_for_message(self, check=checks.setup_options1(ctx, options), timeout = 60.0)
                except asyncio.TimeoutError:
                    try:
                        await ctx.channel.send(":no: | **"+ctx.author.nick + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        break
                    except TypeError:
                        await ctx.channel.send(":no: | **"+ctx.author.name + "** The command menu has closed due to inactivity. Please type tt!setup again to restart the process.")
                        break
                else:
                    if choice.lower() == "yes":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "UPDATE Guilds SET pubquizEnabled = true WHERE guildID = $1"
                            await self.bot.db.execute(query, ctx.guild.id)
                        await self.bot.db.release(connection)
                        await ctx.channel.send("Got it! Pubquiz commands have been enabled.")
                    elif choice.lower() == "no":
                        connection = await self.bot.db.acquire()
                        async with connection.transaction():
                            query = "UPDATE Guilds SET pubquizEnabled = false WHERE guildID = $1"
                            await self.bot.db.execute(query, ctx.guild.id)
                        await self.bot.db.release(connection)
                        await ctx.channel.send("Got it! Pubquiz commands have been disabled.")
                    elif choice.lower == "info":
                        await ctx.channel.send("Info coming soon.")
                    elif choice.lower == "skip":
                        await ctx.channel.send("Got it! I've left your pubquiz settings as is!")
    

    @commands.command(name='botglobalban', aliases=['bgb', 'fuckoff'])
    @checks.justme()
    async def botglobalban(self, ctx, member):
        memberid = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Users SET banned = true WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")


    @commands.command(name='botglobalunban', aliases=['bgub', 'wback'])
    @checks.justme()
    async def botglobalunban(self, ctx, member):
        memberid = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "UPDATE Users SET banned = false WHERE userID = $1"
            await self.bot.db.execute(query, memberid)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

def setup(bot):
    bot.add_cog(adminCog(bot))