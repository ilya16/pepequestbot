import json

import hypothesis
import hypothesis.strategies as st
import pytest

from hackabot.common import Context, BotResponse
from hackabot.responder import ChitchatResponder


URL = 'http://some.url/test'


@hypothesis.given(text=st.text(), user_id=st.text())
def test_non_empty_response(text, user_id, requests_mock):
    context = Context(text, user_id)
    responder = ChitchatResponder(URL)

    response_text = f'response: {text}'
    requests_mock.post(URL, json={'text': response_text})

    assert responder.respond(context) == BotResponse(text=response_text)


@hypothesis.given(text=st.text(), user_id=st.text())
@pytest.mark.parametrize(
    'response_json', [{'text': None}, {}]
)
def test_empty_response(text, user_id, response_json, requests_mock):
    context = Context(text, user_id)
    responder = ChitchatResponder(URL)

    requests_mock.post(URL, json=response_json)

    assert responder.respond(context) is None


@hypothesis.given(text=st.text(), user_id=st.text())
def test_json_decoder_error(text, user_id, requests_mock):
    context = Context(text, user_id)
    responder = ChitchatResponder(URL)

    requests_mock.post(URL, json=None)

    with pytest.raises(json.decoder.JSONDecodeError):
        responder.respond(context)
