from services import mongo, dto

async def get_party_gold(party_name: str):
    gold = await mongo.find_one({"name": "Gold"}, party_name)

    if (gold == None):
        await mongo.insert_one(dto.ItemDto(name="Gold", rarity="Gold"), party_name)
        gold = await mongo.find_one({"name": "Gold"}, party_name)

    del gold["_id"]
    
    return dto.ItemDto(**gold)