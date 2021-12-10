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
    @commands.is_owner()
    async def add(
        self,
        ctx: DPyUtils.Context,
        question: str = commands.Option(description="Question to ask"),
        correct: str = commands.Option(description="The correct answer"),
        wrong_one: str = commands.Option(description="Wrong answer #1"),
        wrong_two: str = commands.Option(description="Wrong answer #2", default="null"),
        wrong_three: str = commands.Option(
            description="Wrong answer #3", default="null"
        ),
    ):
        """
        Add a question to the list of questions.
        """
        async with self.bot.db.cursor() as c:
            await c.execute(
                "INSERT INTO questions(question, correct, wrong_one, wrong_two, wrong_three) VALUES (?, ?, ?, ?, ?)",
                (question, correct, wrong_one, wrong_two, wrong_three),
            )
        await self.bot.db.commit()
        await ctx.send(
            embed=self.bot.Embed(
                title="Question Added",
                description=f"Added `{question}` to the list of questions.",
            )
            .add_field(name="Correct Answer", value=correct)
            .add_field(
                name="Wrong Answers", value=f"{wrong_one}\n{wrong_two}\n{wrong_three}"
            ),
            ephemeral=True,
        )


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Owner(bot))
