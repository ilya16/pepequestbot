import abc
from typing import Mapping

from hackabot.common import Ability, Context, State


class IStateSwitcher(abc.ABC):
    @abc.abstractmethod
    def switch(self, context: Context, state: State) -> State:
        ...


StateSwitchersPipeline = Mapping[Ability, IStateSwitcher]
