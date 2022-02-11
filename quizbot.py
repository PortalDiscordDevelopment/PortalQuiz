"""
Winter Hackathon entry for Portal Development
"""
import os
import aiohttp
import aiosqlite
import discord
import dotenv
import DPyUtils
import PortalUtils
import traceback
from discord.ext import commands
from schemas import schemas
import datetime
from pytz import timezone

dotenv.load_dotenv(verbose=True)


class QuizBot(PortalUtils.Bot):
    """
    Main bot class
    """

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
            if k not in ("presences")
        }
    ),
    owner_ids={
        642416218967375882,
        428903502283014145,
        511655498676699136,
        680801389936508977,
    },
    #    slash_command_guilds=os.getenv("SLASH_GUILDS").split("|"),
    slash_commands=True,
    message_commands=True,
    color=0x34D5E0,
    guild_logs=933694555205824612,
    error_logs=933694555742670878,
    command_logs=933694556266962964,
)

# when joining a server, send a hello message
@bot.listen()
async def on_guild_join(self, guild: discord.Guild):
    here = timezone("America/New_York")
    date_time = datetime.datetime.now(here)
    em = bot.Embed(
        title="Thank You for Inviting!",
        description="Thank you for inviting **Winter Quiz**. To begin, please run `/quiz`. Run `/help` to see information about the other commands.",
    )
    em.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
    em.timestamp = date_time
    bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
    inviter = bot_entry[0].user
    receiver = (
        discord.utils.find(
            lambda c: "staff" in c.name and "chat" in c.name, guild.text_channels
        )
        or inviter
        or guild.owner
        or guild.system_channel
    )
    if receiver:
        await receiver.send(embed=em)
    elif not receiver:
        print(
            "In "
            + guild.name
            + " the owners really messed up, and I can't find a channel to send the message to."
        )
    else:
        print("Really shouldn't be printed")


DPyUtils.load_extensions(bot)

bot.run(os.getenv("QUIZBOT_TOKEN"))
