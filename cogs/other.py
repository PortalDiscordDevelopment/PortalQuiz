import DPyUtils
import json
import discord
from discord.ext import commands
from cogs.internal.views import AcceptSuggestion


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

    @commands.command(name="ping")
    async def ping(self, ctx: DPyUtils.Context):
        """
        Gets bot latency.
        """
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(name="suggestq")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def suggestq(
        self,
        ctx: DPyUtils.Context,
        question: str = commands.Option(description="Question to ask"),
        correct: str = commands.Option(description="The correct answer"),
        wrong_one: str = commands.Option(description="Wrong answer #1"),
        wrong_two: str = commands.Option(description="Wrong answer #2", default="null"),
        wrong_three: str = commands.Option(
            description="Wrong answer #3", default="null"
        ),
        season: str = commands.Option(
            description="The time of year this question should appear"
        ),
    ):
        """
        Suggest a question
        """
        c = self.bot.get_channel(925420070774124565)
        await ctx.send(
            embed=self.bot.Embed(
                title="Question Suggested",
                description=f"Suggested `{question}` to the developers.",
            )
            .add_field(name="Correct Answer", value=f"• {correct}")
            .add_field(
                name="Wrong Answers",
                value=f"• {wrong_one}\n• {wrong_two}\n• {wrong_three}",
            )
            .add_field(name="Season", value=f"{season}"),
            ephemeral=True,
        )
        await c.send(
            embed=sent,
            view=self.bot.Embed(
                title="Question Suggested",
                description="```\n/addq\n"
                f"correct: {correct}\n"
                f"wrong_one: {wrong_one}\n"
                f"wrong_two: {wrong_two}\n"
                f"wrong_three: {wrong_three}\n",
            ),
        )


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Other(bot))
