import collections
import logging
import os
import sys
import threading
import time
from threading import Lock
from typing import Any, DefaultDict

import granula
import telebot
from telebot import types

from hackabot.common.entities import States, UserInfo
from hackabot.storage import GameStorage

sys.path.append(os.path.abspath("."))
from hackabot.tts import TTS
from hackabot.common import CONFIG_PATH
from hackabot.state_machine import get_state_machine, StateMachine

logger = logging.getLogger('telegram')
import sys

sys.path.append(os.path.abspath('../hackabot'))

config = granula.Config.from_path(CONFIG_PATH.absolute())

bot = telebot.TeleBot(token=config.telegram.key)
tts = TTS(config=config.voice_kit)
state_machine: StateMachine = get_state_machine(config)
locks: DefaultDict[Any, Lock] = collections.defaultdict(threading.Lock)

game_storage = GameStorage(config=config.storage)

Quiz = [
    ("Какую долю ваших расходов за месяц занимает косметика?",
     ["10% (5000 ₽)",
      "5% (2500 ₽)",
      "21% (10500 ₽)",
      "13% (6500 ₽)"],
     0),
    ("Назовите максимальную сумму, которую Вы тратили за раз в одном из магазинов:",
     ["15200 ₽",
      "3840 ₽",
      "7340 ₽",
      "2710 ₽"],
     0),
    ("На какую категорию товаров Вы потратили больше всего в прошлом месяце:",
     ["кино",
      "фаст фуд",
      "супермаркеты",
      "искусство"],
     2),
    ("Если ваша цель — просто сохранить свои деньги, оптимальной стратегией будет:",
     ["Хранить деньги под матрасом",
      "Инвестировать в акции/облигации",
      "Положить деньги в банк под стандартный процент",
      "Часть держать на вкладах, часть — в инвестициях."],
     2),
    ("Что из перечисленного нельзя купить на бирже?",
     ["акции",
      "зерно",
      "автомобиль",
      "нефть"],
     2),
    ("Правила минимизации валютных рисков заключается в том, чтобы брать кредиты:",
     ["в рублях",
      "в долларах",
      "в рублях и долларах",
      "в той валюте в которой совершается большая часть расходов и получаются доходы"],
     3),
    ("Предположим, вы положили 10 000 рублей на вклад под 5% годовых. "
     "Какая сумма будет на этом вкладе через 10 лет?",
     ["10 000 * (1+10*0,05)",
      "10 000 * (1+0,05)^10",
      "10 000 * 1,05 * 10",
      "10 000 * 10 / 1,05"],
     1),
    ("Допустим, вы положили 100 000 рублей под 5% годовых на один год. "
     "Инфляция за это время составила 3%. Сколько вы заработали на самом деле?",
     ["Всё просто, 100 000 * 1,05!",
      "100 000 * 1,03",
      "100 000 * (1,05-1,03)",
      "100 000 * 1,05 * 0,97"],
     2),
    ("Вы положили 50 000 рублей под 4% годовых на три года. "
     "В первый год инфляция составила 2,2%, во второй — 6%, в третий — 3,9%. "
     "Выгодным ли отказался вклад?",
     ["Да",
      "Нет"],
     1),
]


# print(Quiz[0])
# question, options, correct_option_id = Quiz[0]
# bot.send_poll(chat_id, question=question, options=options,
#               is_anonymous=False, type='quiz',
#               correct_option_id=correct_option_id, open_period=30)


def get_user(user_json):
    user = game_storage.get_user_info(user_json.id)
    if user is None:
        user = UserInfo(user_id=user_json.id)

    user.username = user_json.username
    user.first_name = user_json.first_name

    return user


def save_user(user):
    game_storage.save_user_info(user)


def _send(message: telebot.types.Message, response: str):
    return bot.send_message(chat_id=message.chat.id, text=response)


def _send_voice(message: telebot.types.Message, voice):
    return bot.send_voice(chat_id=message.chat.id, voice=voice)


