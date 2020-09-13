import dataclasses
from typing import Optional
import enum


class States(enum.Enum):
    start = 0
    first_year = 1
    second_year = 2
    third_year = 3
    forth_year = 4
    quiz = 5


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


@dataclasses.dataclass()
class UserInfo:
    user_id: str
    username: str = ''
    first_name: str = ''
    last_name: str = ''
    state: int = -1
    age: int = -1
    balance: Balance = 0
    frequency: int = -1
    chat_id: int = -1
    quiz_id: int = -1

