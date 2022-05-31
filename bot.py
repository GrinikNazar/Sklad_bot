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
        '5': [['5', '5s', 'se'], (), ('akb', 'backlight')],
        '6': [['6', '6s', '6sPlus', '6Plus'], (), ('akb', 'backlight')],
        '7': [['7', '7Plus'], (), ('akb', 'backlight')],
        '8': [['8', '8Plus', 'se2020'], ('cover'), ('akb', 'backlight')],
        'X': [['X', 'Xs', 'XsM', 'XR'], ('cover'), ('akb', 'backlight')],
        '11': [['11', '11Pro', '11ProMax'], ('cover'), ('akb', 'backlight')],
        '12': [['12', '12Pro', '12ProMax', '12mini'], ('cover'), ('akb')]
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

    list_of_button = []
    markup = types.InlineKeyboardMarkup()

    if len(call.split('_')) == 2:
        #якщо запит не має ключа з словника тоді виводити клавіатуру з моделями
        for key, values in dict_of_models_submodels.items():
            if call.split('_')[0] in values[1]:
                list_of_button.append(types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}'))
            elif call.split('_')[0] in values[2]:
                list_of_button.append(types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}'))
        list_of_button.append(types.InlineKeyboardButton(f'back', callback_data=f'{call}_back'))
        markup.row(*list_of_button)    

    elif len(call.split('_')) == 3:
        #якщо ключ в запиті вказаний тоді виводити підмоделі
        for key, values in dict_of_models_submodels.items():
            if key == call.split('_')[-1]:
                if call.split('_')[0] in values[1]:
                    for but in values[0]:
                        list_of_button.append(types.InlineKeyboardButton(f'{but}', callback_data=f'{call}_{but}'))
                    break
                else:
                    for but in values[0]:
                        list_of_button.append(types.InlineKeyboardButton(f'{but}', callback_data=f'{call}_{but}_nocolor'))
                    break
        markup.row(*list_of_button)

    #Добавити кольори
    elif len(call.split('_')) == 4:
        for color in cover_color_choise:
            if call.split('_')[-1] in color[0]:
                markup.row(*[types.InlineKeyboardButton(f'{color_mod.title()}', callback_data=f'{call}_{color_mod}') for color_mod in color[1]])
                break
    
    #добавити кількість
    elif len(call.split('_')) == 5:
        markup.row(types.InlineKeyboardButton(f'1', callback_data=f'{call}_1'))
        markup.add(*[types.InlineKeyboardButton(f'{i}', callback_data=f'{call}_{i}') for i in range(2, 11)])

    return markup


@bot.callback_query_handler(func=lambda call: True)
def handler_mes(call):
    print(pre_reqest)
    if call.data.split('_')[-1] == 'back':
        bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=button_inine(pre_reqest))

    elif len(call.data.split('_')) == 6:
        bot.edit_message_text(call.data, call.message.chat.id, message_id=call.message.message_id)

    else:
        pre_reqest = call.data
        print(call.data.split('_'))
        bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=button_inine(call.data))


bot.polling()