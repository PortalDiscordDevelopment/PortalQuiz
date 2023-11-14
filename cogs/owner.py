"""owner-only commands"""
import os

from discord import app_commands, Interaction
from discord.ext import commands
from quizbot import QuizBot

from cogs.internal.checks import is_owner


class Owner(commands.Cog):
    """
    Owner commands
    """

    def __init__(self, bot: QuizBot):
        self.bot = bot

    @app_commands.command(name="addq")
    @app_commands.describe(
        question="Question to ask",
        correct="The correct answer",
        wrong_one="Wrong answer #1",
        wrong_two="Wrong answer #2",
        wrong_three="Wrong answer #3",
        category="Season/category",
    )
    @app_commands.guilds(*map(int, os.getenv("SLASH_GUILDS").split("|")))
    @is_owner()
    async def addq(
        self,
        ctx: Interaction,
        question: str,
        correct: str,
        wrong_one: str,
        wrong_two: str = "null",
        wrong_three: str = "null",
        category: str = "null",
    ):
        """
        Add a question to the list of questions.
        """
        if ctx.user.id != 642416218967375882:
            return await ctx.response.send_message("no ty :)", ephemeral=True)
        async with self.bot.db.cursor() as c:
            await c.execute(
                "INSERT INTO questions(question, correct, wrong_one, wrong_two, wrong_three, category) VALUES (?, ?, ?, ?, ?, ?)",
                (question, correct, wrong_one, wrong_two, wrong_three, category),
            )
        await self.bot.db.commit()
        await ctx.response.send_message(
            embed=self.bot.Embed(
                title="Question Added",
                description=f"Added `{question}` to the list of questions.",
            )
            .add_field(name="Correct Answer", value=f"• {correct}")
            .add_field(
                name="Wrong Answers",
                value=f"• {wrong_one}\n• {wrong_two}\n• {wrong_three}",
            )
            .add_field(name="Category", value=category),
            ephemeral=True,
        )


async def setup(bot: QuizBot):  # pylint: disable=missing-function-docstring
    await bot.add_cog(Owner(bot))
