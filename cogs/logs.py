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
    async def guild_logs(self, guild: discord.Guild):
        c = self.bot.get_channel(922487263630327838)
        jl,clr = ("Joined", "green") if self.bot.get_guild(guild.id) else ("Left", "red")
        embed = self.bot.Embed(title=f"{jl} {guild}", color=getattr(discord.Color, "dark_"+clr)(),description=f"""
Guild ID: `{guild.id}`
Owner: `{guild.owner}` (`{guild.owner.id}`)
Humans: `{len([m for m in guild.members if not m.bot])}`
Bots: `{len([m for m in guild.members if m.bot])}`
Total Guilds: `{len(bot.guilds)}`""")
        await c.send(embed=embed)

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
