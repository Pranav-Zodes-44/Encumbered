import discord
from discord.ext import commands
from dotenv import load_dotenv
import pymongo
import os

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
    print(interaction.user.id)
    await interaction.response.send_message(f"Adding gold: {gold}")
    
@bot.tree.command(
    name="setparty",
    description="Set your current party to an existing or new party"
)
async def slash_set_party(
    interaction: discord.Interaction,
    name: str
):
    user = interaction.user
    
    await interaction.response.send_message(f"Set party to `{name}` for {user.mention}")


bot.run(TOKEN)