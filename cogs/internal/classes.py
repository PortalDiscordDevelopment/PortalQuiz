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
        self.total_answered: int = 0
        self.unanswered: int = totalq
        self.right: List[str] = []
        self.wrong: List[str] = []
