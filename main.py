import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
from services import dto, user_service, embed_service, item_service, message_service
from command_groups import mula, party, rope, util

load_dotenv()
TOKEN = os.getenv('TOKEN')

GUILD_IDS = [1121424199576191016, 1178763010140020836, 1181656816753586267]
INTENTS = discord.Intents.all() 
BOT = commands.Bot(command_prefix=commands.when_mentioned_or("!!"), intents=INTENTS, debug_guilds = GUILD_IDS)

def init_bot():
	BOT.tree.add_command(mula.MulaCommands(name="mula", description="All commands dealing with your party's money", bot=BOT))
	BOT.tree.add_command(party.PartyCommands(name="party", description="All commands dealing with your party"))
	BOT.tree.add_command(rope.RopeCommands(name="rope", description="All commands dealing with rope", bot=BOT))
	BOT.tree.add_command(util.UtilCommands(name="util", description="Utility commands (some only accessible by admin)", bot=BOT))

@BOT.event
async def on_ready():
	init_bot()
	await BOT.tree.sync()
	print("Bot connected.")

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
	quantity: int,
	weight: int,
	pp: int = 0,
	gp: int = 0,
	sp: int = 0,
	cp: int = 0,
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


if __name__ == "__main__":
	BOT.run(TOKEN)