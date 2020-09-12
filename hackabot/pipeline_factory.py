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


MESSAGES = [
    """Студенты Сколтеча отправили андроида Олега в прошлое, чтобы он закупил акции успешных компаний и разбогател. Однако в процессе путешествия во времени он потерял память и не помнит, куда вкладываться. Всё же он нашел способ связаться с будущим  - это Вы. Он наладил контакт с вашим устройством и теперь может отправлять вам короткие сообщения. При себе он имеет начальный капитал в пять тысяч долларов. Помоги Олегу заработать миллион долларов, а он в долгу не останется. Сколько раз в неделю вы бы хотели с ним связываться?""",
    """К сожалению, связь с прошлым — энергозатратный процесс, поэтому, чтобы получить возможность контактировать с Олегом более одного раза в день, нужно проходить квиз на финансовую грамотность и зарабатывать на электричество для поддержания контакта. Для прохождения квиза надо написать команду /quiz. Заходя в игру два дня подряд, вы получаете дополнительный заряд энергии для перемещения в прошлое и отмены последнего принятого решения. Чтобы проверить его текущий баланс в прошлом, напиши /balance_past. Чтобы проверить его текущий баланс в настоящем, напиши /balance_present.  Если ты готов начать игру, нажми /go. """,
    """Добрый день! Олег на связи, сейчас 1994 год и я стою перед непростым выбором. Я познакомился с мужчиной, который рассказал мне, как он заработал деньги очень быстро, купив ценные бумаги одной компании. По телевизору везде крутится реклама, однако купить можно только билеты, а не акции компании. Все больше и больше людей покупают эти билеты, а доходность каждой невообразимо высокая. Что посоветуешь сделать?

- купить билеты, мужчина сказал, что за две недели накопил жене на сапоги! 
- не покупать билеты
""",
    """Какую сумму вложить в акции этой компании?""",
    """Описанная выше компания - МММ — крупнейшая в истории России финансовая пирамида. По оценкам экспертов, от МММ пострадало около 10 миллионов человек, общий ущерб населению составляет 110 млн долларов. Вложенные Олегом деньги потеряны навсегда :(""",
]


class PipelineFactory:
    def __init__(self, config: granula.Config):
        self._config = config

    @lazy
    def responders_pipeline(self) -> AbilitiesRespondersPipeline:
        chitchat_url = f'https://{self._config.chitchat.domain}/?key={self._config.chitchat.secret_key}'

        return {
            Abilities.EMPTY: [ConstantResponder(None)],
            Abilities.HELLO: [ConstantResponder(MESSAGES[0])],
            Abilities.TEST: [
                ConstantResponder(m) for m in MESSAGES[1:]
            ],
            # Abilities.HELLO: [ConstantResponder('Здравствуйте!')],
            # Abilities.TEST: [
            #     ConstantResponder('Как вас зовут?'),
            #     ConstantResponder('Сколько вам лет?'),
            #     ConstantResponder('Вы любите программировать?'),
            # ],
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
