from dataclasses import dataclass

import discord


@dataclass
class Player:
    """
    Player class.
    """

    def __init__(self, user: discord.Member):
        self.user = user
        self.score: int = 0
        self.up_by: int = 0
        self.answered: int = 0
        self.unanswered: int = 0


@dataclass
class Game:
    """
    Game class.
    """

    def __init__(self, interaction: discord.Interaction):
        self.active = True
        self.start_by = interaction.user.id
        self.participants = {}
        self.guild = interaction.guild
        self.current_view: discord.ui.View

    async def end(self):
        self.active = False
        await self.current_view.end()
