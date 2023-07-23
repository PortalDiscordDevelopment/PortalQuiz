import sys

import discord
from discord import app_commands
from discord.ext import commands
from DPyUtils import Bot, Interaction

# from cogs.internal.views import AcceptSuggestion


class Misc(commands.Cog):
    """
    Other commands.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="info")
    async def info(self, interaction: Interaction):
        """
        Shows information about the bot.
        """
        view = discord.ui.View()
        for n, u in {
            "Upvote Me": f"https://top.gg/bot/{self.bot.user.id}/vote",
            "Support Server": "https://discord.gg/cXwbSJHuxh",
            "Invite Me": discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(412317240384)),
        }.items():
            view.add_item(discord.ui.Button(label=n, url=u))

        await interaction.send(
            embed=self.bot.Embed(title="Portal Quiz Info")
            .add_field(
                name="Stats",
                value=f"""
                    Portal Quiz Version: `{self.bot.version}`
                    Framework: [discord.py](https://github.com/Rapptz/discord.py)
                    discord.py Version: `{discord.__version__}`
                    Python Version: `{sys.version}`
                    Server Count: `{len(self.bot.guilds)} servers`
                    """,
            )
            .add_field(
                name="Info",
                value=f"""Director: Thomas Morton
                    Developers: {', '.join(map(str, map(self.bot.get_user, (642416218967375882, 511655498676699136))))}
                    """,
            ),
            view=view,
        )

    @app_commands.command(name="ping")
    async def ping(self, interaction: Interaction):
        """
        Gets bot latency.
        """
        await interaction.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="suggestq")
    @app_commands.describe(
        question="Question to ask",
        correct="The correct answer",
        wrong_one="Wrong answer #1",
        wrong_two="Wrong answer #2",
        wrong_three="Wrong answer #3",
        season="The time of year this question should appear",
    )
    # @commands.cooldown(1, 60, commands.BucketType.user)
    async def suggestq(
        self,
        interaction: Interaction,
        question: str,
        correct: str,
        wrong_one: str,
        wrong_two: str = "null",
        wrong_three: str = "null",
        season: str = "winter",
    ):
        """
        Suggest a question
        """
        c = self.bot.get_channel(938852082537103411)
        await interaction.send(
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
            embed=self.bot.Embed(
                title="Question Suggested",
                description="```\n/addq\n"
                f"correct: {correct}\n"
                f"wrong_one: {wrong_one}\n"
                f"wrong_two: {wrong_two}\n"
                f"wrong_three: {wrong_three}\n",
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Misc(bot))
