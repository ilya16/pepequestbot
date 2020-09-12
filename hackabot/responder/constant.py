from typing import Optional

from hackabot.common import Context, BotResponse
from .base import IResponder


class ConstantResponder(IResponder):
    def __init__(self, response_text: Optional[str]):
        self._response_text = response_text

    def respond(self, context: Context) -> Optional[BotResponse]:
        if self._response_text is None:
            return None

        return BotResponse(text=self._response_text)
