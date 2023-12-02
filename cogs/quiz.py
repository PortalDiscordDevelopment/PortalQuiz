"""Quiz cog"""
import asyncio
import datetime
import random

from discord import Interaction, app_commands
from discord.ext import commands
from DPyUtils import s

from cogs.internal.classes import Game, Question
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
        self.games: dict[int, Game] = {}

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
        questions = await self.get_questions(length)
        length = len(questions)  # catch in case there aren't enough questions
        top = interaction.user
        for idx, qstn in enumerate(questions):
            await asyncio.sleep(2)
            answers = [qstn.correct_answer, *qstn.wrong_answers]
            random.shuffle(answers)
            cori = answers.index(qstn.correct_answer)
            cor = chr(65 + cori)
            embed = (
                self.bot.Embed(
                    title=qstn.question,
                    description="\n\n".join(f"**{chr(65+n)}.** {a}" for n, a in enumerate(answers)),
                )
                .set_author(name=f"Category: {qstn.category}", icon_url=top.display_avatar.url)
                .set_footer(text=f"Question {idx+1}/{length} (ID: {qstn.id}) | 15 seconds to answer!")
            )
            v = Answers(self, interaction.guild, answers, idx)
            await interaction.send(embed=embed, view=v)
            self.games[interaction.guild.id].current_view = v
            self.games[interaction.guild.id].q_start = datetime.datetime.now().timestamp()
            try:
                _, _, data = await self.bot.wait_for(
                    "next_question",
                    check=lambda g, _i, d: g == interaction.guild.id and _i == idx,
                    timeout=15,
                )
            except asyncio.TimeoutError:
                data = await v.end()
            #            people = filter(
            #                lambda u: u.active, self.games[ctx.guild.id]["participants"].values()
            #            )
            nv = ShowAnswers(answers, cori)
            top = await self.scoring(interaction, data, cor)
            embed.description = f"__Answer:__\n**{cor}.** {qstn.correct_answer}\n\n__**Scores**__"
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
            ).set_author(name=f"Category: {qstn.category}", icon_url=top.display_avatar.url),
        )
        self.games[interaction.guild.id].active = False

    async def get_questions(self, n: int):
        """
        Retrieve a shuffled list of questions
        """
        questions: list[Question] = []
        async with self.bot.db.cursor() as cur:
            await cur.execute(
                """
                SELECT ROWID, category, question, correct, wrong_one, wrong_two, wrong_three
                    FROM questions
                    ORDER BY RANDOM()
                    LIMIT ?""",
                (n,),
            )
            data = await cur.fetchall()
            questions = [Question(*question_info) for question_info in data]
        # random.shuffle(questions)
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
        return sorted(people.values(), key=lambda p: p.score, reverse=True)[0].user

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
