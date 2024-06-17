import discord
from services import user_service, mula_service, embed_service, dto, message_service
from copy import copy


class MulaCommands(discord.app_commands.Group):
	...
	bot: discord.Client

	def __init__(self, name, description, bot):
		super(MulaCommands, self).__init__(name=name, description=description)
		self.bot = bot

	@discord.app_commands.command(
			name="get",
			description="Get the current amount of gold your party has"
	)
	async def slash_party_gold(
		self,
		interaction: discord.Interaction
	):
		user = await user_service.get_or_insert_user(interaction.user.id)

		has_party = await user_service.check_user_party(user, interaction)

		if (has_party):
			gold = await mula_service.get_party_gold(user.currentParty)
			
			embed = embed_service.get_gold_embed(dto.PartyGoldDto(**gold.value), user, interaction)
			await interaction.response.send_message(embed=embed)


	@discord.app_commands.command(
		name="add",
		description="Add money to your party"
	)
	async def slash_add_party_gold(
		self,
		interaction: discord.Interaction,
		pp: int = 0,
		gp: int = 0,
		sp: int = 0,
		cp: int = 0
	):
		user = await user_service.get_or_insert_user(interaction.user.id)

		has_party = await user_service.check_user_party(user, interaction)

		if (has_party):
			gold_item = await mula_service.get_party_gold(user.currentParty)
			current_gold = dto.PartyGoldDto(**gold_item.value)

			gold_change = dto.PartyGoldDto(
				pp=pp,
				gp=gp,
				sp=sp,
				cp=cp
			)
			
			await interaction.response.send_message(f"Doing the calculations :brain:")

			new_gold = mula_service.add_mula(copy(current_gold), gold_change)

			embed = embed_service.get_gold_embed(current_gold, user, interaction, new_gold)
			message = await interaction.channel.send(embed=embed)
			await message_service.party_money_change(message, user, interaction, new_gold, self.bot)


	@discord.app_commands.command(
		name="minusmula",
		description="Remove money from party"
	)
	async def slash_minus_mula(
		self,
		interaction: discord.Interaction,
		pp: int = 0,
		gp: int = 0,
		sp: int = 0,
		cp: int = 0
	):
		user = await user_service.get_or_insert_user(interaction.user.id)

		has_party = await user_service.check_user_party(user, interaction)

		if (has_party):
			gold_item = await mula_service.get_party_gold(user.currentParty)
			current_gold = dto.PartyGoldDto(**gold_item.value)

			gold_change = dto.PartyGoldDto(
				pp=pp,
				gp=gp,
				sp=sp,
				cp=cp
			)

			await interaction.response.send_message("Taking the money from the party bank :ninja:")

			new_gold = mula_service.minus_mula(copy(current_gold), gold_change)
			
			embed = embed_service.get_gold_embed(current_gold, user, interaction, new_gold)
			message = await interaction.channel.send(embed=embed)
			await message_service.party_money_change(message, user, interaction, new_gold, self.bot)


	@discord.app_commands.command(
		name="set",
		description="Set the gold of your current party"
	)
	async def slash_set_gold(
		self,
		interaction: discord.Interaction,
		pp: int = 0,
		gp: int = 0,
		sp: int = 0,
		cp: int = 0
	):
		user = await user_service.get_or_insert_user(interaction.user.id)

		has_party = await user_service.check_user_party(user, interaction)

		if (has_party):
			new_party_gold = dto.PartyGoldDto(
				pp=pp,
				gp=gp,
				sp=sp,
				cp=cp
			)

			await interaction.response.send_message(f'Getting gold for {user.currentParty} :timer:')

			current_party_gold = await mula_service.get_party_gold(user.currentParty)

			embed = embed_service.get_gold_embed(dto.PartyGoldDto(**current_party_gold.value), user, interaction, new_party_gold)

			message = await interaction.channel.send(embed=embed)
			await message_service.party_money_change(message, user, interaction, new_party_gold, self.bot)
