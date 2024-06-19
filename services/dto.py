from dataclasses import field
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from typing import List, Dict

class UserDto(BaseModel):
	userId: int
	currentParty: str = ""
	parties: List[str] = field(default_factory=list)


class PartyGoldDto(BaseModel):
    pp: int = 0
    gp: int = 0
    sp: int = 0
    cp: int = 0

class ItemDto(BaseModel):
    name: str = "None"
    value: PartyGoldDto = PartyGoldDto()
    rarity: str = "None"
    notes: str = "None"
    weight: int = 0
    quantity: int = 1


class TransactionDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ObjectId = Field(
        alias="_id",
        description="The document unique identifier in MongoDB"
    )
    name: str = "transaction"
    method: str = ""
    original_gold: PartyGoldDto = PartyGoldDto()
    gold_change: PartyGoldDto = PartyGoldDto()

    def get_gold_change_string_list(self):
        return self.gold_change.pp, self.gold_change.gp, self.gold_change.sp, self.gold_change.cp
