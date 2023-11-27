import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from services import mongo, dto, user_service

load_dotenv()
TOKEN = os.getenv('TOKEN')

GUILD_IDS = [1121424199576191016]
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
    await interaction.response.send_message("Party Gold = 55g 77sp")
    
@bot.tree.command(
    name="addgold",
    description="Add gold to party"
)
async def slash_add_party_gold(
    interaction: discord.Interaction,
    gold: int
):
    user = await user_service.get_or_insert_user(interaction.user.id)

    has_party = await user_service.check_user_party(user, interaction)

    if (has_party):
        await interaction.response.send_message(f"Adding gold: {gold}")
    
@bot.tree.command(
    name="setparty",
    description="Set your current party to an existing or new party"
)
async def slash_set_party(
    interaction: discord.Interaction,
    name: str
):
    discord_user = interaction.user

    user = await user_service.get_or_insert_user(discord_user.id)
    await user_service.set_party(discord_user.id, name)

    await interaction.response.send_message(f"Set party to `{name}` for {discord_user.mention}")


bot.run(TOKEN)