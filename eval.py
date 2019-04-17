import io
import textwrap
import traceback
import re
import discord
from contextlib import redirect_stdout
from discord.ext import commands


class evalCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval", aliases=["evaluate"], hidden=True)
    @checks.just_me()
    async def _eval(self, ctx, *, body):
        env = {
            "discord": discord,
            "ctx": ctx,
            "bot": self.bot,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "__import__": __import__
        }

        def cleanup(content):
            # remove triple graves
            if content.startswith(("```", "```py", "```python")) and content.endswith("```"):
                return "\n".join(re.match(r"```(?ms)(?:py|python|)\n*(.*)\n*```", content).group(1).split("\n"))

            # remove single ticks
            return content.strip("` \n")

        env.update(globals())

        body = cleanup(body)
        stdout = io.StringIO()

        to_compile = f"async def func():\n{textwrap.indent(body, '   ')}"

        def paginate(text: str):
            """Paginates ret if longer than message limit. Handles by string, not meaningful delimiters."""
            last = 0
            pages = []
            for current in range(0, len(text)):
                if current % 1990 == 0:
                    pages.append(text[last:current])
                    last = current
                    append_index = current
            if append_index != len(text) - 1:
                pages.append(text[last:current + 1])
            return list(filter(lambda a: a != "", pages))

        try:
            await ctx.message.add_reaction("\u2699") # gear
            exec(to_compile, env)
        except Exception as ex:
            await ctx.message.add_reaction("❌")
            await ctx.message.remove_reaction("\u2699", self.bot.user)
            await ctx.send(embed=f"**An error occurred.**\n`{ex.__class__.__name__}: {ex}`")
            return

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except:
            ex_data = traceback.format_exc()
            await ctx.message.add_reaction("❌")
            await ctx.message.remove_reaction("\u2699", self.bot.user)
            await ctx.send(f"**An error occurred.**\n```{ex_data}```")
            return
        else:
            value = stdout.getvalue()
            await ctx.message.add_reaction("✅")
            await ctx.message.remove_reaction("\u2699", self.bot.user)
            if ret is None:
                if value:
                    try:
                        await ctx.send(f"```\n{value}\n```")
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                await ctx.send(f"```\n{page}\n```")
                                break
                            await ctx.send(f"```\n{page}\n```")
            else:
                try:
                    await ctx.send(f"```\n{value}{ret}\n```")
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            await ctx.send("```\n{page}\n```")
                            break
                        await ctx.send(f"```\n{page}\n```")


def setup(bot):
    bot.add_cog(EvalCog(bot))
