"""owner-only commands"""
import discord, os
import DPyUtils
from discord.ext import commands


class Owner(
    commands.Cog,
    command_attrs={"slash_command_guilds": os.getenv("SLASH_GUILDS").split("|")},
):
    def __init__(self, bot: DPyUtils.Bot):
        self.bot = bot

    @commands.command(name="add")
    async def add(
        self,
        ctx: DPyUtils.Context,
        question: str = commands.Option(description="Question to ask"),
        correct: str = commands.Option(description="The correct answer"),
        wrong_one: str = commands.Option(description="Wrong answer #1"),
        wrong_two: str = commands.Option(description="Wrong answer #2"),
        wrong_three: str = commands.Option(description="Wrong answer #3"),
    ):
        """
        Add a question to the list of questions.
        """
        await ctx.send(
            embed=discord.Embed(
                title="Question Added",
                description=f"Added `{question}` to the list of questions.",
            )
            .add_field(name="Correct Answer", value=correct)
            .add_field(
                name="Wrong Answers", value=f"{wrong_one}\n{wrong_two}\n{wrong_three}"
            )
        )


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Owner(bot))
