import re
from typing import Callable, Any, List, Match

from hackabot.common import Context
from hackabot.matcher.base import IMatcher


class RegexMatcher(IMatcher):
    def __init__(self, regex: str, ignore_case: bool = False, grouper: Callable[[List[Match]], Any] = None):
        flags = re.I if ignore_case else 0
        self._regex = re.compile(regex, flags=flags)
        self._grouper = grouper

    def match(self, context: Context) -> Any:
        return self._grouper(self._regex.findall(context.text))
