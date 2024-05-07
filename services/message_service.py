import discord
from services import dto, embed_service, item_service
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