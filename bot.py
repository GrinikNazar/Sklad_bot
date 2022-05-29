from optparse import Values
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

def action_menu_categories(message):
    menu_change_categories = {'Кришки': 'cover', 'АКБ': 'akb', 'Скло': 'glass', 'Підсвітки': 'backlight', 'Сенсори': 'touch', 'Рамки': 'frame'}
    markup = types.InlineKeyboardMarkup()
    for key, value in menu_change_categories.items():
        if message == key:
            markup.add(types.InlineKeyboardButton('Взяти', callback_data=f'{value}_take'), types.InlineKeyboardButton('Знайти', callback_data=f'{value}_search'), types.InlineKeyboardButton('Добавити', callback_data=f'{value}_add'))
            break
    return markup


@bot.message_handler(content_types=['text'])
def some_func(message):
    bot.send_message(message.chat.id, f'{message.text}', reply_markup=action_menu_categories(message.text))

def button_inine(call):
    dict_of_models_submodels = {
        '5': ['5', '5s', 'se'],
        '6': ['6', '6s', '6sPlus', '6Plus'],
        '7': ['7', '7Plus'],
        '8': ['8', '8Plus', 'se2020'],
        'X': ['X', 'Xs', 'XsM', 'XR'],
        '11': ['11', '11Pro', '11ProMax'],
        '12': ['12', '12Pro', '12ProMax', '12mini']
    }

    model_class = {
        'cover': ['8', '8Plus', 'se2020','X', 'Xs', 'XsM', 'XR', '11', '11Pro', '11ProMax', '12', '12Pro', '12ProMax', '12mini'],
        'glass': [],
        'touch': []
    }

    cover_color_choise = (
        (('8', '8Plus', ), ('gold', 'silver', 'space gray', 'red')),
        (('se2020'), ('black', 'red', 'white')),
        (('X'), ('space gray', 'silver')),
        (('Xs', 'XsM'), ('gold', 'silver', 'space gray')),
        (('XR'), ('black', 'white', 'blue', 'coral', 'red', 'yellow')),
        (('11'), ('black', 'white', 'green', 'purple', 'red', 'yellow')),
        (('11Pro', '11ProMax'), ('gold', 'silver', 'space gray', 'midnight green')),
        (('12'), ('black', 'white', 'green', 'purple', 'red', 'blue')),
        (('12Pro', '12ProMax'), ('gold', 'silver', 'pasific blue', 'graphite')),
        (('12mini'), ('black', 'white', 'blue', 'coral', 'red', 'green'))
    )

    color_glass = {
        'black': [],
        'white': []
    }

    #Exapmle
    #cover_take_8_8Plus_black
    #len() = 5
    if call.split('_')[0] == 'cover' or call.split('_')[0] == 'touch' or call.split('_')[0] == 'glass':
        len_request = 5
    else:
        len_request = 4

    len_call = len(call.split('_')) 
    list_of_button = []
    markup = types.InlineKeyboardMarkup()

    if len_call == 2:
        #якщо запит не має ключа з словника тоді виводити клавіатуру з моделями
        for key in dict_of_models_submodels.keys():
            list_of_button.append(types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}'))
        markup.row(*list_of_button)    

    elif len_call == 3:
        #якщо ключ в запиті вказаний тоді виводити підмоделі
        for key, values in dict_of_models_submodels.items():
            if key == call.split('_')[-1]:
                for but in values:
                    list_of_button.append(types.InlineKeyboardButton(f'{but}', callback_data=f'{call}_{but}'))
                break
        markup.row(*list_of_button)

    #Добавити кольори
    elif len_request == 5:
        if call.split('_')[-1] in model_class['cover']:
            for color in cover_color_choise:
                if call.split('_')[-1] in color[0]:
                    for color_mod in color[1]:
                        list_of_button.append(types.InlineKeyboardButton(f'{color_mod.title()}', callback_data=f'{call}_{color_mod}'))
                    break
            markup.row(*list_of_button)
        return markup
    else:
        #видати заит
        pass

    return markup

@bot.callback_query_handler(func=lambda call: True)
def handler_mes(call):
    if len(call.data.split('_')) == 5:
        bot.edit_message_text(button_inine(call.data), call.message.chat.id, message_id=call.message.message_id) 
    else:
        print(call.data.split('_'))
        bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=button_inine(call.data))
    
    # elif call.data == 'cover_search':
    #     markup = types.InlineKeyboardMarkup()
    #     b1 = types.InlineKeyboardButton('8', callback_data=f'{call.data}_8')
    #     b2 = types.InlineKeyboardButton('X', callback_data=f'{call.data}_X')
    #     b3 = types.InlineKeyboardButton('11', callback_data=f'{call.data}_11')
    #     b4 = types.InlineKeyboardButton('12', callback_data=f'{call.data}_12')
    #     markup.row(b1, b2, b3, b4)
    #     bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    # elif call.data == 'cover_add':
    #     markup = types.InlineKeyboardMarkup()
    #     b1 = types.InlineKeyboardButton('8', callback_data=f'{call.data}_8')
    #     b2 = types.InlineKeyboardButton('X', callback_data=f'{call.data}_X')
    #     b3 = types.InlineKeyboardButton('11', callback_data=f'{call.data}_11')
    #     b4 = types.InlineKeyboardButton('12', callback_data=f'{call.data}_12')
    #     markup.row(b1, b2, b3, b4)
    #     bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    
    # elif call.data == 'cover_take_8':
    #     pass



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