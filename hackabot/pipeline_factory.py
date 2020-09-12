from enum import Enum

import granula

from hackabot.common import Ability
from hackabot.responder import ConstantResponder, AbilitiesRespondersPipeline, EchoResponder, ChitchatResponder
from hackabot.state_switcher import LoopedAbilitySwitcher, NextAbilitySwitcher
from hackabot.ability_classifier import IAbilityClassifier, ChainAbilityClassifier, RegexAbilityClassifier
from lazy import lazy

from hackabot.state_switcher import StateSwitchersPipeline


class Abilities(Ability, Enum):
    EMPTY = 'empty'
    HELLO = 'hello'
    CHITCHAT = 'chitchat'
    TEST = 'test'
    ECHO = 'echo'


START_ABILITY = Abilities.EMPTY


class PipelineFactory:
    def __init__(self, config: granula.Config):
        self._config = config

    @lazy
    def responders_pipeline(self) -> AbilitiesRespondersPipeline:
        chitchat_url = f'https://{self._config.chitchat.domain}/?key={self._config.chitchat.secret_key}'

        return {
            Abilities.EMPTY: [ConstantResponder(None)],
            Abilities.HELLO: [ConstantResponder('Здравствуйте!')],
            Abilities.TEST: [
                ConstantResponder('Как вас зовут?'),
                ConstantResponder('Сколько вам лет?'),
                ConstantResponder('Вы любите программировать?'),
            ],
            Abilities.CHITCHAT: [ChitchatResponder(chitchat_url)],
            Abilities.ECHO: [EchoResponder()]
        }

    @lazy
    def ability_classifier(self) -> IAbilityClassifier:
        return ChainAbilityClassifier([
            RegexAbilityClassifier(r'переключи на эхо', ability=Abilities.ECHO, ignore_case=True),
            RegexAbilityClassifier(r'переключи на болталку', ability=Abilities.CHITCHAT, ignore_case=True),
        ])

    @lazy
    def switchers_pipeline(self) -> StateSwitchersPipeline:
        looped_ability_switcher = LoopedAbilitySwitcher(self.ability_classifier, self.responders_pipeline)
        next_ability_switcher = NextAbilitySwitcher(self.ability_classifier, self.responders_pipeline)

        return {
            Abilities.EMPTY: next_ability_switcher,
            Abilities.HELLO: next_ability_switcher,
            Abilities.TEST: next_ability_switcher,
            Abilities.CHITCHAT: looped_ability_switcher,
            Abilities.ECHO: looped_ability_switcher,
        }
