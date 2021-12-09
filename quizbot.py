"""
Winter Hackathon entry for Portal Development
"""
import os
import aiohttp
import aiosqlite
import discord
import dotenv
import DPyUtils
from discord.ext import commands

dotenv.load_dotenv(verbose=True)


class QuizBot(DPyUtils.Bot):
    """
    Main bot class
    """

    def __init__(self, *args, **kwargs):
        self.db: aiosqlite.Connection  # pylint: disable=
        self.session: aiohttp.ClientSession
        super().__init__(*args, **kwargs)

    async def start(self, *args, **kwargs):
        async with aiosqlite.connect(
            "data.db"
        ) as db, aiohttp.ClientSession() as session:
            self.db = db
            self.session = session
            await super().start(*args, **kwargs)

    async def on_message(self, message: discord.Message):
        #        if message.author.bot or message.author.id not in self.owner_ids:
        #            return
        await self.process_commands(message)


# [687429190165069838, 721784188189016226, 720838318857781299]
bot = QuizBot(
    command_prefix=commands.when_mentioned_or("**"),
    intents=discord.Intents(
        **{
            k: v
            for k, v in dict(discord.Intents.all()).items()
            if k not in ("presences", "messages")
        }
    ),
    slash_command_guilds=os.getenv("SLASH_GUILDS").split("|"),
    slash_commands=True,
    message_commands=True,
)


class Embed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = self.color or 0x34D5E0


bot.Embed = Embed

DPyUtils.load_extensions(bot, extra_cogs=["jishaku"])

bot.run(os.getenv("QUIZBOT_TOKEN"))
