from typing import Any

from hackabot.common import Context
from hackabot.matcher.base import IMatcher


class IdenticalMatcher(IMatcher):
    def match(self, context: Context) -> Any:
        return context
