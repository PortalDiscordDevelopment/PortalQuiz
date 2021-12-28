import DPyUtils
import json
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

        def get_version() -> str:
            with open("data.json", "r") as f:
                return json.loads(f.read())["version"]

        version = get_version()

        await ctx.send(
            embed=self.bot.Embed(
                title="Winter Quiz",
                description=f"""
                    **Stats:**
                    Version: {version}
                    Server Count: {len(self.bot.guilds)} servers
                    Director: Thomas Morton
                    Developers: {', '.join(map(str, map(self.bot.get_user, (642416218967375882, 511655498676699136))))}
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
                description=f"[Click here to invite the bot to your server.]({discord.utils.oauth_url(self.bot.user.id, scopes=('applications.commands', 'bot'), permissions=discord.Permissions(412317240384))})",
            )
        )


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Other(bot))
