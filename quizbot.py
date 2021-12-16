"""
Winter Hackathon entry for Portal Development
"""
import os
import aiohttp
import aiosqlite
import discord
import dotenv
import DPyUtils
import traceback
from discord.ext import commands
from schemas import schemas

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
            for schema in schemas:
                try:
                    await db.execute(schema)
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
            await super().start(*args, **kwargs)

    async def on_message(self, message: discord.Message):
        #        if message.author.bot or message.author.id not in self.owner_ids:
        #            return # Why is this commented out?
        await self.process_commands(message)


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


class CustomMinimalHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        e = self.context.bot.Embed(description="")
        for page in self.paginator.pages:
            e.description += page
        await self.context.send(embed=e)


bot.help_command = CustomMinimalHelp(
    command_attrs={"name": "help", "aliases": ["h", "commands"]},
    verify_checks=False,
)
bot.Embed = Embed

DPyUtils.load_extensions(bot, extra_cogs=["jishaku"])

bot.run(os.getenv("QUIZBOT_TOKEN"))
