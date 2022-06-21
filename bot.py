import engine
import keyboard
import iphone_db
import conf
import telebot
from telebot import types
import time
import threading
import random

bot = telebot.TeleBot(conf.config['token'])

users = {
    'Назар': 375385945,
    'Ваня': 239724045,
    'Саша': 350257882,
    'Артур': 372369919,
    'Льоша': 522646080,
    'Вадим': 1318753542

}


expect = [
    '🇺🇦 Слава Україні 🇺🇦',
    'Ой у лузі червона калина...',
    'рускій корабль іді нахуй',
    '..тін хуйло',
    '2-3 секунди і готово',
    'Так тримати, молодець \U0001F60E',
    'Хочу додому😭',
    'Працюю, на відміну від декого...',
    'Їбашу...',
    'Зараз блять...',
    'Хуярю...'
]


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
    button_8 = types.KeyboardButton('\U0001F4F2Touch iPad')
    button_9 = types.KeyboardButton('\U0001F250Копії')
    button_10 = types.KeyboardButton('\U0001FA79Клей АКБ + проклейки')
    button_11 = types.KeyboardButton('\U0001F50CІнше')
    markup.row(button_3, button_4, button_5, button_6)
    markup.row(button_7, button_2, button_8, button_9)
    markup.row(button_10, button_11)

    #авторизація
    if message.from_user.id in users.values():
        bot.send_message(message.chat.id, 'Привіт, вибирай дію \U0001F916', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Ти не авторизований, та й таке \U0001F4A9')
        bot.send_message(users['Назар'], f'Спроба запуску бота:\n{message.from_user.first_name}\n{message.from_user.username}\n{message.from_user.id}')


@bot.message_handler(commands=['my_id'])
def get_my_id(message):
    bot.send_message(375385945, f'{message.from_user.first_name}: {message.from_user.username}: {message.from_user.id}')


@bot.message_handler(commands=['list_ref'])
def get_list_ref(message):
    result = engine.list_ref_parts()
    global clipboard_list
    clipboard_list = ''
    for res in result[:-1]:
        bot.send_message(message.chat.id, res)
        clipboard_list += res
    else:
        bot.send_message(message.chat.id, result[-1])


@bot.message_handler(commands=['add_to_list'])
def add_to_list(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Добавити', switch_inline_query_current_chat='\n'), types.InlineKeyboardButton('Очистити', callback_data=f'clean_worksheet'))
    bot.send_message(message.chat.id, 'Список додаткових позицій', reply_markup=markup)


@bot.message_handler(commands=['get_null'])
def get_null(message):
    bot.send_message(message.chat.id, engine.get_null_things())


@bot.message_handler(content_types=['text'])
def some_func(message):
    global text_message
    text_message = message.text
    if message.text.split('\n')[0].rstrip() == '@FlarkenCatBot':
        bot.send_message(message.chat.id, 'Їбашу...')
        engine.add_to_list(message.text)
        bot.send_message(message.chat.id, 'Добавлено\U0001F91F')
    else:
        bot.send_message(message.chat.id, f'{message.text}', reply_markup=keyboard.action_menu_categories(message.text))


@bot.callback_query_handler(func=lambda call: True)
def handler_mes(call):
    
    if call.data.split('_')[-1] == 'back' and len(call.data.split('_')) == 3:
        bot.edit_message_text(text_message, call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.action_menu_categories(text_message))
    
    elif call.data.split('_')[:2] == 'list_order'.split('_'):
        result = engine.list_copy_and_battery(call.data.split('_')[-1], text_message)
        bot.edit_message_text(result, call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'clean_worksheet':
        engine.clean_worksheet()
        bot.send_message(call.message.chat.id, 'Додатковий список очищено!')

    elif call.data.split('_')[-1] == 'back':
        markup_key = keyboard.button_inine(('_').join(call.data.split('_')[:-2]))
        bot.edit_message_text(f'{text_message}:  {markup_key[1]}', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_key[0])

    elif len(call.data.split('_')) == 6 or call.data.split('_')[1] == 'search':
        # bot.edit_message_text(call.data, call.message.chat.id, message_id=call.message.message_id)
        bot.edit_message_text(random.choice(expect), call.message.chat.id, message_id=call.message.message_id)
        result_main = engine.main(call.data)

        if call.data.split('_')[1] == 'take':
            bot.edit_message_text(result_main[0], call.message.chat.id, message_id=call.message.message_id)
            if result_main[1]:
                bot.send_message(-674239373, f'{call.from_user.first_name}: {result_main[0]}')

        elif call.data.split('_')[1] == 'search':
            bot.edit_message_text(result_main, call.message.chat.id, message_id=call.message.message_id)

    else:
        markup_key = keyboard.button_inine(call.data)
        bot.edit_message_text(f'{text_message}:  {markup_key[1]}', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_key[0])


if __name__ == '__main__':

    time_bud = '10:00:00'

    threading.Thread(target=engine.main_time, args=((time_bud, bot))).start()

    bot.polling(non_stop=True, timeout=25)
