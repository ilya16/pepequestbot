import hypothesis
import hypothesis.strategies as st
import pytest

from hackabot.common import Context, BotResponse
from hackabot.responder import EchoResponder


@pytest.fixture(scope='module')
def echo_responder() -> EchoResponder:
    return EchoResponder()


@hypothesis.given(text=st.text(), user_id=st.text())
def test_echo(text, user_id, echo_responder: EchoResponder):
    context = Context(text, user_id)
    expected = BotResponse(text=f'Ваш идентификатор: {user_id}\nВаше сообщение: {text}')

    assert echo_responder.respond(context) == expected
