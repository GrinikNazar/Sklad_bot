import gspread_my_py
import conf
import telebot
from telebot import types

bot = telebot.TeleBot(conf.config['token'])

#Привітання, а також повідомлення яких кришок немає
@bot.message_handler(commands=['start'])
def send_message_welcome(message):
    
    #Головна клавіатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton('/start')
    button_2 = types.KeyboardButton('Кришки')
    button_3 = types.KeyboardButton('АКБ')
    button_4 = types.KeyboardButton('Скло')
    button_5 = types.KeyboardButton('Підсвітки')
    button_6 = types.KeyboardButton('Сенсори')
    button_7 = types.KeyboardButton('Рамки')  
    markup.row(button_3, button_4, button_5)
    markup.row(button_6, button_7, button_2)
    markup.row(button_1)

    #Те що закінчилось
    chat_id_bot = 375385945
    if gspread_my_py.get_cover_null():
        bot.send_message(chat_id_bot, '!!!Кришки які закінчились!!!', reply_markup=markup)
        string_of_covers_null = gspread_my_py.get_cover_null()
        bot.send_message(chat_id_bot, string_of_covers_null)
    else:
        bot.send_message(chat_id_bot, '!!!Всі кришки є!!!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def some_func(message):
    if message.text == 'Кришки':
        markup = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton('Взяти', callback_data='cover_take')
        b2 = types.InlineKeyboardButton('Знайти', callback_data='cover_search')
        b3 = types.InlineKeyboardButton('Добавити', callback_data='cover_add')
        markup.add(b1, b2, b3)
        bot.send_message(message.chat.id, 'Що потрібно зробити з кришками?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Шось не так')

def button_inine(call):
    list_of_models = ['8', 'X', '11', '12']
    markup = types.InlineKeyboardMarkup()
    list_of_button = []
    for value in list_of_models:
        list_of_button.append(types.InlineKeyboardButton(value, callback_data=f'{call}_{value}')) 
    return (markup, list_of_button) 

@bot.callback_query_handler(func=lambda call: True)
def handler_mes(call):
    if call.data == 'cover_take':
        tupple_of_function = button_inine(call.data)  
        tupple_of_function[0].row(tupple_of_function[1][0], tupple_of_function[1][1], tupple_of_function[1][2], tupple_of_function[1][3])
        bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=tupple_of_function[0])

    elif call.data == 'cover_search':
        markup = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton('8', callback_data=f'{call.data}_8')
        b2 = types.InlineKeyboardButton('X', callback_data=f'{call.data}_X')
        b3 = types.InlineKeyboardButton('11', callback_data=f'{call.data}_11')
        b4 = types.InlineKeyboardButton('12', callback_data=f'{call.data}_12')
        markup.row(b1, b2, b3, b4)
        bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data == 'cover_add':
        markup = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton('8', callback_data=f'{call.data}_8')
        b2 = types.InlineKeyboardButton('X', callback_data=f'{call.data}_X')
        b3 = types.InlineKeyboardButton('11', callback_data=f'{call.data}_11')
        b4 = types.InlineKeyboardButton('12', callback_data=f'{call.data}_12')
        markup.row(b1, b2, b3, b4)
        bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    
    elif call.data == 'cover_take_8':
        pass



#Приклад обробника
# @bot.callback_query_handler(func=lambda call: True)
# def handle(call):
#     if call.data == 'cover':
#         bot.send_message(call.message.chat.id, 'Які дії з кришками ви хочете зробити?')
#         bot.answer_callback_query(call.id)


# @bot.message_handler(content_types='text')
# def get_cover(message):
#     chat_id_bot = 375385945
#     chat_id_chat = -674239373
#     if message.text == f'@{bot.get_me().username} q':
#         bot.send_message(chat_id_bot, 'О здоров)')
#     elif message.text[:3] == 'add':
#         list_of_addicted = message.text[4:].split('\n')
#         gspread_my_py.add_cover(list_of_addicted)
#         bot.send_message(chat_id_bot, 'Кришки добавлені')

#     elif message.text[:-3:-1] in [str(x) + ' ' for x in range(1, 20)]:
#         try:
#             user = message.chat.first_name
#             mes = gspread_my_py.get_cover(message.text)
#             bot.send_message(chat_id_bot, f'{user} {mes[0]}\n{mes[1]}')
#             bot.send_message(chat_id_chat, f'{user} {mes[0]}\n{mes[1]}')
#         except ValueError:
#             bot.reply_to(message, 'Вася, напиши нормально! Шо це за каляки маляки?')
#         except UnboundLocalError:
#             bot.reply_to(message, 'Вася, напиши нормально! Шо це за каляки маляки?')
#     else:
#         if gspread_my_py.search_covers(message.text):
#             bot.reply_to(message, 'Вдалося знайти:')
#             bot.send_message(message.chat.id, gspread_my_py.search_covers(message.text))
#         else:
#             bot.send_message(message.chat.id, 'Чувак, ти шось не то вводиш, подивись звідки руки!')


bot.polling()