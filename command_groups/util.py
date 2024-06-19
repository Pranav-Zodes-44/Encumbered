import discord

class UtilCommands(discord.app_commands.Group):
    ...

    bot: discord.Bot

    def __init__(self, name, description, bot):
        super(UtilCommands, self).__init__(name=name, description=description)
        self.bot = bot


    @discord.app_commands.command(
        name="purge",
        description="Purge bot messages"
    )
    async def slash_purge_admin(
        self,
        interaction: discord.Interaction,
        limit: int = 100
    ):
        if interaction.user.id != 251302176192856074:
            await interaction.channel.send(content="You do not have permission to use this command, please contact @Zodes to use it.", mention_author=True)
            return

        def is_bot(m: discord.Message):
            return m.author.id == self.bot.user.id
        
        await interaction.response.defer()
        
        deleted = await interaction.channel.purge(limit=limit+1, check=is_bot)

        await interaction.channel.send(content=f"Successfully deleted {len(deleted)} messages from {interaction.guild} - {interaction.channel.mention}.")
