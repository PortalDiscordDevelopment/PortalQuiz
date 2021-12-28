import DPyUtils
import json
import discord
from discord.ext import commands
from discord.ext.commands.core import Command
from discord.ext.commands.errors import CommandOnCooldown


class Other(commands.Cog):
    """
    Other commands.
    """

    def __init__(self, bot: DPyUtils.Bot):
        self.bot = bot

    @commands.command(name="info")
    async def info(self, ctx: DPyUtils.Context):
        """
        Shows information about the Bot.
        """

        def get_version() -> str:
            with open("data.json", "r") as f:
                return json.loads(f.read())["version"]

        version = get_version()

        await ctx.send(
            embed=self.bot.Embed(
                title="Winter Quiz",
                description=f"""
                    **Stats:**
                    Version: {version}
                    Server Count: {len(self.bot.guilds)} servers
                    Director: Thomas Morton
                    Developers: {', '.join(map(str, map(self.bot.get_user, (642416218967375882, 511655498676699136))))}
                    Framework: [enhanced-discord.py](https://github.com/iDevision/enhanced-discord.py)
                    """.replace(
                    "    ", ""
                ),
            )
        )

    @commands.command(name="invite")
    async def invite(self, ctx: DPyUtils.Context):
        """
        Invite the bot to your server.
        """
        await ctx.send(
            embed=self.bot.Embed(
                title="Invite the bot to your server",
                description=f"[Click here to invite the bot to your server.]({discord.utils.oauth_url(self.bot.user.id, scopes=('applications.commands', 'bot'), permissions=discord.Permissions(412317240384))})",
            )
        )

    @commands.command(name="suggestq")
    @commands.cooldown(1,60,commands.BucketType.user)
    async def suggestq(self, ctx: DPyUtils.Context, question: str):
        """
        Suggest a question.
        """
        try: 
            c = self.bot.get_channel(925420070774124565)
            embed = self.bot.Embed(
                title="Suggestion Created",
                description=f"{ctx.author} suggested a quesiton")
            embed.add_field(name="Question", value=question)
            await c.send(embed=embed)
            await ctx.send("Your Suggestion has been sent!")

        except CommandOnCooldown:
            await ctx.send(embed=self.bot.Embed(title="Cooldown", description="You are on cooldown. Please wait a minute before trying again."))

        except Exception as e:
            if isinstance(e, CommandOnCooldown):
                pass
            else:
                error = self.bot.Embed(
                    title=f"Error while running command ('{ctx.command}')",
                    description=f"{e}",
                    color = discord.Color.dark_red()
                )
                usererror = self.bot.Embed(
                    title=f"Error while running command ('{ctx.command}')",
                    description="Sorry, an error has occured while running this command. Try again in a few minutes, a traceback has been sent to the developers.",
                    color = discord.Color.dark_red()
                )
                await c.send(embed=error)
                await ctx.send(embed=usererror)
        


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Other(bot))
