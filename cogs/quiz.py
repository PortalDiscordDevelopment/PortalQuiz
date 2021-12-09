"""Quiz cog"""
import asyncio
import datetime
import random
import DPyUtils
from discord.ext import commands
from cogs.internal.views import JoinStartLeave, Answers, ShowAnswers


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
            ephemeral=False,
        )
        try:
            await self.bot.wait_for(
                "quiz_start",
                check=lambda i, m: i == ctx.guild.id and m == ctx.author.id,
                timeout=300,
            )
        except asyncio.TimeoutError:
            pass
        if len(self.games[ctx.guild.id]["participants"]) < 1:
            return await ctx.send(f"You can't play a game with no players!")
        await ctx.send(
            f"Game starting!\nParticipants: {', '.join(ctx.guild.get_member(i).mention for i in self.games[ctx.guild.id]['participants'])}",
        )
        questions = [
            ("rudolph", "exists", "dead", "muskrat", "purple"),
            ("turtle", "butt", "horton"),
        ]
        #        async with self.bot.db.cursor() as cur:
        #            await cur.execute("SELECT question, correct, wrong_one, wrong_two, wrong_three FROM questions")
        #            questions = await cur.fetchall()
        random.shuffle(questions)
        qs = questions[:length]
        length = len(qs)
        for i, q in enumerate(qs):
            question = q[0]
            answers = list(q[1:])
            random.shuffle(answers)
            cori = answers.index(q[1])
            cor = chr(65 + cori)
            embed = self.bot.Embed(
                title=question,
                description="\n\n".join(
                    f"**{chr(65+n)}.** {a}" for n, a in enumerate(answers)
                ),
            ).set_footer(text=f"Question {i+1}/{length}")
            v = Answers(self, ctx.guild, answers, i)
            await ctx.send(embed=embed, view=v)
            _, _, data = await self.bot.wait_for(
                "next_question", check=lambda g, _i, d: g == ctx.guild.id and _i == i
            )
            nv = ShowAnswers(answers, cori)
            embed.description = f"Correct Answer: **{cor}.** {q[1]}"
            await ctx.send(embed=embed, view=nv)
            await asyncio.sleep(5)
        await ctx.send("this is totally final scores")


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Quiz(bot))
