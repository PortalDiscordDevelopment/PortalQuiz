import discord
import DPyUtils
from dataclasses import dataclass


@dataclass
class Player:
    """
    Player class.
    """

    def __init__(self, user: discord.Member):
        self.user = user
        self.score: int = 0
        self.answered: int = 0
        self.unanswered: int = 0


@dataclass
class Game:
    """
    Game class.
    """

    def __init__(self, ctx: DPyUtils.Context):
        self.active = True
        self.start_by = ctx.author.id
        self.participants = {}
        self.guild = ctx.guild
        self.current_view: discord.ui.View

    async def end(self):
        self.active = False
        await self.current_view.end()
