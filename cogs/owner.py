"""owner-only commands"""
import os
import DPyUtils
from discord.ext import commands
import json
from cogs.internal.views import Version
import datetime
from pytz import timezone


class Owner(
    commands.Cog,
    command_attrs={"slash_command_guilds": os.getenv("SLASH_GUILDS").split("|")},
):
    def __init__(self, bot: DPyUtils.Bot):
        self.bot = bot

    @commands.command(name="addq")
    @commands.is_owner()
    async def addq(
        self,
        ctx: DPyUtils.Context,
        question: str = commands.Option(description="Question to ask"),
        correct: str = commands.Option(description="The correct answer"),
        wrong_one: str = commands.Option(description="Wrong answer #1"),
        wrong_two: str = commands.Option(description="Wrong answer #2", default="null"),
        wrong_three: str = commands.Option(
            description="Wrong answer #3", default="null"
        ),
    ):
        """
        Add a question to the list of questions.
        """
        if ctx.author.id != 642416218967375882:
            return await ctx.send("no ty :)", ephemeral=True)
        async with self.bot.db.cursor() as c:
            await c.execute(
                "INSERT INTO questions(question, correct, wrong_one, wrong_two, wrong_three) VALUES (?, ?, ?, ?, ?)",
                (question, correct, wrong_one, wrong_two, wrong_three),
            )
        await self.bot.db.commit()
        await ctx.send(
            embed=self.bot.Embed(
                title="Question Added",
                description=f"Added `{question}` to the list of questions.",
            )
            .add_field(name="Correct Answer", value=f"• {correct}")
            .add_field(
                name="Wrong Answers",
                value=f"• {wrong_one}\n• {wrong_two}\n• {wrong_three}",
            ),
            ephemeral=True,
        )
    @commands.command(name="setversion")
    @commands.is_owner()
    async def setversion(self, ctx: DPyUtils.Context, version: str):
        """
        Set the Version of the Bot
        """
        here = timezone('America/New_York')
        date_time = datetime.datetime.now(here)
        embed = self.bot.Embed(title="Confirmation", description = f"Are you sure you want to set the version to {version}?")
        embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
        embed.timestamp = date_time
        v = Version(version)
        await ctx.send(embed=embed, view=v)



def setup(bot: DPyUtils.Bot):
    bot.add_cog(Owner(bot))
