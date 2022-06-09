import engine
import keyboard
import iphone_db
import conf
import telebot
from telebot import types

bot = telebot.TeleBot(conf.config['token'])

users = {
    'Назар': 375385945,
    'Ваня': 239724045,
    'Саша': 350257882,
    'Артур': 372369919,
}

#Привітання, а також повідомлення яких кришок немає
@bot.message_handler(commands=['start'])
def send_message_welcome(message):
    
    #Головна клавіатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_2 = types.KeyboardButton('\U0001F6BDКришки')
    button_3 = types.KeyboardButton('\U0001F50BАКБ')
    button_4 = types.KeyboardButton('\U0001F60EСкло')
    button_5 = types.KeyboardButton('\U0001F526Пiдсвiтки')
    button_6 = types.KeyboardButton('\U0001F4F2Сенсори')
    button_7 = types.KeyboardButton('\U0001F4A9Рамки')  
    button_8 = types.KeyboardButton('\U0001F4F2Сенсори iPad')
    markup.row(button_3, button_4, button_5)
    markup.row(button_6, button_7, button_2)
    markup.row(button_8)

    #авторизація
    if message.from_user.id in users.values():
        bot.send_message(message.chat.id, 'Привіт, вибирай дію \U0001F916', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Ти не авторизований, та й таке \U0001F4A9')
        bot.send_message(users['Назар'], f'Спроба запуску бота:\n{message.from_user.first_name}\n{message.from_user.username}\n{message.from_user.id}')
    #Те що закінчилось
    # if gspread_my_py.get_cover_null():
    #     #string_of_covers_null = gspread_my_py.get_cover_null()
    #     #bot.send_message(message.chat.id, string_of_covers_null, reply_markup=markup)
    #     bot.send_message(message.chat.id, 'Привіт, вибирай дію \U0001F916', reply_markup=markup)
    # else:
    #     bot.send_message(message.chat.id, '!!!Все є!!!', reply_markup=markup)


@bot.message_handler(commands=['my_id'])
def get_my_id(message):
    bot.send_message(375385945, f'{message.from_user.first_name}: {message.from_user.username}: {message.from_user.id}')


@bot.message_handler(content_types=['text'])
def some_func(message):
    global text_message
    text_message = message.text
    bot.send_message(message.chat.id, f'{message.text}', reply_markup=keyboard.action_menu_categories(message.text))


@bot.callback_query_handler(func=lambda call: True)
def handler_mes(call):
    
    if call.data.split('_')[-1] == 'back' and len(call.data.split('_')) == 3:
        # print('3 back', call.data.split('_'))
        bot.edit_message_text(text_message, call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.action_menu_categories(text_message))
    
    elif call.data.split('_')[-1] == 'back':
        # print('back', call.data.split('_'))
        markup_key = keyboard.button_inine(('_').join(call.data.split('_')[:-2]))
        bot.edit_message_text(f'{text_message}:  {markup_key[1]}', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_key[0])

    elif len(call.data.split('_')) == 6 or call.data.split('_')[1] == 'search':
        bot.edit_message_text(call.data, call.message.chat.id, message_id=call.message.message_id)

        if call.data.split('_')[1] == 'take':
            result_main = engine.main(call.data) #результат повернення функції
            bot.edit_message_text(result_main, call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(-674239373, f'{call.from_user.first_name} {result_main}')

        elif call.data.split('_')[1] == 'search':
            result_main = engine.main(call.data)
            bot.edit_message_text(result_main, call.message.chat.id, message_id=call.message.message_id)

    else:
        # print('ok', call.data.split('_'))
        markup_key = keyboard.button_inine(call.data)
        bot.edit_message_text(f'{text_message}:  {markup_key[1]}', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_key[0])


try:
    bot.polling()
except bot.ReadTimeout:
    print('Time out')