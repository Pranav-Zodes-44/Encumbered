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