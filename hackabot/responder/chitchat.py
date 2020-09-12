from typing import Optional

import requests
from requests import RequestException

from hackabot.common import Context, BotResponse
from .base import IResponder


class ChitchatResponder(IResponder):
    def __init__(self, url: str):
        self._url = url

    def respond(self, context: Context) -> Optional[BotResponse]:
        try:
            response = requests.post(self._url, json={'text': context.text, 'user_id': context.user_id})
            text = response.json().get('text')
            bot_response = BotResponse(text=text) if text is not None else None
        except RequestException:
            bot_response = None

        return bot_response
