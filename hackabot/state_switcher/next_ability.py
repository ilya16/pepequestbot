from .base import IStateSwitcher, State

from hackabot.common import Context
from hackabot.ability_classifier import IAbilityClassifier
from hackabot.common import START_STEP
from hackabot.matcher import IMatcher, IdenticalMatcher
from hackabot.responder import AbilitiesRespondersPipeline


class NextAbilitySwitcher(IStateSwitcher):
    def __init__(self, ability_classifier: IAbilityClassifier, responders_pipeline: AbilitiesRespondersPipeline,
                 matcher: IMatcher = IdenticalMatcher()):
        self._ability_classifier = ability_classifier
        self._responders_pipeline = responders_pipeline

        abilities = list(responders_pipeline)
        self._next_ability = {abilities[i]: abilities[i + 1] for i in range(len(abilities) - 1)}
        self._next_ability[abilities[-1]] = abilities[0]

        self._matcher = matcher

    def switch(self, context: Context, state: State) -> State:
        classified_ability = self._ability_classifier.classify(context, state)
        if classified_ability is not None and classified_ability != state.ability:
            return State(classified_ability, step=START_STEP)

        ability_responders = self._responders_pipeline[state.ability]
        if state.step == len(ability_responders) - 1:
            next_ability = self._next_ability[state.ability]
            return State(next_ability, step=START_STEP)

        if state.step < len(ability_responders) - 1 and self._matcher.match(context) is not None:
            return State(state.ability, step=state.step + 1)

        return state
