from services import mongo, dto

async def get_party_gold(party_name: str):
	gold = await mongo.find_one({"name": "Gold"}, party_name)

	if (gold == None):
		await mongo.insert_one(dto.ItemDto(name="Gold", rarity="Gold", value=dto.PartyGoldDto().__dict__).__dict__, party_name)
		gold = await mongo.find_one({"name": "Gold"}, party_name)

	del gold["_id"]
	
	return dto.ItemDto(**gold)


async def set_party_gold(party_name: str, new_party_gold: dto.PartyGoldDto):
	await mongo.update_one({"name": "Gold"}, {"value": new_party_gold.__dict__}, party_name)


def add_mula(current_party_gold: dto.PartyGoldDto, gold_change: dto.PartyGoldDto):
	new_party_gold = current_party_gold
	
	new_party_gold.pp += gold_change.pp
	new_party_gold.gp += gold_change.gp
	new_party_gold.sp += gold_change.sp
	new_party_gold.cp += gold_change.cp
	
	return new_party_gold


def minus_mula(current_party_gold: dto.PartyGoldDto, gold_change: dto.PartyGoldDto):
	new_party_gold = current_party_gold

	new_party_gold.pp -= gold_change.pp
	new_party_gold.gp -= gold_change.gp
	new_party_gold.sp -= gold_change.sp
	new_party_gold.cp -= gold_change.cp
	
	return new_party_gold
