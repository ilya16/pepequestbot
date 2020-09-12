import collections
import logging
import os
import threading
from threading import Lock
from typing import Any, DefaultDict

import requests
import telebot
import granula

from tts import TTS
from hackabot.common import CONFIG_PATH, Context
from hackabot.state_machine import get_state_machine, StateMachine

logger = logging.getLogger('telegram')


def get_full_name(user: telebot.types.User) -> str:
    name = user.first_name or ''
    if user.last_name:
        name += f' {user.last_name}'
    if user.username:
        name += f' @{user.username}'
    return name


def run_bot(config: granula.Config):
    locks: DefaultDict[Any, Lock] = collections.defaultdict(threading.Lock)
    bot = telebot.TeleBot(token=config.telegram.key)
    state_machine: StateMachine = get_state_machine(config)
    tts = TTS(config=config['voice_kit'])

    def _send(message: telebot.types.Message, response: str):
        return bot.send_message(chat_id=message.chat.id, text=response, parse_mode='html')

    def _send_voice(message: telebot.types.Message, voice):
        return bot.send_voice(chat_id=message.chat.id, voice=voice)

    @bot.message_handler(commands=['start'])
    def _start(message: telebot.types.Message):
        with locks[message.chat.id]:
            _send(message, response='Привествую тебя. Нажми /start_quest :)')

    # @bot.message_handler(commands=['start_quest'])
    # def _start_quest(message: telebot.types.Message):
    #     with locks[message.chat.id]:
    #         _send(message, response='Задавайте ваши вопросы')

    def _send_response(message: telebot.types.Message):
        chat_id = message.chat.id
        user_id = str(message.from_user.id) if message.from_user else '<unknown>'

        with locks[chat_id]:
            try:
                context = Context(message.text, user_id)
                response = state_machine.get_response(context)
                response_text = response.text if response is not None else 'Ответа нет'
            except KeyboardInterrupt:
                return
            except Exception as e:
                logger.exception(e)
                response_text = 'Произошла ошибка'

            _send(message, response=response_text)

            path = tts.audio2text(response_text)
            message = _send_voice(message, voice=open(path, 'rb'))
            print(message.voice.file_id)
            os.remove(path)

    @bot.message_handler()
    def send_response(message: telebot.types.Message):  # pylint:disable=unused-variable
        try:
            _send_response(message)
        except KeyboardInterrupt:
            return
        except Exception as e:
            logger.exception(e)

    logger.info('Telegram bot started')
    bot.polling(none_stop=True)


def main():
    run_bot(config=granula.Config.from_path(CONFIG_PATH.absolute()))


if __name__ == '__main__':
    while True:
        try:
            main()
        except requests.RequestException as e:
            logger.exception(e)
