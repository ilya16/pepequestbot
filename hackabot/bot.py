import telebot;
from telebot import types
import time
import os


bot = telebot.TeleBot(API_TOKEN);

name = '';
surname = '';
age = 0;
our_time=0;
investment_rub=0

@bot.message_handler(commands=['go'])  
def first_year(message):  
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Купить билеты, мужчина сказал, что за две недели накопил жене на сапоги!', callback_data='yes'  
  ), 
        telebot.types.InlineKeyboardButton(  
            'Не покупать билеты', callback_data='no'
  )  
    )  
    bot.send_message(  
        message.chat.id,  
        'Добрый день! Олег на связи, сейчас 1994 год и я стою перед непростым выбором. Я познакомился с мужчиной, который рассказал мне, как он заработал деньги очень быстро, купив ценные бумаги одной компании. По телевизору везде крутится реклама, однако купить можно только билеты, а не акции компании. Все больше и больше людей покупают эти билеты, а доходность каждой невообразимо высокая. Что посоветуешь сделать?',  
        reply_markup=keyboard 
        
    )
@bot.callback_query_handler(func=lambda call: True )
def callback_worker(call):
    if call.data == "yes": 
        bot.send_message(call.message.chat.id,'Какую сумму вложить в акции этой компании?') 
        bot.register_next_step_handler(call.message, get_investment);
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Приветствую! Это Олег из прошлого, 2000 год. Все большую популярность набирает интернет, а поисковики становятся главным способом информации в интернете.');
        time.sleep(1)
        bot.send_message(call.message.chat.id, 'Пока не поздно я решил вложить свои деньги в одну из следующих компаний в этом направлении. Первая - известная Американская компания, несколько лет на рынке, однако в данный момент испытывает финансовые трудности в связи с тем что конкуренты ушли вперед и вкладываются в развитие технологий.');
        time.sleep(2)
        bot.send_message(call.message.chat.id, 'Другая - новая российская компания, занимающаяся русскоязычным аналом, не имеющая конкурентов на данный момент. Что подсказывает тебе твое инвесторское чутьё?')
        time.sleep(2)
        bot.register_next_step_handler(call.message, second_year);
    
    
def get_investment(message): #получаем фамилию
    global investment_rub;
    name = message.text;
    bot.send_message(message.from_user.id, 'Описанная выше компания - МММ — крупнейшая в истории России финансовая пирамида. По оценкам экспертов, от МММ пострадало около 10 миллионов человек, общий ущерб населению составляет 110 млн долларов. Вложенные Олегом деньги потеряны навсегда :(');
    bot.send_message(call.message.chat.id, 'Приветствую! Это Олег из прошлого, 2000 год. Все большую популярность набирает интернет, а поисковики становятся главным способом информации в интернете.');
    time.sleep(1)
    bot.send_message(call.message.chat.id, 'Пока не поздно я решил вложить свои деньги в одну из следующих компаний в этом направлении. Первая - известная Американская компания, несколько лет на рынке, однако в данный момент испытывает финансовые трудности в связи с тем что конкуренты ушли вперед и вкладываются в развитие технологий.');
    time.sleep(2)
    bot.send_message(call.message.chat.id, 'Другая - новая российская компания, занимающаяся русскоязычным аналом, не имеющая конкурентов на данный момент. Что подсказывает тебе твое инвесторское чутьё?')
    bot.register_next_step_handler(message, second_year);    
    
def second_year(message): #получаем фамилию
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Первая компания - Yahoo. Yahoo все еще не восстановилась после кризиса 2000-2001 годов', callback_data='yes'  
  ), 
        telebot.types.InlineKeyboardButton(  
            'Вторая - Яндекс. Поисковая система «Яндекс» является четвёртой среди поисковых систем мира по количеству обрабатываемых поисковых запросов.', callback_data='no'
  )  
    )  
    bot.send_message(  
        message.chat.id,  
        'конец игры',  
        reply_markup=keyboard 
        
    )
