from services import dto, mongo, mula_service

RARITY_OPTIONS = ["Common", "Uncommon", "Rare", "Very Rare", "Legendary", "Artifact"]

async def create_or_update_item(
    party_name: str,
	item: dto.ItemDto,
):
	mongo_item = await mongo.find_one({'name': item.name}, party_name)

	if (mongo_item == None):
		await mongo.insert_one(item_to_dict(item), party_name)
		
		return item, None
	
	del mongo_item["_id"]

	updated_item = get_update_item(dto.ItemDto(**mongo_item), item)
	old_item = dto.ItemDto(**mongo_item)
	old_item.value = old_item.convert_value_to_party_gold_dto()

	return old_item, updated_item


async def remove_rope(
    party_name: str,
	rope_to_remove: dto.ItemDto,
):
	old_rope = get_item(party_name, "Rope")

	if (old_rope is None):
		return None, "You gotta add rope before you take some. Use /addrope to get started"

	new_rope_length = old_rope.quantity - rope_to_remove.quantity

	if (new_rope_length < 0):
		return None, "Make sure you got enough rope before you decide to use it!"

	updated_rope = dto.ItemDto(
		name="Rope",
		quantity=new_rope_length
	)

	return updated_rope, "Updated"


async def add_rope(
    party_name: str,
	rope_to_add: dto.ItemDto,
):
	old_rope = get_item(party_name, "Rope")
	
	new_length = rope_to_add.quantity

	if (old_rope is not None):
		new_length += old_rope.quantity
	
	updated_rope = dto.ItemDto(
		name="Rope",
		quantity=new_length
	)

	return updated_rope


async def get_item(
	party_name: str,
	item_name: str
) -> dto.ItemDto:
	mongo_item = await mongo.find_one({'name': item_name}, party_name)

	if (mongo_item is not None):
		del mongo_item["_id"]

		return dto.ItemDto(**mongo_item)

	return None


def get_update_item(
	old_item: dto.ItemDto,
	new_item: dto.ItemDto
):
	updated_item = dto.ItemDto(
		name = new_item.name,
		value = mula_service.add_mula(old_item.convert_value_to_party_gold_dto(), new_item.value),
		rarity = new_item.rarity,
		notes = update_notes(old_item.notes, new_item.notes),
		weight = old_item.weight + new_item.weight,
		quantity = old_item.quantity + new_item.quantity
	)

	return updated_item


async def update_item(
	party_name: str,
	item: dto.ItemDto
):
	await mongo.update_one({"name": item.name}, item_to_dict(item), party_name) 


def update_notes(
	old_notes: str,
	new_notes: str
):
	if (new_notes == "" or new_notes != old_notes):
		return old_notes

	return f"{old_notes} | {new_notes}"


def item_to_dict(item: dto.ItemDto) -> dict:
    item_dict = item.__dict__.copy()  # Convert ItemDto to dictionary

    # Convert nested PartyGoldDto to dictionary
    if isinstance(item_dict['value'], dto.PartyGoldDto):
        item_dict['value'] = party_gold_to_dict(item_dict['value'])

    return item_dict


def party_gold_to_dict(party_gold: dto.PartyGoldDto) -> dict:
    return party_gold.__dict__