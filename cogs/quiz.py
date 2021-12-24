"""Quiz cog"""
import asyncio
import datetime
import discord
import random
import DPyUtils
from DPyUtils import s
from discord.ext import commands
from cogs.internal.views import JoinStartLeave, Answers, ShowAnswers
from cogs.internal.classes import Game
import json


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

    @commands.command(name="info")
    async def info(self, ctx: DPyUtils.Context):
        """
        Shows information about the Bot.
        """
        def get_version() -> str:
            with open('data.json', 'r') as f:
                return json.loads(f.read())['version']
        
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
                )
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
                description="[Click here to invite the bot to your server.]"
                "(https://discord.com/api/oauth2/authorize?"
                "client_id=871981757531050064&permissions=412317240384&"
                "scope=applications.commands%20bot)",
            )
        )

    @commands.command(name="quiz")
    async def quiz(
        self,
        ctx: DPyUtils.Context,
        length: int = commands.Option(description="# of questions."),
    ):
        """
        Starts a Christmas-themed quiz.
        """
        self.games[ctx.guild.id] = Game(ctx)
        questions = await self.get_questions()
        qs = questions[:length]
        length = len(qs)
        #        v = JoinStartLeave(self, length)
        #        await ctx.send(
        #            embed=self.bot.Embed(
        #                title="Quiz Starting!",
        #                description=f"Winter quiz beginning <t:{int(datetime.datetime.now().timestamp()+300)}:R>! Press the button below to join.",
        #            )
        #            .set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
        #            .set_footer(text=ctx.guild, icon_url=ctx.guild.icon or discord.Embed.Empty),
        #            view=v,
        #            ephemeral=False,
        #        )
        #        try:
        #            await self.bot.wait_for(
        #                "quiz_start",
        #                check=lambda i, m: i == ctx.guild.id and m == ctx.author.id,
        #                timeout=300,
        #            )
        #        except asyncio.TimeoutError:
        #            pass
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
                description="\n\n".join(
                    f"**{chr(65+n)}.** {a}" for n, a in enumerate(answers)
                ),
            ).set_footer(
                text=f"Question {i+1}/{length} (ID: {rid}) | 15 seconds to answer!"
            )
            v = Answers(self, ctx.guild, answers, i)
            await ctx.send(embed=embed, view=v)
            self.games[ctx.guild.id].current_view = v
            self.games[ctx.guild.id].q_start = datetime.datetime.now().timestamp()
            try:
                _, _, data = await self.bot.wait_for(
                    "next_question",
                    check=lambda g, _i, d: g == ctx.guild.id
                    and _i == i,  # pylint: disable=cell-var-from-loop
                    timeout=15,
                )
            except asyncio.TimeoutError:
                data = await v.end()
            #            people = filter(
            #                lambda u: u.active, self.games[ctx.guild.id]["participants"].values()
            #            )
            nv = ShowAnswers(answers, cori)
            await self.scoring(ctx, data, cor)
            embed.description = f"__Answer:__\n**{cor}.** {q[1]}\n\n__**Scores**__"
            embed.description += await self.fmt_scores(ctx)
            await ctx.send(embed=embed, view=nv)
            if not self.games[ctx.guild.id].active:
                break
        #            if not any(people):
        #                break
        await ctx.send(
            embed=self.bot.Embed(
                title="Final Scores", description=await self.fmt_scores(ctx, True)
            )
        )
        self.games[ctx.guild.id].active = False

    async def get_questions(self):
        questions = []
        async with self.bot.db.cursor() as cur:
            await cur.execute(
                "SELECT ROWID, question, correct, wrong_one, wrong_two, wrong_three FROM questions"
            )
            data = await cur.fetchall()
            for q in data:
                t = list(q)
                while "null" in t:
                    t.remove("null")
                questions.append(tuple(t))
        random.shuffle(questions)
        return questions

    async def scoring(self, ctx: DPyUtils.Context, data: dict, cor: str):
        people = self.games[ctx.guild.id].participants
        for uid, p in people.items():
            a, t = data.get(uid, ["", 0])
            if not a:
                p.unanswered += 1
                continue
            p.answered += 1
            this_score = 0
            if a == cor:
                this_score = round((15 - (t - self.games[ctx.guild.id].q_start)) * 4)
                p.score += this_score
            p.up_by = this_score

    async def fmt_scores(self, ctx: DPyUtils.Context, final: bool = False):
        scores = ""
        for i, p in enumerate(
            sorted(
                self.games[ctx.guild.id].participants.values(),
                key=lambda p: p.score,
                reverse=True,
            ),
            1,
        ):
            m = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"**{i}.**"
            if final and i == 1:
                scores += f"🏆 **Winner!**\n{p.user} with {p.score} points.\n"
            else:
                scores += (
                    f"\n{m} `{p.score}` point{s(p.score)} (`+{p.up_by}`): {p.user}"
                )
        return scores

    @commands.command(name="endquiz")
    @commands.has_permissions(manage_messages=True)
    async def endquiz(self, ctx: DPyUtils.Context):
        if not self.games.get(ctx.guild.id, None) or (
            self.games.get(ctx.guild.id, None) and not self.games[ctx.guild.id].active
        ):
            return await ctx.send("There is no quiz currently running!", ephemeral=True)
        await self.games[ctx.guild.id].end()
        await ctx.send(f"*Quiz ended by {ctx.author}*")


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Quiz(bot))
