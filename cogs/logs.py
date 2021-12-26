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
        tr = "Total" if self.bot.get_guild(guild.id) else "Remaining"
        embed = self.bot.Embed(title=f"{jl} {guild}")
        embed.set_author(author=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.add_field(name="Owner:", value=guild.owner)
        embed.add_field(name=f"{tr} Servers:", value=len(self.bot.guilds),inline=True)
        embed.add_field(name="Guild ID:", value=f"'{guild.id}'", inline=False)
        embed.add_field(name="Humans:", value=len([m for m in guild.members if not m.bot]),inline=True)
        embed.add_field(name="Bots:", value=len([m for m in guild.members if m.bot]), inline=True)
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
