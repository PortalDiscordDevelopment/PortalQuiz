"""Quiz cog"""
import discord
import DPyUtils
from discord.ext import commands


class Quiz(commands.Cog):
    """Quiz cog"""

    def __init__(self, bot: DPyUtils.Bot):
        self.bot = bot

    @commands.command(name="quiz")
    async def quiz(
        self,
        ctx: DPyUtils.Context,
        length: int = commands.Option(description="# of questions."),
    ):
        """
        Starts a Christmas-themed quiz.
        """
        await ctx.send(
            f"Started quiz with {length} questions.\n||That's a lie, I'm too lazy to implement it rn :)||",
            ephemeral=True,
        )


#        async with self.bot.db.cursor() as cur:
#            await cur.execute("SELECT questions, correct_answer, wrong_1, wrong_2, wrong_3 FROM questions")


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Quiz(bot))
