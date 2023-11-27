from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class UserDto:
    userId: int
    currentParty: str = ""
    parties: List[str] = field(default_factory=list)

@dataclass
class ItemDto:
    name: str = "None"
    value: Dict[str, int] = field(default_factory=lambda: {"pp": 0, "gp": 0,"sp": 0, "cp": 0})
    rarity: str = "None"

@dataclass
class PartyGoldDto:
    pp: int = 0,
    gp: int = 0,
    sp: int = 0,
    cp: int = 0
