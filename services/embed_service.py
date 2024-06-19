from services import dto, transaction_service
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
    embed.add_field(name="Notes", value=notes_str, inline=False)
    embed.add_field(name="Weight", value=weight_str, inline=False)
    embed.add_field(name="Rarity", value=rarity_str, inline=False)
    embed.add_field(name="Value:", value="", inline=False)
    embed.add_field(name="", value=pp_str, inline=False)
    embed.add_field(name="", value=gold_str, inline=False)
    embed.add_field(name="", value=silver_str, inline=False)
    embed.add_field(name="", value=copper_str, inline=False)

    return embed

def get_rope_embed(
    new_rope: dto.ItemDto,
    user: dto.UserDto,
    interaction: Interaction,
    updated_rope: dto.ItemDto = None,
    change_type: str = ""
):
    embed = Embed(title=f"{user.currentParty}: Rope :knot:", colour=0x43270F)

    description: str = f"{user.currentParty}'s rope collection"

    length_str = f"{new_rope.quantity}ft"

    if (change_type != "" and updated_rope != None):
        old_length = (updated_rope.quantity - new_rope.quantity) if change_type == "add" else (updated_rope.quantity + new_rope.quantity)

        description = f"{new_rope.quantity}ft of rope, {change_type}ed by {interaction.user.mention}"

        length_str = f"{old_length} :arrow_right: {updated_rope.quantity}"

    embed.description = description
    
    embed.set_image(url="https://cdn.discordapp.com/attachments/1178763011226337374/1250148497164992582/80368935_2948706871814793_2924688968400240640_n.jpg?ex=6669e304&is=66689184&hm=2dc7199648a9ad0ad59c1062119308cb1c5c2f7a3a1f5437d8ae4f0184a41562&")

    embed.add_field(name="Length", value=length_str)

    return embed


def get_transaction_embed(
    user: dto.UserDto,
    interaction: Interaction,
    transactions: list[dto.TransactionDto]
):
    embed = Embed(title=f"{user.currentParty}: Transactions :bank:", colour=0x355E3B)
    embed.add_field(name="Legend", value=":pencil2: - Set mula", inline=False)
    embed.add_field(name="", value=":inbox_tray: - Add mula", inline=False)
    embed.add_field(name="", value=":outbox_tray: - Minus mula", inline=False)
    embed.add_field(name="", value="", inline=False)

    transaction_data = transaction_service.get_transaction_strings(transactions)

    embed.add_field(name="Transactions", value="", inline=False)

    for transaction in transaction_data:
        embed.add_field(name="", value=transaction, inline=False)

    embed.add_field(name="", value="", inline=False)
    

    embed.set_footer(text=f"Requested by @{interaction.user.display_name} || Member of {user.currentParty}")

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