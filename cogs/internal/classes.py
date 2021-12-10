import discord
from dataclasses import dataclass
from typing import List


@dataclass
class Player:
    """
    Player class.
    """

    def __init__(self, user: discord.Member, totalq):
        self.user = user
        self.active: bool = True
        self.score: int = 0
        self.answered: int = 0
        self.unanswered: int = 0
        self.left: int = totalq
