import re
from typing import Optional

from .base import IAbilityClassifier
from hackabot.common import Context, Ability, State


class RegexAbilityClassifier(IAbilityClassifier):
    def __init__(self, regex: str, ability: Ability, ignore_case: bool = False):
        flags = re.I if ignore_case else 0
        self._regex = re.compile(regex, flags=flags)
        self._ability = ability

    def classify(self, context: Context, state: State) -> Optional[Ability]:
        return self._ability if self._regex.search(context.text) else None
