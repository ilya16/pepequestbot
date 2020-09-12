from typing import Optional

from hackabot.common import Context, BotResponse
from .base import IResponder


class EchoResponder(IResponder):
    def respond(self, context: Context) -> Optional[BotResponse]:
        return BotResponse(text=f'Ваш идентификатор: {context.user_id}\nВаше сообщение: {context.text}')
