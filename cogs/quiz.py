"""Quiz cog"""
import datetime
import random
import DPyUtils
from discord.ext import commands
from cogs.internal.views import Answers, JoinStartLeave


class Quiz(commands.Cog):
    """Quiz cog"""

    def __init__(self, bot: DPyUtils.Bot):
        """
        games format:
        ..code-block:: json
            {
                guild_id: {
                    "active": bool,
                    "start_by": user_id,
                    "participants": {
                        user_id: cogs.classes.Player
                    }
                }
            }
        """
        self.bot = bot
        self.games = {}

    @commands.command(name="quiz")
    async def quiz(
        self,
        ctx: DPyUtils.Context,
        length: int = commands.Option(description="# of questions."),
    ):
        """
        Starts a Christmas-themed quiz.
        """
        self.games[ctx.guild.id] = {
            "active": False,
            "start_by": ctx.author.id,
            "participants": {},
        }
        await ctx.send(
            f"Started quiz with {length} questions.\n||That's a lie, I'm too lazy to implement it rn :)||",
            ephemeral=True,
        )
        v = JoinStartLeave(self, length)
        await ctx.send(
            f"Winter quiz beginning <t:{int(datetime.datetime.now().timestamp()+300)}:R>! Press the button below to join.",
            view=v,
        )
        questions = []
        random.shuffle(questions)
        for i, q in enumerate(questions[:length]):
            question = q[0]
            answers = q[1:]
            random.shuffle(answers)
            cor = ord(65 + answers.index(q[1]))
            embed = self.bot.Embed(
                title=question,
                description="\n\n".join(
                    f"**{ord(65+n)}.** {a}" for n, a in enumerate(answers)
                ),
            ).set_footer(text=f"Question {i}/{length}")
            v = Answers(self, ctx.guild, len(answers))
            await ctx.send(embed=embed, view=v)


#        async with self.bot.db.cursor() as cur:
#            await cur.execute("SELECT questions, correct_answer, wrong_1, wrong_2, wrong_3 FROM questions")


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Quiz(bot))
