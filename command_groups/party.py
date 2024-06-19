import discord
from services import user_service

class PartyCommands(discord.app_commands.Group):
	...

	@discord.app_commands.command(
		name="set",
		description="Set your current party to an existing or new party"
	)
	async def slash_set_party(
		self,
		interaction: discord.Interaction,
		name: str
	):
		discord_user = interaction.user

		await user_service.set_party(discord_user.id, name)

		await interaction.response.send_message(f"Set party to `{name}` for {discord_user.mention}")


	@discord.app_commands.command(
		name="get",
		description="Get your currently set party"
	)
	async def slash_get_party(
		self,
		interaction: discord.Interaction,
	):
		discord_user = interaction.user

		party = await user_service.get_user_party(discord_user.id)

		if (party == ""):
			await interaction.response.send_message(f"You currently have no party set. Please use **/setparty** do so :troll:.")
		else:
			await interaction.response.send_message(f"Your current party is **{party}**, {discord_user.mention} :people_wrestling:")

