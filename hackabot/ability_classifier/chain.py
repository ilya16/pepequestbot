from typing import Optional, Sequence

from .base import IAbilityClassifier
from hackabot.common import Context, Ability, State


class ChainAbilityClassifier(IAbilityClassifier):
    def __init__(self, classifiers: Sequence[IAbilityClassifier]):
        self._classifiers = classifiers

    def classify(self, context: Context, state: State) -> Optional[Ability]:
        for classifier in self._classifiers:
            ability = classifier.classify(context, state)
            if ability is not None:
                return ability

        return None
