import DPyUtils
from discord.ext import commands


class Other(commands.Cog):
    """
    Other commands.
    """

    def __init__(self, bot: DPyUtils.Bot):
        self.bot = bot

    @commands.command(name="info")
    async def info(self, ctx: DPyUtils.Context):
        """
        Shows information about the Bot.
        """
        await ctx.send(
            embed=self.bot.Embed(
                title=f"{self.bot.name} Info",
                description=f"""
                    Server Count: {len(self.bot.guilds)} servers
                    Director: Thomas Morton
                    Developers: {', '.join(map(str, map(self.bot.get_user, (642416218967375882, 511655498676699136, 680801389936508977))))}
                    Framework: [enhanced-discord.py](https://github.com/iDevision/enhanced-discord.py)
                    """.replace(
                    "    ", ""
                ),
            )
        )

    @commands.command(name="invite")
    async def invite(self, ctx: DPyUtils.Context):
        """
        Invite the bot to your server.
        """
        await ctx.send(
            embed=self.bot.Embed(
                title="Invite the bot to your server",
                description="[Click here to invite the bot to your server.]"
                "(https://discord.com/api/oauth2/authorize?"
                "client_id=871981757531050064&permissions=412317240384&"
                "scope=applications.commands%20bot)",
            )
        )


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Other(bot))
