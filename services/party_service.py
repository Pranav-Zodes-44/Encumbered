from services import mongo, dto

async def get_party_gold(party_name: str):
    gold = await mongo.find_one({"name": "Gold"}, party_name)

    if (gold == None):
        await mongo.insert_one(dto.ItemDto(name="Gold", rarity="Gold"), party_name)
        gold = await mongo.find_one({"name": "Gold"}, party_name)

    del gold["_id"]
    
    return dto.ItemDto(**gold)

async def set_party_gold(party_name: str, new_party_gold: dto.PartyGoldDto):
    await mongo.update_one({"name": "Gold"}, {"value": new_party_gold.__dict__}, party_name)