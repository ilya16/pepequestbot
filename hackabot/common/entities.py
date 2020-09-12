import dataclasses
from typing import Optional

Ability = str
Step = int
START_STEP: Step = 0
Balance = float


@dataclasses.dataclass(frozen=True)
class Context:
    text: str
    user_id: str


@dataclasses.dataclass()
class BotResponse:
    text: str


@dataclasses.dataclass(frozen=True)
class State:
    ability: Ability
    step: Optional[Step]


@dataclasses.dataclass(frozen=True)
class UserInfo:
    user_id: str
    state: State
    balance: Balance

