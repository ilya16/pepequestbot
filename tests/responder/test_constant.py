import hypothesis
import hypothesis.strategies as st
import pytest

from hackabot.common import BotResponse, Context
from hackabot.responder import ConstantResponder


@pytest.fixture(scope='module')
def constant_responder() -> ConstantResponder:
    return ConstantResponder(response_text='response')


@hypothesis.given(text=st.text(), user_id=st.text())
def test_constant(text, user_id, constant_responder: ConstantResponder):
    context = Context(text, user_id)
    expected = BotResponse(text='response')

    assert constant_responder.respond(context) == expected
