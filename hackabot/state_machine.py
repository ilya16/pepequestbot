import granula

from hackabot.common import START_STEP, State, Context, BotResponse
from hackabot.responder import ConstantResponder, IResponder, AbilitiesRespondersPipeline
from hackabot.state_switcher import StateSwitchersPipeline
from hackabot.pipeline_factory import PipelineFactory, START_ABILITY, Abilities


class StateMachineError(Exception):
    ...


class StateMachine:
    _ABILITIES = set(Abilities)

    def __init__(
            self,
            responders_pipeline: AbilitiesRespondersPipeline,
            switchers_pipeline: StateSwitchersPipeline,
            default_responder: IResponder
    ):
        self._responders_pipeline = responders_pipeline
        self._switchers_pipeline = switchers_pipeline
        self._default_responder = default_responder

        self._state = State(START_ABILITY, START_STEP)

    def get_response(self, context: Context) -> BotResponse:
        switcher = self._switchers_pipeline[self._state.ability]
        new_state = switcher.switch(context, self._state)

        if new_state.ability not in self._ABILITIES:
            raise StateMachineError('Ability does not exist')

        if new_state.step is None:
            return self._default_responder.respond(context)

        responders = self._responders_pipeline[new_state.ability]
        if new_state.step >= len(responders):
            raise StateMachineError('Step is out of bound')

        self._state = new_state
        return responders[new_state.step].respond(context)


def get_state_machine(config: granula.Config):
    factory = PipelineFactory(config)
    
    return StateMachine(
        responders_pipeline=factory.responders_pipeline,
        switchers_pipeline=factory.switchers_pipeline,
        default_responder=ConstantResponder('Что вы хотите сделать?'),
    )
