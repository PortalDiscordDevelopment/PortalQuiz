"""
Winter Hackathon entry for Portal Development
"""
import asyncio
import os
import traceback

import aiohttp
import aiosqlite
import discord
import dotenv
import DPyUtils
import PortalUtils
from discord.ext import commands

from schemas import schemas

dotenv.load_dotenv(verbose=True)


class QuizBot(PortalUtils.Bot):
    """
    Main bot class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: aiosqlite.Connection
        self.session: aiohttp.ClientSession
        self.version = 2.1

    async def start(self, *args, **kwargs):
        async with aiosqlite.connect("data.db") as db:
            self.db = db
            for schema in schemas:
                try:
                    await db.execute(schema)
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
            await super().start(*args, **kwargs)


bot = QuizBot(
    command_prefix=commands.when_mentioned_or("b*"),
    intents=discord.Intents(**{k: v for k, v in dict(discord.Intents.all()).items() if k not in ("presences")}),
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
    activity=discord.Game(name="my own quiz"),
)


async def main():
    await DPyUtils.load_extensions(bot)
    async with bot:
        await bot.start(os.getenv("QUIZBOT_TOKEN"))


discord.utils.setup_logging(level=20)
asyncio.run(main(), debug=True)
