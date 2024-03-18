import datetime

from discord import ButtonStyle, Guild, Interaction, ui
from discord.ext import commands

from quizbot import QuizBot

from .classes import Player


class Answer(ui.Button):
    def __init__(self, _type: int = 0, answer: str = "", **kwargs):
        bkey = {-1: 4, 0: 1, 1: 3}
        kwargs.update(style=ButtonStyle(bkey[_type]), disabled=_type != 0)
        self.answer = answer
        super().__init__(**kwargs)

    async def callback(self, interaction: Interaction):
        game = self.view.cog.games.get(interaction.guild_id, None)
        if not game:
            return await interaction.send("why is this button active without an associated game 🤔", ephemeral=True)
        user = game.participants.get(interaction.user.id, None)
        if not user:
            user = Player(interaction.user)
            game.participants[interaction.user.id] = user
        self.view.answered[interaction.user.id] = [
            self.label,
            datetime.datetime.now().timestamp(),
        ]
        await interaction.send(f"Answered: {self.answer}", ephemeral=True)


#        await self.view.all_done()


class Leave(ui.Button):
    def __init__(self, cog: commands.Cog, **kwargs):
        kwargs.update(style=ButtonStyle(4), label="Leave")
        super().__init__(**kwargs)
        self.cog = cog

    async def callback(self, interaction: Interaction):
        # await interaction.response.defer()
        gdat = self.cog.games.get(interaction.guild_id, None)
        if not gdat:
            return
        user = gdat["participants"].get(interaction.user.id, None)
        if not user or not user.active:
            return await interaction.send("You are not in this game.", ephemeral=True)
        if hasattr(self.view, "participating"):
            self.view.participating.remove(user.user.id)
        if gdat["active"]:
            user.active = False
            await self.view.all_done()
            await interaction.send(f"{user.user} has left the game.")
        else:
            self.cog.games[interaction.guild.id]["participants"].pop(user.user.id)
            await interaction.send("Joined the game.", ephemeral=True)
        people = (
            lambda u: u.active,
            self.cog.games[interaction.guild.id]["participants"].values(),
        )
        if not any(people):
            await interaction.send("No one is playing... Ending the game.")
            await self.view.all_done()


class JoinStartLeave(ui.View):
    def __init__(self, cog: commands.Cog, totalq: int, **kwargs):
        self.totalq = totalq
        self.cog = cog
        kwargs.setdefault("timeout", 300)
        super().__init__(**kwargs)
        self.add_item(Leave(self.cog))

    @ui.button(label="Join", style=ButtonStyle(3))
    async def join_game(self, interaction: Interaction, btn: ui.Button):
        # await interaction.response.defer()
        if self.cog.games[interaction.guild.id]["participants"].get(interaction.user.id, None):
            return await interaction.send("You are already in this game.", ephemeral=True)
        self.cog.games[interaction.guild_id]["participants"][interaction.user.id] = Player(interaction.user)
        await interaction.send("Joined the game.", ephemeral=True)

    @ui.button(label="Start", style=ButtonStyle(1))
    async def start_game(self, interaction: Interaction, btn: ui.Button):
        # await interaction.response.defer()
        if self.cog.games[interaction.guild_id]["start_by"] != interaction.user.id:
            return await interaction.send(
                "Only the person who ran the command to start this quiz can begin it early.",
                ephemeral=True,
            )
        if len(self.cog.games[interaction.guild_id]["participants"]) < 1:
            return await interaction.send("There are no players in this game!", ephemeral=True)
        self.cog.games[interaction.guild_id]["active"] = True
        await interaction.send("Starting quiz!", ephemeral=True)
        self.stop()
        self.cog.bot.dispatch("quiz_start", interaction.guild_id, interaction.user.id)


class Answers(ui.View):
    def __init__(self, cog: commands.Cog, guild: Guild, answers: int, qnum: int, **kwargs):
        self.qnum: int = qnum
        self.answered = {}
        self.participating = [u.user.id for u in cog.games[guild.id].participants.values()]
        self.cog = cog
        self.guild = guild
        kwargs.setdefault("timeout", 15)
        super().__init__(**kwargs)
        for i, l in enumerate("ABCD"[: len(answers)]):
            self.add_item(Answer(0, answers[i], label=l))

    #        self.add_item(Leave(cog))

    #    async def all_done(self):
    #        if set(self.answered) == set(self.participating):
    #            await self.end()

    async def on_timeout(self):
        await self.end()

    async def end(self):
        self.stop()
        self.cog.bot.dispatch("next_question", self.guild.id, self.qnum, self.answered)
        return self.answered


class ShowAnswers(ui.View):
    def __init__(self, answers: list, ind_correct: int, **kwargs):
        super().__init__(**kwargs)
        for i, l in enumerate("ABCD"[: len(answers)]):
            self.add_item(Answer(1 if i == ind_correct else -1, label=l))


class AcceptSuggestion(ui.View):
    def __init__(
        self,
        bot: QuizBot,
        suggester_id: int,
        question: str,
        category: str,
        correct: str,
        wrong_one: str,
        wrong_two="null",
        wrong_three="null",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.bot = bot
        self.category = category
        self.question = question
        self.correct = correct
        self.wrong_one = wrong_one
        self.wrong_two = wrong_two
        self.wrong_three = wrong_three
        self.suggester_id = suggester_id

    @ui.button(label="Yes", style=ButtonStyle(3))
    async def yes(self, interaction: Interaction, btn: ui.Button):
        if interaction.user.id != 642416218967375882:
            return await interaction.send("no ty :)", ephemeral=True)
        async with self.bot.db.cursor() as c:
            await c.execute(
                "INSERT INTO questions(category, question, correct, wrong_one, wrong_two, wrong_three) VALUES (?, ?, ?, ?, ?)",
                (self.category, self.question, self.correct, self.wrong_one, self.wrong_two, self.wrong_three),
            )
        await self.bot.db.commit()
        await interaction.send(
            embed=self.bot.Embed(
                title="Question Added",
                description=f"Added `{self.question}` to the list of questions.",
            )
            .add_field(name="Correct Answer", value=f"• {self.correct}")
            .add_field(
                name="Wrong Answers",
                value=f"• {self.wrong_one}\n• {self.wrong_two}\n• {self.wrong_three}",
            ),
            ephemeral=True,
        )
        em = self.bot.Embed(
            title="Suggestion Accepted",
            description=f"A developer has accepted your suggestion for {self.bot.mention}.",
        )
        em.add_field(name="Question", value=f"{self.question}")
        em.add_field(name="Correct Answer", value=f"{self.correct}")
        em.add_field(
            name="Wrong Answers",
            value=f"{self.wrong_one}\n{self.wrong_two}\n{self.wrong_three}",
        )
        try:
            await self.bot.get_user(self.suggester_id).send(embed=em)
        except:
            pass
        self.stop()

    @ui.button(label="No", style=ButtonStyle(4))
    async def no(self, interaction: Interaction, btn: ui.Button):
        await interaction.send("Suggestion not accepted.")
        embed = self.bot.Embed(
            title="Suggestion not accepted",
            description=f"Your Suggestion for {self.bot.user.mention} was not accepted.",
        )
        embed.add_field(name="Suggested Question", value=f"{self.question}")
        embed.add_field(name="Correct Answer", value=f"{self.correct}")
        embed.add_field(
            name="Wrong Answers",
            value=f"{self.wrong_one}\n{self.wrong_two}\n{self.wrong_three}",
        )
        try:
            await self.bot.get_user(self.suggester_id).send(embed=embed)
        except:
            pass
        self.stop()
