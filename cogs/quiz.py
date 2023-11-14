"""Quiz cog"""
import asyncio
import datetime
import random

from discord import Interaction, app_commands
from discord.ext import commands
from DPyUtils import s

from cogs.internal.classes import Game
from cogs.internal.views import Answers, ShowAnswers
from quizbot import QuizBot


class Quiz(commands.Cog):
    """Quiz cog"""

    def __init__(self, bot: QuizBot):
        """
        games format:

        .. code-block:: python3
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

    @app_commands.command(name="quiz")
    @app_commands.describe(length="# of questions.")
    async def quiz(
        self,
        interaction: Interaction,
        length: int,
    ):
        """
        Starts a Christmas-themed quiz.
        """
        # await interaction.response.defer()
        if length < 1:
            return await interaction.send("You need a minimum of 1 question.")
        self.games[interaction.guild.id] = Game(interaction)
        questions = await self.get_questions()
        qs = questions[:length]
        length = len(qs)
        for i, q in enumerate(qs):
            await asyncio.sleep(2)
            rid = q[0]
            q = q[1:]
            question = q[0]
            answers = list(q[1:])
            random.shuffle(answers)
            cori = answers.index(q[1])
            cor = chr(65 + cori)
            embed = self.bot.Embed(
                title=question,
                description="\n\n".join(f"**{chr(65+n)}.** {a}" for n, a in enumerate(answers)),
            ).set_footer(text=f"Question {i+1}/{length} (ID: {rid}) | 15 seconds to answer!")
            v = Answers(self, interaction.guild, answers, i)
            print("made it to send")
            await interaction.send(embed=embed, view=v)
            self.games[interaction.guild.id].current_view = v
            self.games[interaction.guild.id].q_start = datetime.datetime.now().timestamp()
            try:
                _, _, data = await self.bot.wait_for(
                    "next_question",
                    check=lambda g, _i, d: g == interaction.guild.id and _i == i,
                    timeout=15,
                )
            except asyncio.TimeoutError:
                data = await v.end()
            #            people = filter(
            #                lambda u: u.active, self.games[ctx.guild.id]["participants"].values()
            #            )
            nv = ShowAnswers(answers, cori)
            await self.scoring(interaction, data, cor)
            embed.description = f"__Answer:__\n**{cor}.** {q[1]}\n\n__**Scores**__"
            embed.description += await self.fmt_scores(interaction)
            await interaction.send(embed=embed, view=nv)
            if not self.games[interaction.guild.id].active:
                break
        #            if not any(people):
        #                break
        await interaction.send(
            embed=self.bot.Embed(
                title="Final Scores",
                description=await self.fmt_scores(interaction, True),
            )
        )
        self.games[interaction.guild.id].active = False

    async def get_questions(self):
        """
        Retrieve a shuffled list of questions
        """
        questions = []
        async with self.bot.db.cursor() as cur:
            await cur.execute("SELECT ROWID, question, correct, wrong_one, wrong_two, wrong_three FROM questions")
            data = await cur.fetchall()
            for q in data:
                t = list(q)
                while "null" in t:
                    t.remove("null")
                questions.append(tuple(t))
        random.shuffle(questions)
        return questions

    async def scoring(self, interaction: Interaction, data: dict, cor: str):
        """
        Calculates scores
        """
        people = self.games[interaction.guild.id].participants
        for uid, p in people.items():
            a, t = data.get(uid, ["", 0])
            if not a:
                p.unanswered += 1
                continue
            p.answered += 1
            this_score = 0
            if a == cor:
                this_score = round((15 - (t - self.games[interaction.guild.id].q_start)) * 4)
                p.score += this_score
            p.up_by = this_score

    async def fmt_scores(self, interaction: Interaction, final: bool = False):
        """
        Score formatter
        """
        scores = ""
        for i, p in enumerate(
            sorted(
                self.games[interaction.guild.id].participants.values(),
                key=lambda p: p.score,
                reverse=True,
            ),
            1,
        ):
            m = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"**{i}.**"
            if final and i == 1:
                scores += f"🏆 **Winner!**\n{p.user} with {p.score} points.\n"
            else:
                scores += f"\n{m} `{p.score}` point{s(p.score)} (`+{p.up_by}`): {p.user}"
        return scores

    @app_commands.command(name="endquiz")
    async def endquiz(self, interaction: Interaction):
        """
        Ends the active quiz.
        """
        if not self.games.get(interaction.guild.id, None) or (
            self.games.get(interaction.guild.id, None) and not self.games[interaction.guild.id].active
        ):
            return await interaction.send("There is no quiz currently running!", ephemeral=True)
        g: Game = self.games[interaction.guild.id]
        if not (
            interaction.channel.permissions_for(interaction.user).manage_messages or interaction.user.id == g.start_by
        ):
            raise commands.MissingPermissions("manage_messages")
        await self.games[interaction.guild.id].end()
        await interaction.send(f"*Quiz ended by {interaction.user}*")


async def setup(bot: QuizBot):
    await bot.add_cog(Quiz(bot))