@bot.message_handler(commands=['go'])
def first_year(message):
    user = get_user(message.from_user)
    user.state = States.first_year.value
    save_user(user)

    bot.send_message(message.chat.id, text='*День 1. Назад в 90е.*', parse_mode='Markdown')
    _send_voice(message, voice=tts.text2audio('Добрый день! На дворе 1994 год'))
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton('Купить билеты', callback_data='yes_first'),
        telebot.types.InlineKeyboardButton('Не покупать билеты', callback_data='no_first'))
    _send_voice(message, voice=tts.text2audio('Олег на связи и я стою перед непростым выбором.'))
    _send_voice(message, voice=tts.text2audio(
        'Я познакомился с мужчиной, который рассказал мне, как он заработал деньги очень быстро, купив ценные бумаги '
        'одной компании.'))
    _send_voice(message, voice=tts.text2audio(
        'По телевизору везде крутится реклама, однако купить можно только билеты, а не акции компании.'))
    _send_voice(message, voice=tts.text2audio(
        'Все больше и больше людей покупают эти билеты, а доходность каждой невообразимо высокая.'))
    time.sleep(10)
    bot.send_message(message.chat.id, 'Что посоветуешь сделать?', reply_markup=keyboard)


def _send_balance(message, balance=0.):
    _send(message, response=f'Баланс Олега: ${balance:.2f}')


@bot.message_handler(commands=['balance'])
def balance(message):
    user = get_user(message.from_user)
    _send_balance(message, balance=user.balance)


@bot.message_handler(commands=['next'])
def next_year(message):
    user = get_user(message.from_user)
    if user.state == States.first_year.value:
        user.state = States.second_year.value
        save_user(user)

        bot.send_message(message.chat.id, text='*День 2. Привет, 2000!*', parse_mode='Markdown')
        _send_voice(message, voice=tts.text2audio('Приветствую! Это Олег из прошлого, 2000 год.'))
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton('Первая компания', callback_data='yes_second'),
            telebot.types.InlineKeyboardButton('Вторая компания', callback_data='no_second'))
        _send_voice(message, voice=tts.text2audio(
            'Все большую популярность набирает интернет, а поисковики становятся главным способом информации в интернете.'))
        _send_voice(message, voice=tts.text2audio(
            'Пока не поздно, я решил вложить свои деньги в одну из следующих компаний в этом направлении. '))
        _send_voice(message, voice=tts.text2audio(
            'Первая - известная американская компания, несколько лет на рынке, однако в данный момент испытывает '
            'финансовые трудности в связи с тем что конкуренты ушли вперед и вкладываются в развитие технологий. '))
        _send_voice(message, voice=tts.text2audio(
            'Другая - новая российская компания, занимающаяся русскоязычным аналогом, не имеющая конкурентов на '
            'данный момент.'))
        time.sleep(10)
        bot.send_message(message.chat.id, 'Что подсказывает тебе твое инвесторское чутьё?', reply_markup=keyboard)
    elif user.state == States.second_year.value:
        user.state = States.third_year.value
        save_user(user)

        bot.send_message(message.chat.id, text='*День 3. Верните мне мой 2007.*', parse_mode='Markdown')
        _send_voice(message, voice=tts.text2audio('Добрый день! Это Олег из 2007'))
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton('Конечно, нельзя упускать такую возможность.',
                                               callback_data='yes_third'),
            telebot.types.InlineKeyboardButton('Я против.', callback_data='no_third'))

        _send_voice(message, voice=tts.text2audio(
            'В мире все большую популярность набирают ПК и интернет, но многие люди не могут себе этого позволить.'))
        _send_voice(message, voice=tts.text2audio(
            'Я решил потратить часть накопленных денег на аренду помещения (500 долларов/месяц)'))
        _send_voice(message, voice=tts.text2audio(
            'И конечно на закупку компьютеров (400 долларов/шт), чтобы дать возможность людям собираться вместе и играть.'))
        _send_voice(message,
                    voice=tts.text2audio(
                        'Я думаю это будет приносить неплохой пассивный доход и очень быстро окупится.'))

        time.sleep(10)
        bot.send_message(message.chat.id, 'Что скажешь по этому поводу?', reply_markup=keyboard)
    elif user.state == States.third_year.value:
        user.state = States.forth_year.value
        save_user(user)

        bot.send_message(message.chat.id, text='*День 4. 2010.*', parse_mode='Markdown')
        _send_voice(message, voice=tts.text2audio('Привет, это снова Олег! 2010 год.'))
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton('в валюте', callback_data='yes_fourth'),
            telebot.types.InlineKeyboardButton('в рублях', callback_data='no_fourth'))
        _send_voice(message, voice=tts.text2audio('Я решил открыть кафе в Москве, но у меня нет начального капитала.'))
        _send_voice(message, voice=tts.text2audio(
            'Я решил взять ссуду в банке на достаточно короткий срок. Мне предложили 2 варианта:'))
        _send_voice(message, voice=tts.text2audio(
            'валютный кредит очень маленьким процентом (4%), и кредит в рублях с большим процентом 10%).'))
        time.sleep(5)
        bot.send_message(message.chat.id, 'В какой валюте мне стоит взять кредит?', reply_markup=keyboard)


