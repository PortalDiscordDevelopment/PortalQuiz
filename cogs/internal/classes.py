from dataclasses import dataclass

import discord


@dataclass
class Question:
    """
    Question class.
    """

    def __init__(self, qid: int, category: str, question: str, correct_answer: str, *wrong_answers: str):
        self.id = qid
        self.category = category
        self.question = question
        self.correct_answer = correct_answer
        self.wrong_answers = tuple(a for a in wrong_answers if a != "null")


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
        self.participants: dict[int, Player] = {}
        self.guild = interaction.guild
        self.current_view: discord.ui.View

    async def end(self):
        self.active = False
        await self.current_view.end()
