from dataclasses import dataclass, field
from typing import List

@dataclass
class UserDto:
    userId: int
    currentParty: str = ""
    parties: List[str] = field(default_factory=list)