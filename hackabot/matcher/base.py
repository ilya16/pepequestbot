import abc
from typing import Any

from hackabot.common import Context


class IMatcher(abc.ABC):
    @abc.abstractmethod
    def match(self, context: Context) -> Any:
        ...
