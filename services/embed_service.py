from services import dto
from discord import Embed, Interaction

icons: dict = {
    "gold": "<:gold:1178765750153007224>",
    "silver": "<:silver:1178765685871083561>",
    "copper": "<:copper:1178765620762906754>",
    "electrum": "<:electrum:1178765784605003827>",
    "platinum": "<:platinum:1178765817983279124>"
}

rarity: dict = {
    "common": 0xe8e8e8,
    "uncommon": 0x3BB143,
    "rare":0x007fff,
    "very rare":0x7851A9,
    "legendary":0xDA9100,
    "artifact":0xB80F0A,
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

    pp_str, gold_str, silver_str, copper_str = _get_gold_change(party_gold, new_party_gold)

    embed.add_field(name="Platinum", value=pp_str, inline=False)
    embed.add_field(name="Gold", value=gold_str, inline=False)
    embed.add_field(name="Silver", value=silver_str, inline=False)
    embed.add_field(name="Copper", value=copper_str, inline=False)

    if (new_party_gold is not None):
        embed.add_field(name="Confirm new change", value="React with 🫡 to confirm the change.", inline=False)

    return embed

def get_item_embed(
    item: dto.ItemDto,
    user: dto.UserDto,
    interaction: Interaction,
    updated_item: dto.ItemDto = None
) -> Embed:

    if (updated_item is not None):
        return get_updated_item_embed(item, user, interaction, updated_item)
    else:
        description: str = f"Added {item.quantity} of {item.name} to {user.currentParty} by {interaction.user.mention} :package:"

        embed = Embed(title=f"{user.currentParty}: {item.name}", description=description, colour=rarity[item.rarity])

        item_value = _get_gold_string(item.value)

        embed.add_field(name="Quantity", value=item.quantity, inline=False)
        embed.add_field(name="Weight", value=item.weight, inline=False)
        embed.add_field(name="Rarity", value=item.rarity.capitalize(), inline=False)
        embed.add_field(name="Notes", value=item.notes if item.notes != "" else "None", inline=False)
        embed.add_field(name="Value", value=f"{', '.join(map(str, item_value))}", inline=False)
        
        return embed
    

def get_updated_item_embed(
    item: dto.ItemDto,
    user: dto.UserDto,
    interaction: Interaction,
    updated_item: dto.ItemDto = None
) -> Embed:
    
    description: str = f"{item.name}, updated by {interaction.user.mention}"

    updated_item_value = None

    if (updated_item is not None):
        updated_item_value = updated_item.value
    
    pp_str, gold_str, silver_str, copper_str = _get_gold_change(item.value, updated_item_value)

    weight_str, quantity_str, notes_str, rarity_str = _get_item_change_string(item, updated_item)

    embed = Embed(title=f"{user.currentParty}: {item.name}", description=description, colour=rarity[updated_item.rarity])
    embed.add_field(name="Quantity", value=quantity_str, inline=False)
    embed.add_field(name="Weight", value=weight_str, inline=False)
    embed.add_field(name="Rarity", value=rarity_str, inline=False)
    embed.add_field(name="Notes", value=notes_str, inline=False)
    embed.add_field(name="Value:", value="", inline=False)
    embed.add_field(name="", value=pp_str, inline=False)
    embed.add_field(name="", value=gold_str, inline=False)
    embed.add_field(name="", value=silver_str, inline=False)
    embed.add_field(name="", value=copper_str, inline=False)

    return embed


def _get_gold_change(
    old_gold: dto.PartyGoldDto,
    new_gold: dto.PartyGoldDto = None,
) -> tuple[str, str, str, str]:
    pp_str, gold_str, silver_str, copper_str = _get_gold_string(old_gold)

    if (new_gold is not None):
        pp_str += f" :arrow_right: {new_gold.pp}"
        gold_str += f" :arrow_right: {new_gold.gp}"
        silver_str += f" :arrow_right: {new_gold.sp}"
        copper_str += f" :arrow_right: {new_gold.cp}"
    
    return pp_str, gold_str, silver_str, copper_str


def _get_gold_string(
        gold: dto.PartyGoldDto
) -> tuple[str, str, str, str]:
    pp_str = f"{icons['platinum']}: {gold.pp}"
    gold_str = f"{icons['gold']}: {gold.gp}"
    silver_str = f"{icons['silver']}: {gold.sp}"
    copper_str = f"{icons['copper']}: {gold.cp}"

    return pp_str, gold_str, silver_str, copper_str


def _get_item_change_string(
    old_item: dto.ItemDto,
    new_item: dto.ItemDto
) -> tuple[str, str, str]:
    
    rarity_str = old_item.rarity.capitalize()
    if (new_item.rarity != old_item.rarity):
        rarity_str = f"{old_item.rarity.capitalize()} :arrow_right: {new_item.rarity.capitalize()}"

    weight_str = f"{old_item.weight} :arrow_right: {new_item.weight}"
    quantity_str = f"{old_item.quantity} :arrow_right: {new_item.quantity}"
    notes_str = f"{old_item.notes} :arrow_right: {new_item.notes}"

    if (old_item.notes == "" and new_item.notes == ""):
        notes_str = "None"

    if (old_item.notes == new_item.notes):
        notes_str = new_item.notes

    return weight_str, quantity_str, notes_str, rarity_str