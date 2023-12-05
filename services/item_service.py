from services import mongo, embed_service, dto, user_service

async def create_or_update_item(
    party_name: str,
	item_name: str,
	rarity: str,
	notes: str,
	weight: int,
	quantity: int,
	ddb_link: str
):
	#First find out if the item already exists in the party's inventory
	#If it does, update the weight, quantity, and value to be added to the item and push the updated item.
	#If it doesn't, create item and push item to mongo and return item.
	#Return item and bool (Updated)
	print("f")