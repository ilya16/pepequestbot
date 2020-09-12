import abc
from typing import Optional

from hackabot.common import Context, Ability, State


class IAbilityClassifier(abc.ABC):
    @abc.abstractmethod
    def classify(self, context: Context, state: State) -> Optional[Ability]:
        ...
