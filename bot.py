"""
Winter Hackathon entry for Portal Development
"""

import asyncio
import os

import dotenv
import DPyUtils
import jishaku
from discord import Game, Intents, utils
from discord.ext import commands

import config
from quizbot import QuizBot

dotenv.load_dotenv(verbose=True)

jishaku.Flags.NO_UNDERSCORE = True
jishaku.Flags.HIDE = True

intents = Intents.all()
intents.presences = False
bot = QuizBot(
    command_prefix=commands.when_mentioned_or(config.prefix),
    intents=intents,
    owner_ids=config.owner_ids,
    color=config.color,
    guild_logs=config.guild_logs,
    error_logs=config.error_logs,
    command_logs=config.command_logs,
    activity=Game(name="my own quiz"),
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print(f"Running on {len(bot.guilds)} guilds")


async def main():
    await DPyUtils.load_extensions(bot)
    async with bot:
        await bot.start(os.getenv("QUIZBOT_TOKEN"))


utils.setup_logging(level=20)
asyncio.run(main(), debug=True)
