import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio
from services import dto, mula_service, user_service, embed_service, item_service, message_service
from copy import copy

load_dotenv()
TOKEN = os.getenv('TOKEN')

GUILD_IDS = [1121424199576191016, 1178763010140020836, 1181656816753586267]
INTENTS = discord.Intents.all() 
BOT = commands.Bot(command_prefix=commands.when_mentioned_or("!!"), intents=INTENTS, debug_guilds = GUILD_IDS)

@BOT.event
async def on_ready():
	await BOT.tree.sync()
	print("Bot connected.")

@BOT.tree.command(
	name="getmula",
	description="Tracks the party gold"
)
async def slash_party_gold(
	interaction: discord.Interaction
):
	user = await user_service.get_or_insert_user(interaction.user.id)

	has_party = await user_service.check_user_party(user, interaction)

	if (has_party):
		gold = await mula_service.get_party_gold(user.currentParty)
		
		embed = embed_service.get_gold_embed(dto.PartyGoldDto(**gold.value), user, interaction)
		await interaction.response.send_message(embed=embed)

@BOT.tree.command(
	name="addmula",
	description="Add money to party"
)
async def slash_add_party_gold(
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
		await party_money_change(message, user, interaction, new_gold)


@BOT.tree.command(
		name="minusmula",
		description="Remove money from party"
)
async def slash_minus_mula(
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
		await party_money_change(message, user, interaction, new_gold)


@BOT.tree.command(
	name="setparty",
	description="Set your current party to an existing or new party"
)
async def slash_set_party(
	interaction: discord.Interaction,
	name: str
):
	discord_user = interaction.user

	await user_service.set_party(discord_user.id, name)

	await interaction.response.send_message(f"Set party to `{name}` for {discord_user.mention}")

@BOT.tree.command(
	name="getparty",
	description="Get your currently set party"
)
async def slash_get_party(
	interaction: discord.Interaction,
):
	discord_user = interaction.user

	party = await user_service.get_party(discord_user.id)

	if (party == ""):
		await interaction.response.send_message(f"You currently have no party set. Please use **/setparty** do so :troll:.")
	else:
		await interaction.response.send_message(f"Your current party is **{party}**, {discord_user.mention} :people_wrestling:")


@BOT.tree.command(
	name="setmula",
	description="Set the gold of your current party"
)
async def slash_set_gold(
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
		await party_money_change(message, user, interaction, new_party_gold)


@BOT.tree.command(
	name="additem",
	description="Add an item to your party's inventory"
)
@app_commands.choices( 
	rarity =
		[
			app_commands.Choice(name="Common", value="common"),
			app_commands.Choice(name="Uncommon", value="uncommon"),
			app_commands.Choice(name="Rare", value="rare"),
			app_commands.Choice(name="Very Rare", value="very rare"),
			app_commands.Choice(name="Legendary", value="legendary"),
			app_commands.Choice(name="Artifact", value="artifact")
		]
)
async def slash_add_item(
	interaction: discord.Interaction,
	name: str,
	rarity: app_commands.Choice[str],
	weight: int,
	quantity: int,
	pp: int,
	gp: int,
	sp: int,
	cp: int,
	notes: str = ""
):
	if (quantity < 1):
		await interaction.response.send_message("Quantity cannot be 0 for an item that you are adding!")
		return
	
	if (name.lower() == "gold"):
		await interaction.response.send_message("Please use any of the 'mula' commands to deal with the party gold :moneybag:")
		return
	
	user = await user_service.get_or_insert_user(interaction.user.id)
	
	has_party = await user_service.check_user_party(user, interaction)

	if (has_party):

		new_item = dto.ItemDto(
			name = name,
			rarity = rarity.value,
			notes = notes,
			weight = weight,
			value = dto.PartyGoldDto(
				pp=pp,
				gp=gp,
				sp=sp,
				cp=cp
			),
			quantity = quantity
		)

		await interaction.response.send_message(f"Adding {new_item.name} to {user.currentParty} :inbox_tray:")
		item, updated_item = await item_service.create_or_update_item(user.currentParty, new_item)

		embed = embed_service.get_item_embed(item, user, interaction, updated_item)
		message = await interaction.channel.send(embed=embed)

		if (updated_item is not None):
			item = updated_item

		await message_service.confirm_item_add(message, user, interaction, item, BOT, updated_item)


async def party_money_change(
	message: discord.Message, 
	user: dto.UserDto, 
	interaction: discord.Interaction, 
	new_party_gold: dto.PartyGoldDto
):
	await message.add_reaction('🫡')

	try:
		await BOT.wait_for('reaction_add',
						check=lambda reaction, user: reaction.emoji == '🫡' and user.id == interaction.user.id, timeout=15)
	except asyncio.TimeoutError as e:
		await message.delete()
		await interaction.channel.send("Timer expired, please try again.")
		return
	
	await mula_service.set_party_gold(user.currentParty, new_party_gold)

	embed = embed_service.get_gold_embed(new_party_gold, user, interaction)
	await message.clear_reactions()
	await message.edit(content=f"**Successfully updated party gold for {user.currentParty} :money_mouth:**", embed=embed)


BOT.run(TOKEN)