@bot.callback_query_handler(func=lambda call: True )
def callback_worker(call):
    if call.data == "yes": 
        bot.send_message(call.message.chat.id,'энд') 
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'энд');


    
    
# def first_year
# @bot.message_handler(commands=['help'])  
# def help_command(message):  
#     keyboard = telebot.types.InlineKeyboardMarkup()  
#     keyboard.add(  
#         telebot.types.InlineKeyboardButton(  
#             'Message the developer', url='telegram.me/artiomtb'  
#   )  
#     )  
#     bot.send_message(  
#         message.chat.id,  
#         '1) To receive a list of available currencies press /exchange.\n' +  
#         '2) Click on the currency you are interested in.\n' +  
#         '3) You will receive a message containing information regarding the source and the target currencies, ' +  
#         'buying rates and selling rates.\n' +  
#         '4) Click “Update” to receive the current information regarding the request. ' +  
#         'The bot will also show the difference between the previous and the current exchange rates.\n' +  
#         '5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.',  
#         reply_markup=keyboard  
#     )

# @bot.message_handler(commands=['calendar'])
# def get_calendar(message):
#     now = datetime.datetime.now() #Текущая дата
#     chat_id = message.chat.id
#     date = (now.year,now.month)
#     current_shown_dates[chat_id] = date #Сохраним текущую дату в словарь
#     markup = create_calendar(now.year,now.month)
#     bot.send_message(message.chat.id, "Пожалйста, выберите дату", reply_markup=markup)

def get_help(message):
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Поможете ему разбогатеть?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: True )
def callback_worker(call):
    if call.data == "yes": 
        bot.send_message(call.message.chat.id, 'Вам это зачтется : )');
        time.sleep(1)
        bot.send_message(call.message.chat.id,'Сколько раз в неделю вы бы хотели с ним связываться?') 
        bot.register_next_step_handler(call.message, get_time);
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Ваш баланс счета опустел : )');
        time.sleep(2)
        bot.send_message(call.message.chat.id, 'game over');
        time.sleep(10)
    
def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);
    
def get_time(message):
    global our_time;
    our_time=message.text;
    bot.send_message(message.from_user.id,'К сожалению, связь с прошлым — энергозатратный процесс, поэтому, чтобы получить возможность контактировать с Олегом более одного раза в день, нужно проходить квиз на финансовую грамотность и зарабатывать на электричество для поддержания контакта.');
    time.sleep(6)
    bot.send_message(message.from_user.id,'Для прохождения квиза надо написать команду /quiz. Заходя в игру два дня подряд, вы получаете дополнительный заряд энергии для перемещения в прошлое и отмены последнего принятого решения. Чтобы проверить его текущий баланс в прошлом, напиши /balance_past. Чтобы проверить его текущий баланс в настоящем, напиши /balance_present.  Если ты готов начать игру, нажми /go.')
    time.sleep(6)

        

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Студенты Сколтеча отправили андроида Олега в прошлое, чтобы он закупил акции успешных компаний и разбогател. 🤖");
        time.sleep(2)
        bot.send_message(message.chat.id, 'Однако в процессе путешествия во времени он потерял память и не помнит, куда вкладываться. Всё же он нашел способ связаться с будущим  - это Вы. Он наладил контакт с вашим устройством и теперь может отправлять вам короткие сообщения.')
        time.sleep(5)
        bot.send_message(message.chat.id, ' При себе он имеет начальный капитал в 5000$. Помоги Олегу заработать миллион долларов, а он в долгу не останется.')
        bot.register_next_step_handler(message, get_help); #следующий шаг – функция get_time
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши /start")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

# balance=100    
# @bot.message_handler(commands=['balance'])   
# def get_balance(message):
#     bot.send_message(message.from_user.id, balance);
# # @bot.message_handler(content_types=['text', 'document', 'audio'])

bot.polling(none_stop=True, interval=0)


      