def final(message):
    user = get_user(message.chat)
    bot.send_message(message.chat.id, text='*Конец.*', parse_mode='Markdown')
    _send_voice(message, voice=tts.text2audio(
        'Поздравляем! Вы успешно завершили текущий квест и помогли Олегу увеличить его капитал.'))
    _send_balance(message, balance=user.balance)
    _send_voice(message, voice=tts.text2audio(
        'Олег ждёт вас на следующем квесте через неделю :)'))


def get_investment_first_year(message):  # получаем фамилию
    user = get_user(message.from_user)
    try:
        investment = min(user.balance, int(message.text))
    except Exception:
        investment = 2000
    user.balance -= investment
    save_user(user)

    _send_voice(message, voice=tts.text2audio(
        'Описанная выше компания - МММ — крупнейшая в истории России финансовая пирамида. По оценкам экспертов, '
        'от МММ пострадало около 10 миллионов человек, общий ущерб населению составляет 110 млн долларов. Вложенные '
        'Олегом деньги потеряны навсегда :('))
    time.sleep(6)
    _send_voice(message, voice=tts.text2audio('К сожалению, баланс Олега уменьшился.'))
    time.sleep(8)
    _send_voice(message, voice=tts.text2audio('Олег надеется, что в следующий раз Вы поможете ему лучше.'))
    _send_balance(message, balance=user.balance)

    _send(message, response='Для продолжения игры отправьте /next')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user = get_user(call.message.chat)

    if call.data == "yes_help":
        _send_voice(call.message, voice=tts.text2audio('Вам это зачтется :)'))
        _send_voice(call.message, voice=tts.text2audio('Сколько раз в неделю вы бы хотели с ним связываться?'))
        bot.register_next_step_handler(call.message, get_time)
    elif call.data == "no_help":
        _send_voice(call.message, voice=tts.text2audio('Ваш баланс счета опустел :)'))
        _send_voice(call.message, voice=tts.text2audio('Попробуйте с самого начала'))
        user.balance = 0
        time.sleep(10)
    elif call.data == "yes_first":
        bot.send_message(call.message.chat.id, 'Какую сумму вложить в акции этой компании?')
        bot.register_next_step_handler(call.message, get_investment_first_year)
    elif call.data == "no_first":
        _send_voice(call.message, voice=tts.text2audio(
            'Описанная выше компания - МММ — крупнейшая в истории России финансовая пирамида. По оценкам экспертов, '
            'от МММ пострадало около 10 миллионов человек, общий ущерб населению составляет 110 млн долларов.'))
        time.sleep(6)
        _send_voice(call.message, voice=tts.text2audio(
            'Благодаря Вам Олег не вложился в МММ и сохранил свои деньги, вместо этого он вложился в акции Газпрома ('
            '2000 долларов) и за 5 лет заработал еще 5000 долларов.'))
        user.balance += 5000
        _send_balance(call.message, balance=user.balance)
        _send(call.message, response='Для продолжения игры отправьте /next')
    elif call.data == "yes_second":
        _send_voice(call.message, voice=tts.text2audio('Первая компания - Yahoo. Вторая - Яндекс.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Поисковая система «Яндекс» является четвёртой среди поисковых систем мира по количеству обрабатываемых '
            'поисковых запросов.'))
        _send_voice(call.message,
                    voice=tts.text2audio('Yahoo все еще не восстановилась после кризиса 2000-2001 годов.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Вложившись в Yahoo, Олег к 2003 году потеряет половину от вложенной суммы, и, разочаровавшись в компании '
            'продаст их акции.'))
        user.balance /= 2
        _send_balance(call.message, balance=user.balance)
        _send(call.message, response='Для продолжения игры отправьте /next')
    elif call.data == "no_second":
        _send_voice(call.message, voice=tts.text2audio('Первая компания - Yahoo. Вторая - Яндекс.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Поисковая система «Яндекс» является четвёртой среди поисковых систем мира по количеству обрабатываемых '
            'поисковых запросов.'))
        _send_voice(call.message,
                    voice=tts.text2audio('Yahoo все еще не восстановилась после кризиса 2000-2001 годов.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Вложившись в Yandex, Олег не прогадал. На настоящий момент он значительно приумножил свое состояние '
            'благодаря вашей помощи и пока хранит эти акции у себя на балансе в банке Тинькофф ; )'))
        user.balance *= 5
        _send_balance(call.message, balance=user.balance)
        _send(call.message, response='Для продолжения игры отправьте /next')
    elif call.data == "yes_third":
        _send_voice(call.message, voice=tts.text2audio('Олегу повезло, компьютерные клубы стали очень популярны'))
        _send_voice(call.message, voice=tts.text2audio('Его затраты окупились через 4 месяца.'))
        _send_voice(call.message, voice=tts.text2audio(' За те несколько лет, в которые данный бизнес был успешен.'))
        _send_voice(call.message, voice=tts.text2audio('Олег смог заработать 40000 долларов.'))
        user.balance += 40000
        _send_balance(call.message, balance=user.balance)
        _send(call.message, response='Для продолжения игры отправьте /next')
    elif call.data == "no_third":
        _send_voice(call.message, voice=tts.text2audio('Олег упустил неплохую возможность заработать.'))
        _send_balance(call.message, balance=user.balance)
        _send(call.message, response='Для продолжения игры отправьте /next')
    elif call.data == "yes_fourth":
        _send_voice(call.message, voice=tts.text2audio('Недостаточная устойчивость российской экономики'))
        _send_voice(call.message, voice=tts.text2audio('как правило, порождает в отношении рубля'))
        _send_voice(call.message,
                    voice=tts.text2audio('не такие оптимистичные, как в отношении доллара, инфляционные ожидания.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Так как прибыль Олега от кафе будет исчисляться в рублях, то кредит ему тоже следует брать в рублях'))
        _send_voice(call.message,
                    voice=tts.text2audio('с целью минимизации рисков в случае внезапно большой инфляции.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Олегу, не повезло: в 2014 году курс доллара вырос с 35 рублей за доллар до 65.'))
        _send_voice(call.message, voice=tts.text2audio(
            'К счастью, наш герой оказался грамотным руководителем, его кафе пользовалось спросом и окупилось за 7 лет.'))
        _send_voice(call.message, voice=tts.text2audio('Хотя если бы он взял кредит в рублях - окупилось бы за 5 лет.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Таким образом, спустя три года чистая прибыль с него составила 30000 долларов.'))
        user.balance += 30000
        final(call.message)
    elif call.data == "no_fourth":
        _send_voice(call.message, voice=tts.text2audio(
            'Недостаточная устойчивость российской экономики, как правило, порождает в отношении рубля'))
        _send_voice(call.message,
                    voice=tts.text2audio('не такие оптимистичные, как в отношении доллара, инфляционные ожидания.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Так как прибыль Олега от кафе будет исчисляться в рублях, то кредит ему тоже следует брать в рублях'))
        _send_voice(call.message,
                    voice=tts.text2audio('с целью минимизации рисков в случае внезапно большой инфляции.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Благодаря Вам кафе Олега окупилось на два года раньше (в сравнении с версией Олега взявшего валютный кредит)'))
        _send_voice(call.message,
                    voice=tts.text2audio('ведь в 2014 году курс доллара вырос с 35 рублей за доллар до 65.'))
        _send_voice(call.message, voice=tts.text2audio(
            'Олег выплатил кредит в 2015 году и спустя пять лет чистая прибыль с него составила 50000 долларов'))
        user.balance += 50000
        final(call.message)
    else:
        _send(call.message, response='Произошла ошибка :( Попробуйте с самого начала /start.')

    save_user(user)


