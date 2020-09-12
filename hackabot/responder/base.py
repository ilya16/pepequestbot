import abc
from typing import Optional, List, Mapping

from hackabot.common import Context, BotResponse, Ability


class IResponder(abc.ABC):
    @abc.abstractmethod
    def respond(self, context: Context) -> Optional[BotResponse]:
        ...


RespondersPipeline = List[IResponder]
AbilitiesRespondersPipeline = Mapping[Ability, RespondersPipeline]
