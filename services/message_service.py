import discord
from services import dto, embed_service, item_service, mula_service
import asyncio

async def confirm_item_add(
	message: discord.Message,
	user: dto.UserDto,
	interaction: discord.Interaction,
	item: dto.ItemDto,
	bot: discord.Client,
	updated_item: dto.ItemDto
):
	await message.add_reaction('🫡')

	react_message = await interaction.channel.send(f"React with 🫡 to confirm inventory changes")

	try:
		await bot.wait_for('reaction_add',
						check=lambda reaction, user: reaction.emoji == '🫡' and user.id == interaction.user.id, timeout=15)
	except asyncio.TimeoutError as e:
		await react_message.delete()
		await message.delete()
		await interaction.channel.send("Timer expired, please try again.")
		return
	
	await react_message.delete()
	
	if (updated_item is not None):
		await item_service.update_item(user.currentParty, item)

	embed = embed_service.get_item_embed(item, user, interaction)

	await message.clear_reactions()
	await message.edit(content=f"**Successfully added {item.quantity} {item.name}(s) for {user.currentParty} :package:**", embed=embed)

async def update_rope(
	message: discord.Message,
	user: dto.UserDto,
	interaction: discord.Interaction,
	new_rope: dto.ItemDto,
	change_length: int,
	add: bool,
	bot: discord.Client,
):
	await message.add_reaction('🪢')

	react_message = await interaction.channel.send(f"React with 🪢 to confirm rope stash changes")

	try:
		await bot.wait_for('reaction_add',
						check=lambda reaction, user: reaction.emoji == '🪢' and user.id == interaction.user.id, timeout=15)
	except asyncio.TimeoutError as e:
		await react_message.delete()
		await message.delete()
		await interaction.channel.send("Timer expired, please try again.")
		return
	
	await react_message.delete()

	await item_service.update_item(user.currentParty, new_rope)

	embed = embed_service.get_rope_embed(new_rope, user, interaction)

	await message.clear_reactions()
	await message.edit(content=f"**Successfully {'added' if add else 'removed'} {change_length}ft rope for {user.currentParty} {':yarn:' if add else ':thread:'}**", embed=embed)

async def party_money_change(
	message: discord.Message, 
	user: dto.UserDto, 
	interaction: discord.Interaction, 
	new_party_gold: dto.PartyGoldDto,
	bot: discord.Client
):
	await message.add_reaction('🫡')

	try:
		await bot.wait_for('reaction_add',
						check=lambda reaction, user: reaction.emoji == '🫡' and user.id == interaction.user.id, timeout=15)
	except asyncio.TimeoutError as e:
		await message.delete()
		await interaction.channel.send("Timer expired, please try again.")
		return
	
	await mula_service.set_party_gold(user.currentParty, new_party_gold)

	embed = embed_service.get_gold_embed(new_party_gold, user, interaction)
	await message.clear_reactions()
	await message.edit(content=f"**Successfully updated party gold for {user.currentParty} :money_mouth:**", embed=embed)