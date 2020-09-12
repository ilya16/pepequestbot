from .base import IStateSwitcher, State

from hackabot.common import Context
from hackabot.ability_classifier import IAbilityClassifier
from hackabot.common import START_STEP
from hackabot.matcher import IMatcher, IdenticalMatcher
from ..responder import RespondersPipeline, AbilitiesRespondersPipeline


class LoopedAbilitySwitcher(IStateSwitcher):
    def __init__(self, ability_classifier: IAbilityClassifier, responders_pipeline: AbilitiesRespondersPipeline,
                 matcher: IMatcher = IdenticalMatcher()):
        self._ability_classifier = ability_classifier
        self._responders_pipeline = responders_pipeline
        self._matcher = matcher

    def switch(self, context: Context, state: State) -> State:
        classified_ability = self._ability_classifier.classify(context, state)
        if classified_ability is not None and classified_ability != state.ability:
            return State(classified_ability, step=START_STEP)

        ability_responders = self._responders_pipeline[state.ability]
        if state.step == len(ability_responders) - 1:
            return State(state.ability, step=START_STEP)

        if state.step < len(ability_responders) - 1 and self._matcher.match(context) is not None:
            return State(state.ability, step=state.step + 1)

        return state
