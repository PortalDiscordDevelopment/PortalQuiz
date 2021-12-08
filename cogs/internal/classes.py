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
        self.active = True
        self.score = 0
        self.total_answered = 0
        self.right = 0
        self.wrong = 0
        self.unanswered = totalq

    active: bool
    score: int
    total_answered: int
    right: List[str]
    wrong: List[str]
    unanswered: List[str]
