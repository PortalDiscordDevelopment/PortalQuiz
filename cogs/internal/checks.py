import discord


def is_owner():
    async def check(interaction: discord.Interaction):
        bot = interaction.client
        if await bot.is_owner(interaction.user):
            return True
        raise discord.app_commands.CheckFailure(f"You must own this bot to run {interaction.command.name}.")

    return discord.app_commands.check(check)
