from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class UserDto:
	userId: int
	currentParty: str = ""
	parties: List[str] = field(default_factory=list)

@dataclass
class PartyGoldDto:
    pp: int = 0
    gp: int = 0
    sp: int = 0
    cp: int = 0

@dataclass
class ItemDto:
    name: str = "None"
    value: PartyGoldDto = PartyGoldDto()
    rarity: str = "None"
    notes: str = "None"
    weight: int = 0
    quantity: int = 1

    def convert_value_to_party_gold_dto(self) -> PartyGoldDto:
        return PartyGoldDto(**self.value)


