import discord
from discord.ext import commands
from .classes import Player


class Answer(discord.ui.Button):
    def __init__(self, _type: int = 0, **kwargs):
        bkey = {-1: 4, 0: 1, 1: 3}
        kwargs.update(style=discord.ButtonStyle(bkey[_type]), disabled=_type != 0)
        super().__init__(**kwargs)

    async def callback(self, interaction: discord.Interaction):
        self.view.ans = self.label


class Leave(discord.ui.Button):
    def __init__(self, cog: commands.Cog, **kwargs):
        kwargs.update(style=discord.ButtonStyle(4))
        super().__init__(**kwargs)
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        gdat = self.cog.games.get(interaction.guild_id, None)
        if not gdat:
            return
        user = gdat["participants"].get(interaction.user_id, None)
        if not user:
            return
        if not gdat["active"]:
            gdat["participants"].pop(user.id)
        else:
            user.active = False
        await interaction.followup.send(f"{user.name} has left the game.")


class Answers(discord.ui.View):
    def __init__(self, cog: commands.Cog, guild: discord.Guild, lena: int, **kwargs):
        self.ans: str
        self.answered = []
        self.participating = [
            u.user.id for u in cog.games[guild.id]["participants"].values()
        ]
        self.cog = cog
        kwargs.setdefault("timeout", 60)
        super().__init__(**kwargs)
        for l in "ABCD"[:lena]:
            self.add_item(Answer(label=l))
        self.add_item(Leave(cog))

    async def all_done(self):
        if self.answered == self.participating:
            self.stop()


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
        self.cog.games[interaction.guild_id]["participants"][
            interaction.user_id
        ] = Player(interaction.user, totalq)
        await interaction.followup.send_message(
            f"{interaction.user.mention} joined the game."
        )

    @discord.ui.button(label="Start", style=discord.ButtonStyle(1))
    async def start_game(self, btn: discord.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.cog.games[interaction.guild_id]["start_by"] == interaction.user_id:
            self.cog.games[interaction.guild_id]["active"] = True
        await interaction.followup.send_message("Quiz starting now!")
