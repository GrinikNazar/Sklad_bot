from cgitb import text
import gspread_my_py
import iphone_db
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
    if gspread_my_py.get_cover_null():
        bot.send_message(message.chat.id, '!!!Кришки які закінчились!!!', reply_markup=markup)
        string_of_covers_null = gspread_my_py.get_cover_null()
        bot.send_message(message.chat.id, string_of_covers_null)
    else:
        bot.send_message(message.chat.id, '!!!Всі кришки є!!!', reply_markup=markup)

#функція для створення клавіатури
def action_menu_categories(message):
    change_categories = iphone_db.gen_keyboard(message)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Взяти', callback_data=f'{change_categories}_take'), types.InlineKeyboardButton('Знайти', callback_data=f'{change_categories}_search'))
    return markup


@bot.message_handler(content_types=['text'])
def some_func(message):
    global text_message
    text_message = message.text
    bot.send_message(message.chat.id, f'{message.text}', reply_markup=action_menu_categories(message.text))

#функція створення клавіатури для вибору моделей і кольорів
def button_inine(call):

    markup = types.InlineKeyboardMarkup()
    #добавити модель
    if len(call.split('_')) == 2:
        markup.row(*[types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}') for key in iphone_db.choise_models(call.split('_')[0])])
        markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))

    #добавити підмодель
    elif len(call.split('_')) == 3:
        if not iphone_db.choise_colors(call.split('_')[0], call.split('_')[-1]):
            markup.row(*[types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}_nocolor') for key in iphone_db.choise_submodels(call.split('_')[0], call.split('_')[-1])])
        else:
            markup.row(*[types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}') for key in iphone_db.choise_submodels(call.split('_')[0], call.split('_')[-1])])
        markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))

    #Добавити кольори
    elif len(call.split('_')) == 4:
        print(call.split('_'))
        string_color = iphone_db.choise_colors(call.split('_')[0], call.split('_')[-1])
        if string_color:
            string_color = string_color.split('\r\n')
            markup.row(*[types.InlineKeyboardButton(f'{color_mod.title()}', callback_data=f'{call}_{color_mod}') for color_mod in string_color])
            markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))

    #добавити кількість
    elif len(call.split('_')) == 5:
        markup.row(types.InlineKeyboardButton(f'1', callback_data=f'{call}_1'))
        markup.add(*[types.InlineKeyboardButton(f'{i}', callback_data=f'{call}_{i}') for i in range(2, 11)])
        markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))

    #функція повертає клавіатуру в залежності від умов
    return markup


@bot.callback_query_handler(func=lambda call: True)
def handler_mes(call):
    
    if call.data.split('_')[-1] == 'back' and len(call.data.split('_')) == 3:
        bot.edit_message_text(text_message, call.message.chat.id, message_id=call.message.message_id, reply_markup=action_menu_categories(text_message))
    
    elif call.data.split('_')[-1] == 'back':
        bot.edit_message_text(text_message, call.message.chat.id, message_id=call.message.message_id, reply_markup=button_inine(('_').join(call.data.split('_')[:-2])))

    elif len(call.data.split('_')) == 6:
        print(call.data.split('_'))
        bot.edit_message_text(call.data, call.message.chat.id, message_id=call.message.message_id)

    else:
        print(call.data.split('_'))
        bot.edit_message_text('Вибір моделі', call.message.chat.id, message_id=call.message.message_id, reply_markup=button_inine(call.data))

bot.polling()