import discord, asyncio, sys, traceback, checks, useful
from discord.ext import commands

class adminCog:
    def __init__(self, bot):
        self.bot = bot
        self.welcomeChannel = 0
        self.raidmodeState = False

    @commands.command()
    @checks.has_role("Admin", "Moderator")
    async def setwelcome(self, ctx):
        self.welcomeChannel = ctx.channel.id
        await ctx.channel.send("Welcome channel set here!")

    @commands.command(name="raidmode", aliases=['rm', 'raid', 'raidtoggle'])
    @checks.has_role("Admin", "Moderator")
    async def raidmode(self, ctx):
        self.raidmodeState = not self.raidmodeState
        await ctx.channel.send("Raid mode set to: " + str(self.raidmodeState))

    @commands.command(name="jail", aliases=['silence', 'unmute', 'unsilence', 'unjail'])
    @checks.has_role("Admin", "Moderator")
    async def jail(self, ctx, member):
        memberid = useful.getid(member)
        if discord.utils.get(ctx.guild.roles, name= "jail") in ctx.guild.get_member(memberid).roles:
            await ctx.guild.get_member(memberid).remove_roles(discord.utils.get(ctx.guild.roles, name="jail"))
            await ctx.channel.send("Unjailed " + ctx.guild.get_member(memberid).mention +"!")

        else:
            await ctx.guild.get_member(memberid).add_roles(discord.utils.get(ctx.guild.roles, name="jail"))
            await ctx.channel.send("Jailed " + ctx.guild.get_member(memberid).mention + "!")

    async def on_member_join(self, ctx):
        if self.raidmodeState == True:
            await ctx.add_roles(discord.utils.get(ctx.guild.roles, name="jail"))
            await ctx.send("This server is currently under attack! Please DM <@164921837107675137> or <@163691476788838401> if you are a legitimate user to get unjailed.")
        elif self.welcomeChannel != 0:
            await ctx.guild.get_channel(self.welcomeChannel).send("Welcome to /r/Traa Community, " + ctx.mention + "!")





def setup(bot):
    bot.add_cog(adminCog(bot))