def get_help(message):
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes_help')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no_help')
    keyboard.add(key_no)
    question = 'Поможете ему разбогатеть?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


HELP_MESSAGE = 'Для прохождения квиза надо написать команду /quiz. Заходя в игру два дня подряд, вы получаете ' \
               'дополнительный заряд энергии для перемещения в прошлое и отмены последнего принятого решения. Чтобы ' \
               'проверить его текущий баланс, напиши /balance.  Если ты готов начать квест, нажми /go. '


def get_time(message):
    user = get_user(message.from_user)
    user.frequency = message.text
    save_user(user)

    _send_voice(message, voice=tts.text2audio(
        'К сожалению, связь с прошлым — энергозатратный процесс.'))
    _send_voice(message, voice=tts.text2audio(
        'Поэтому, чтобы получить возможность контактировать с Олегом более одного раза в день, нужно проходить квиз '
        'на финансовую грамотность и зарабатывать на электричество для поддержания контакта.'))
    _send(message, response=HELP_MESSAGE)


@bot.message_handler(commands=['start'])
def start_bot(message):
    user = get_user(message.from_user)
    user.state = States.start.value
    save_user(user)

    response_text = f'Привет{", " + user.first_name if user.first_name else ""}!' \
                    f'\n\nДля начала квеста отправь /start_quest'
    _send(message, response=response_text)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start_quest":
        user = get_user(message.from_user)
        user.balance = 5000
        save_user(user)
        get_user(message.from_user)

        response_text = "Студенты Сколтеча отправили андроида Олега в прошлое, чтобы он закупил акции успешных " \
                        "компаний и разбогател. "
        _send_voice(message, voice=tts.text2audio(response_text))
        # print(message.voice.file_id)
        time.sleep(2)
        response_text = 'Однако в процессе путешествия во времени он потерял память и не помнит, куда вкладываться. ' \
                        'Всё же он нашел способ связаться с будущим  - это Вы. Он наладил контакт с вашим устройством ' \
                        'и теперь может отправлять вам короткие сообщения. '
        _send_voice(message, voice=tts.text2audio(response_text))
        time.sleep(2)
        response_text = 'При себе он имеет начальный капитал в 5000$. Помоги Олегу заработать миллион долларов, ' \
                        'а он в долгу не останется. '
        _send_voice(message, voice=tts.text2audio(response_text))
        _send_balance(message, balance=user.balance)
        get_help(message)
    elif message.text == "/help":
        _send(message, response=HELP_MESSAGE)
    else:
        response_text = "Я тебя не понимаю. Напиши /help."
        _send(message, response=tts.text2audio(response_text))


bot.polling(none_stop=True, interval=0)
