import discord
from services import dto, mongo

_collection = "users"

async def check_user_party(user: dto.UserDto, interaction: discord.Interaction) -> bool:
    has_party: bool = True

    if (user.currentParty == ""):
        await interaction.response.send_message("Please set your party first using `/setparty` before using any other party commands :)")
        has_party = False
    
    return has_party

async def get_or_insert_user(user_id: int):
    filter = {"userId": user_id}
    user = await mongo.find_one(filter, _collection)

    if (user == None):
        await mongo.insert_one(dto.UserDto(userId=user_id), "users")
        user = await mongo.find_one(filter, _collection)

    del user["_id"]

    return dto.UserDto(**user)

async def set_party(user_id: int, party_name):
    filter = {"userId": user_id}
    
    user = await get_or_insert_user(user_id)

    user_parties = user.parties
    if (party_name not in user_parties):
        user_parties.append(party_name)

    await mongo.update_one(filter, {"currentParty": party_name, "parties": user_parties}, _collection)






