import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
print(TOKEN)

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

bot.run(TOKEN)