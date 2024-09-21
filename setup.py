import discord, asyncio, sys, traceback, checks, useful, asyncpg, random
from discord.ext import commands


class setupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "exit", aliases =['quit'], hidden = True)
    @checks.justme()
    async def exit(self, ctx):
        thanos = random.randint(1,5)
        if thanos == 1:
            await ctx.channel.send("Mrs Assertive I dont feel so good...")
        if thanos == 2:
            await ctx.channel.send("Why...")
        if thanos == 3:
            await ctx.channel.send(":wave: Goodbye.")
        if thanos == 4:
            await ctx.channel.send("Faster, Bambi! Don't look back! Keep running! Keep running!")
        if thanos == 5:
            await ctx.channel.send("The horror. The horror.")
        await self.bot.db.close()
        ##await self.bot.logout()
        await self.bot.close()
        sys.exit(0)

    @commands.command()
    @checks.justme()  # Or adjust the check as needed
    async def update_all_server_data(self, ctx):
        """Updates the database with information from all servers the bot is in."""

        await ctx.send("Starting server data update...")

        for guild in self.bot.guilds:
            # 1. Add guild to 'guilds' table
            await self._add_guild_to_db(guild)

            # 2. Add guild members to 'guild_users' table
            for member in guild.members:
                await self._add_member_to_db(member, guild)

            # 3. Add guild roles to 'guild_roles' table
            for role in guild.roles:
                await self._add_role_to_db(role, guild)

        await ctx.send(":white_check_mark: | Server data update complete!")

    @commands.command()
    @checks.justme()
    async def update_current_server_data(self, ctx):
        """Updates the database with information from the current server."""

        await ctx.send("Starting server data update...")

        guild = ctx.guild

        # 1. Add guild to 'guilds' table
        await self._add_guild_to_db(guild)

        # 2. Add guild members to 'guild_users' table
        for member in guild.members:
            await self._add_member_to_db(member, guild)

        # 3. Add guild roles to 'guild_roles' table
        for role in guild.roles:
            await self._add_role_to_db(role, guild)

        await ctx.send(":white_check_mark: | Server data update complete!")

    async def _add_guild_to_db(self, guild):
        query = """
            INSERT INTO guilds (guild_id)
            VALUES ($1)
            ON CONFLICT (guild_id) DO NOTHING;  -- Ignore if already exists
        """
        await self.bot.db.execute(query, guild.id)

    async def _add_member_to_db(self, member, guild):
        # 1. Add user to 'users' table if not already present
        await self._add_user_to_db(member)

        # 2. Add user-guild profile to 'guild_users' table
        query = """
            INSERT INTO guild_users (user_id, guild_id)
            VALUES ($1, $2)
            ON CONFLICT (user_id, guild_id) DO NOTHING;
        """
        await self.bot.db.execute(query, member.id, guild.id)

    async def _add_user_to_db(self, user):
        query = """
            INSERT INTO users (user_id)
            VALUES ($1)
            ON CONFLICT (user_id) DO NOTHING;
        """
        await self.bot.db.execute(query, user.id)

    async def _add_role_to_db(self, role, guild):
        # 1. Add role to 'roles' table if not already present
        await self._add_role_to_db_if_not_exists(role)

        # 2. Add guild-role association to 'guild_roles' table
        query = """
            INSERT INTO guild_roles (guild_id, role_id, role_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (guild_id, role_name) DO UPDATE 
            SET role_id = $2;  -- Update role_id if role_name already exists for the guild
        """
        await self.bot.db.execute(query, guild.id, role.id, role.name)

    async def _add_role_to_db_if_not_exists(self, role):
        query = """
            INSERT INTO roles (role_id)
            VALUES ($1)
            ON CONFLICT (role_id) DO NOTHING;
        """
        await self.bot.db.execute(query, role.id)

    @commands.command(hidden=True)
    @checks.has_role("Quizmaster", "Pub Quiz Senate")
    async def addmembers(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            for member in ctx.guild.members:
                # 1. Add user to 'users' table if not already present
                await self._add_user_to_db(member)

                # 2. Add user-guild profile to 'guild_users' table
                query = """
                    INSERT INTO guild_users (user_id, guild_id)
                    VALUES ($1, $2)
                    ON CONFLICT (user_id, guild_id) DO NOTHING;
                """
                await self.bot.db.execute(query, member.id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @commands.command(hidden=True)
    @checks.justme()
    async def addroles(self, ctx):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            for role in ctx.guild.roles:
                # 1. Add role to 'roles' table if not already present
                await self._add_role_to_db_if_not_exists(role)

                # 2. Add guild-role association to 'guild_roles' table
                query = """
                    INSERT INTO guild_roles (guild_id, role_id, role_name)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (guild_id, role_name) DO UPDATE 
                    SET role_id = $2;
                """
                await self.bot.db.execute(query, ctx.guild.id, role.id, role.name)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.command(hidden=True)
    @checks.justme()
    async def addguild(self, ctx):
        await self._add_guild_to_db(ctx.guild)  # Directly add the guild
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.command(hidden=True)
    @checks.justme()
    async def deletemember(self, ctx, member):
        member_id = int(useful.getid(member))
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            # Delete the user's profile from the specific guild
            query = "DELETE FROM guild_users WHERE user_id = $1 AND guild_id = $2"
            await self.bot.db.execute(query, member_id, ctx.guild.id)
        await self.bot.db.release(connection)
        await ctx.channel.send(":white_check_mark: | Done!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            # 1. Add guild to 'guilds' table
            await self._add_guild_to_db(guild)

            # 2. Add guild members to 'guild_users' table
            for member in guild.members:
                await self._add_member_to_db(member, guild)

            # 3. Add guild roles to 'guild_roles' table
            for role in guild.roles:
                await self._add_role_to_db(role, guild)
        await self.bot.db.release(connection)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            # 1. Add role to 'roles' table if not already present
            await self._add_role_to_db_if_not_exists(role)

            # 2. Add guild-role association to 'guild_roles' table
            query = """
                INSERT INTO guild_roles (guild_id, role_id, role_name)
                VALUES ($1, $2, $3)
                ON CONFLICT (guild_id, role_name) DO NOTHING; 
            """
            await self.bot.db.execute(query, role.guild.id, role.id, role.name)
        await self.bot.db.release(connection)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            # Delete the guild-role association from 'guild_roles' table
            query = "DELETE FROM guild_roles WHERE guild_id = $1 AND role_id = $2"
            await self.bot.db.execute(query, role.guild.id, role.id)
        await self.bot.db.release(connection)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            query = "DELETE FROM guild_users WHERE user_id = $1 AND guild_id = $2"
            await self.bot.db.execute(query, member.id, member.guild.id)
        await self.bot.db.release(connection)

        query = "SELECT leave_enabled, leave_channel_id, leave_message FROM guilds WHERE guild_id = $1"
        result = await self.bot.db.fetchrow(query, member.guild.id)
        if result and result['leave_enabled']:
            channel_id = result["leave_channel_id"]
            leave_text = useful.formatTextLeave(member, result["leave_message"])
            await member.guild.get_channel(int(channel_id)).send(leave_text)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        connection = await self.bot.db.acquire()
        async with connection.transaction():
            # 1. Add user to 'users' table if not already present
            await self._add_user_to_db(member)

            # 2. Add user-guild profile to 'guild_users' table
            query = """
                INSERT INTO guild_users (user_id, guild_id)
                VALUES ($1, $2)
                ON CONFLICT (user_id, guild_id) DO NOTHING;
            """
            await self.bot.db.execute(query, member.id, member.guild.id)
        await self.bot.db.release(connection)

        query = "SELECT welcome_enabled, welcome_channel_id, welcome_message FROM guilds WHERE guild_id = $1"
        result = await self.bot.db.fetchrow(query, member.guild.id)
        if result and result['welcome_enabled']:
            channel_id = result["welcome_channel_id"]
            welcome_text = useful.formatText(member, result["welcome_message"])
            await member.guild.get_channel(int(channel_id)).send(welcome_text)


async def setup(bot):
    await bot.add_cog(setupCog(bot))
    return