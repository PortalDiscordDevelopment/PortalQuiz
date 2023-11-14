"""
Winter Hackathon entry for Portal Development
"""
import asyncio
import os

import dotenv
import DPyUtils
from discord import Game, Intents, utils
from discord.ext import commands

from quizbot import QuizBot

dotenv.load_dotenv(verbose=True)

intents = Intents.all()
intents.presences = False
bot = QuizBot(
    command_prefix=commands.when_mentioned_or("b*"),
    intents=intents,
    owner_ids={
        642416218967375882,
        428903502283014145,
        511655498676699136,
        680801389936508977,
    },
    color=0x34D5E0,
    guild_logs=933694555205824612,
    error_logs=933694555742670878,
    command_logs=933694556266962964,
    activity=Game(name="my own quiz"),
)


async def main():
    await DPyUtils.load_extensions(bot)
    async with bot:
        await bot.start(os.getenv("QUIZBOT_TOKEN"))


utils.setup_logging(level=20)
asyncio.run(main(), debug=True)
