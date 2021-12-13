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
        await interaction.response.defer()
        gdat = self.view.cog.games.get(interaction.guild_id, None)
        user = gdat["participants"].get(interaction.user.id, None)
        if not user or not user.active:
            return await interaction.followup.send(
                "Only players can use this button.", ephemeral=True
            )
        self.view.answered[interaction.user.id] = self.label
        await interaction.followup.send(f"Answered: {self.answer}", ephemeral=True)
        await self.view.all_done()


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
        if not user or not user.active:
            return await interaction.followup.send(
                "You are not in this game.", ephemeral=True
            )
        if hasattr(self.view, "participating"):
            self.view.participating.remove(user.user.id)
        if gdat["active"]:
            user.active = False
            await self.view.all_done()
            await interaction.followup.send(f"{user.user} has left the game.")
        else:
            self.cog.games[interaction.guild.id]["participants"].pop(user.user.id)
            await interaction.followup.send("Joined the game.", ephemeral=True)


# class RejoinPrompt(discord.ui.View):
#     def __init__(self, cog: commands.Cog, user: discord.User, **kwargs):
#         super().__init__(**kwargs)
#         self.cog = cog
#         @discord.ui.button(label="Join", style=discord.ButtonStyle(3))
#         async def rejoin(interaction: discord.Interaction):
#             ...


class JoinStartLeave(discord.ui.View):
    def __init__(self, cog: commands.Cog, totalq: int, **kwargs):
        self.totalq = totalq
        self.cog = cog
        kwargs.setdefault("timeout", 300)
        super().__init__(**kwargs)
        self.add_item(Leave(self.cog))

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
            interaction.user.id
        ] = Player(interaction.user, self.totalq)
        await interaction.followup.send("Joined the game.", ephemeral=True)

    @discord.ui.button(label="Start", style=discord.ButtonStyle(1))
    async def start_game(self, btn: discord.Button, interaction: discord.Interaction):
        await interaction.response.defer()
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
        self.qnum: int = qnum
        self.answered = {}
        self.participating = [
            u.user.id for u in cog.games[guild.id]["participants"].values()
        ]
        self.cog = cog
        self.guild = guild
        kwargs.setdefault("timeout", 30)
        super().__init__(**kwargs)
        for i, l in enumerate("ABCD"[: len(answers)]):
            self.add_item(Answer(0, answers[i], label=l))
        self.add_item(Leave(cog))

    async def all_done(self):
        if set(self.answered) == set(self.participating):
            await self.end()

    async def on_timeout(self):
        await self.end()

    async def end(self):
        self.stop()
        self.cog.bot.dispatch("next_question", self.guild.id, self.qnum, self.answered)


class ShowAnswers(discord.ui.View):
    def __init__(self, answers: list, ind_correct: int, **kwargs):
        super().__init__(**kwargs)
        for i, l in enumerate("ABCD"[: len(answers)]):
            self.add_item(Answer(1 if i == ind_correct else -1, label=l))
