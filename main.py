import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from services import mongo, dto, user_service, party_service, embed_service

load_dotenv()
TOKEN = os.getenv('TOKEN')

GUILD_IDS = [1121424199576191016, 1178763010140020836]
INTENTS = discord.Intents.all() 
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!!"), intents=INTENTS, debug_guilds = GUILD_IDS)

@bot.event
async def on_ready():
	await bot.tree.sync()
	print("Bot connected.")


@bot.tree.command(
	name="gold",
	description="Tracks the party gold"
)
async def slash_party_gold(
	interaction: discord.Interaction
):
	user = await user_service.get_or_insert_user(interaction.user.id)

	has_party = await user_service.check_user_party(user, interaction)

	if (has_party):
		gold = await party_service.get_party_gold(user.currentParty)
		
		embed = embed_service.get_gold_embed(dto.PartyGoldDto(**gold.value), user, interaction)
		await interaction.response.send_message(embed=embed)


@bot.tree.command(
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
		gold_item = await party_service.get_party_gold(user.currentParty)
		current_gold = dto.PartyGoldDto(**gold_item.value)

		gold_change = dto.PartyGoldDto(
			pp=pp,
			gp=gp,
			sp=sp,
			cp=cp
		)
		new_gold = party_service.add_mula(current_gold, gold_change)
		
		embed = embed_service.get_gold_embed(current_gold, user, interaction, new_gold)
		message = await interaction.channel.send(embed=embed)
		await party_money_change(message, user, interaction, new_gold)

@bot.tree.command(
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


@bot.tree.command(
	name="setgold",
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

		current_party_gold = await party_service.get_party_gold(user.currentParty)

		embed = embed_service.get_gold_embed(dto.PartyGoldDto(**current_party_gold.value), user, interaction, new_party_gold)

		message = await interaction.channel.send(embed=embed)
		await party_money_change(message, user, interaction, new_party_gold)


async def party_money_change(
		message: discord.Message, 
		user: dto.UserDto, 
		interaction: discord.Interaction, 
		new_party_gold: dto.PartyGoldDto
):
	await message.add_reaction('🫡')

	try:
		await bot.wait_for('reaction_add',
						check=lambda reaction, user: reaction.emoji == '🫡' and user.id == interaction.user.id, timeout=15)
	except asyncio.TimeoutError as e:
		await message.delete()
		await interaction.channel.send("Timer expired, please try again.")
	
	await party_service.set_party_gold(user.currentParty, new_party_gold)

	embed = embed_service.get_gold_embed(new_party_gold, user, interaction)
	await message.clear_reactions()
	await message.edit(content=f"**Successfully updated party gold for {user.currentParty} :money_mouth:**", embed=embed)


bot.run(TOKEN)