import discord
import DPyUtils
from discord.ext import commands


class Logging(commands.Cog):
    """
    Logs bot stuff.
    """

    def __init__(self, bot: DPyUtils.Bot):
        self.bot = bot

    @commands.Cog.listener("on_guild_join")
    @commands.Cog.listener("on_guild_remove")
    async def on_guild_join(self, guild: discord.Guild):
        c = self.bot.get_channel(922487263630327838)
        jl = "Joined" if self.bot.get_guild(guild.id) else "Left"
        await c.send(
            f"{jl} {guild}, Owner: {guild.owner}\nTotal: {len(self.bot.guilds)}"
        )

    @commands.Cog.listener()
    async def on_command(self, ctx: DPyUtils.Context):
        c = self.bot.get_channel(922487264775385118)
        if ctx.command.qualified_name.split()[0] == "jishaku":
            return
        await c.send(
            f"{ctx.author} ran `{ctx.command}` in {ctx.guild}\nFull message: `{ctx.message.content}`"
        )


def setup(bot: DPyUtils.Bot):
    bot.add_cog(Logging(bot))
