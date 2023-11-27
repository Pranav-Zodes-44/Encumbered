from services import dto
from discord import Embed, Interaction

icons: dict = {
    "gold": "<:gold:1178765750153007224>",
    "silver": "<:silver:1178765685871083561>",
    "copper": "<:copper:1178765620762906754>",
    "electrum": "<:electrum:1178765784605003827>",
    "platinum": "<:platinum:1178765817983279124>"
}

def get_gold_embed(
        party_gold: dto.PartyGoldDto, 
        user: dto.UserDto, 
        interaction: Interaction, 
        new_party_gold: dto.PartyGoldDto = None
):
    description: str = f"Current gold for {user.currentParty} requested by {interaction.user.mention}"

    if (new_party_gold is not None):
        description = description.replace("Current", "New")

    embed = Embed(title=f"{user.currentParty}: Gold", description=description, colour=0xD4AF37)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1176583186587865239/1178762626327650365/Treasure_AFRT.webp?ex=6577533e&is=6564de3e&hm=b47d2c6d33d4dbb70c78d08345d4810994bebd399b6bdc167de867c1663342a5&")

    pp_str = f"{icons['platinum']}: {party_gold.pp}"
    gold_str = f"{icons['gold']}: {party_gold.gp}"
    silver_str = f"{icons['silver']}: {party_gold.sp}"
    copper_str = f"{icons['copper']}: {party_gold.cp}"

    if (new_party_gold is not None):
        pp_str += f" :arrow_right: {new_party_gold.pp}"
        gold_str += f" :arrow_right: {new_party_gold.gp}"
        silver_str += f" :arrow_right: {new_party_gold.sp}"
        copper_str += f" :arrow_right: {new_party_gold.cp}"

    embed.add_field(name="Platinum", value=pp_str, inline=False)
    embed.add_field(name="Gold", value=gold_str, inline=False)
    embed.add_field(name="Silver", value=silver_str, inline=False)
    embed.add_field(name="Copper", value=copper_str, inline=False)

    if (new_party_gold is not None):
        embed.add_field(name="Confirm new change", value="React with 🫡 to confirm the change.", inline=False)

    return embed
