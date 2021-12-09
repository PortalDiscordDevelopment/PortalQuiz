import discord
from discord.ext import commands
from .classes import Player


class Answer(discord.ui.Button):
    def __init__(self, _type: int = 0, answer: str = "", **kwargs):
        bkey = {-1: 4, 0: 1, 1: 3}
        kwargs.update(style=discord.ButtonStyle(bkey[_type]), disabled=_type != 0)
        self.answer = answer
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction):
        self.view.ans = self.label
        self.view.answered.append(interaction.user.id)
        await interaction.response.send_message(
            f"Answered: {self.answer}", ephemeral=True
        )
        await self.view.all_done()
        gdat = self.cog.games.get(interaction.guild_id, None)
        user = gdat["participants"].get(interaction.user.id, None)
        user.active = False


class Leave(discord.ui.Button):
    def __init__(self, cog: commands.Cog, **kwargs):
        kwargs.update(style=discord.ButtonStyle(4), label="Leave")
        super().__init__(**kwargs)
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        gdat = self.cog.games.get(interaction.guild_id, None)
        if not gdat:
            return
        user = gdat["participants"].get(interaction.user.id, None)
        if not user:
            return await interaction.followup.send(
                "You are not in this game.", ephemeral=True
            )
        if not gdat["active"]:
            gdat["participants"].pop(user.user.id)
            if not gdat["participants"]:
                await interaction.followup.send("The game has been termiminated due to a lack of players.")
                await self.cog.end_game(gdat)
                #not even sure if this exists but i didn't code this so im assuming this exists but again i didn't code this so clari pls tutorial thx
        else:
            user.active = False
        await interaction.followup.send(f"{user.user} has left the game.")

class ShowAnswers(discord.ui.View):
    def __init__(self, answers: list, ind_correct: int, **kwargs):
        for i, l in enumerate("ABCD"[:len(answers)]):
            self.add_item(Answer(1 if i == ind_correct else -1, label=l))
        super().__init__(**kwargs)

class ShowAnswers(discord.ui.View):
    def __init__(self, answers: list, ind_correct: int, **kwargs):
        for i, l in enumerate("ABCD"[:len(answers)]):
            self.add_item(Answer(1 if i == ind_correct else -1, label=l))
        super().__init__(**kwargs)


class JoinStartLeave(discord.ui.View):
    def __init__(self, cog: commands.Cog, totalq: int, **kwargs):
        self.totalq = totalq
        self.cog = cog
        kwargs.setdefault("timeout", 300)
        super().__init__(**kwargs)
        self.children.insert(1, Leave(self.cog))

    @discord.ui.button(label="Join", style=discord.ButtonStyle(3))
    async def join_game(self, btn: discord.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.cog.games[interaction.guild.id]["participants"].get(
            interaction.user.id, None
        ):
            return await interaction.followup.send(
                "You are already in this game.", ephemeral=True
            )
        self.cog.games[interaction.guild_id]["participants"][
            interaction.user_id
        ] = Player(interaction.user, self.totalq)
        await interaction.followup.send_message(
            f"{interaction.user.mention} joined the game."
        )

    @discord.ui.button(label="Start", style=discord.ButtonStyle(1))
    async def start_game(self, btn: discord.Button, interaction: discord.Interaction):
        await interaction.response.defer()
<<<<<<< HEAD
        if self.cog.games[interaction.guild_id]["start_by"] != interaction.user.id:
            return await interaction.followup.send(
                "Only the person who ran the command to start this quiz can begin it early.",
                ephemeral=True,
            )
        if len(self.cog.games[interaction.guild_id]["participants"]) < 1:
            return await interaction.followup.send(
                "There are no players in this game!", ephemeral=True
            )
        self.cog.games[interaction.guild_id]["active"] = True
        await interaction.followup.send("Starting quiz!", ephemeral=True)
        self.stop()
        self.cog.bot.dispatch("quiz_start", interaction.guild_id, interaction.user.id)


class Answers(discord.ui.View):
    def __init__(
        self, cog: commands.Cog, guild: discord.Guild, answers: int, qnum: int, **kwargs
    ):
        self.ans: str = ""
        self.qnum: int = qnum
        self.answered = []
        self.answer_data = {}
        self.participating = [
            u.user.id for u in cog.games[guild.id]["participants"].values()
        ]
        self.cog = cog
        self.guild = guild
        kwargs.setdefault("timeout", 60)
        super().__init__(**kwargs)
        for i, l in enumerate("ABCD"[: len(answers)]):
            self.add_item(Answer(0, answers[i], label=l))
        self.add_item(Leave(cog))

    async def all_done(self):
        if set(self.answered) == set(self.participating):
            self.stop()
            self.cog.bot.dispatch(
                "next_question", self.guild.id, self.qnum, self.answer_data
            )


class ShowAnswers(discord.ui.View):
    def __init__(self, answers: list, ind_correct: int, **kwargs):
        super().__init__(**kwargs)
        for i, l in enumerate("ABCD"[: len(answers)]):
            self.add_item(Answer(1 if i == ind_correct else -1, label=l))
=======
        if self.cog.games[interaction.guild_id]["start_by"] == interaction.user_id:
            self.cog.games[interaction.guild_id]["active"] = True
        await interaction.followup.send_message("Quiz starting now!")
        self.stop()
>>>>>>> ee60bdb (No message specified)
