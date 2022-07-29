import engine
import keyboard
import iphone_db
import conf
import telebot
from telebot import types
import time
import threading
import random
import handler_wp
import work_progress_db
import os

bot = telebot.TeleBot(conf.conf_test['token'])

users = iphone_db.select_hose()

expect = [
    '🇺🇦 Слава Україні 🇺🇦',
    '2-3 секунди і готово',
    'Так тримати, молодець \U0001F60E',
    'Хочу додому😭',
    'Працюю, на відміну від декого...',
    'Секундочку...',
    'Вже майже майже...',
    'Скидиш',
]


def autorize_hose(func):
    def wrapper(message):
        if message.from_user.id in users.values():
            if message.chat.id == -740139442 and message.text.split('\n')[0].rstrip() == '@FlarkenCatBot _wp':
                result = func(message)
            elif message.chat.id == -740139442:
                return None
            else:
                result = func(message)
        else:
            result = bot.send_message(message.chat.id, 'Ти не авторизований, та й таке \U0001F4A9')
            bot.send_message(users['Назар'], f'Спроба запуску бота:\n{message.from_user.first_name}\n{message.from_user.username}\n{message.from_user.id}')
        return result
    return wrapper


@bot.message_handler(commands=['start'])
@autorize_hose
def send_message_welcome(message):
    bot.send_message(message.chat.id, 'Привіт, вибирай дію \U0001F916', reply_markup=keyboard.main_board())


@bot.message_handler(commands=['readme'])
@autorize_hose
def send_message_welcome(message):
    with open(os.path.join(os.path.dirname(__file__), 'WP.jpg'), 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['my_id'])
def get_my_id(message):
    bot.send_message(375385945, f'{message.from_user.first_name}: {message.from_user.username}: {message.from_user.id}')
    if message.from_user.id != message.chat.id:
        bot.send_message(375385945, f'id чату:{message.chat.id}')


@bot.message_handler(commands=['list_ref'])
@autorize_hose
def get_list_ref(message):
    result = keyboard.list_ref_parts()
    bot.send_message(message.chat.id, 'Виберіть варіант формування списку:', reply_markup=result)


@bot.message_handler(commands=['add_to_list'])
@autorize_hose
def add_to_list(message):
    result = keyboard.add_to_list()
    bot.send_message(message.chat.id, 'Список додаткових позицій\nІнструкція: Позиція*кількість\nПриклад: АКБ iPhone 6 ( 0-2 циклу) оригінал*2', reply_markup=result)


@bot.message_handler(commands=['get_null'])
@autorize_hose
def get_null(message):
    bot.send_message(message.chat.id, engine.get_null_things())


@bot.message_handler(commands=['other'])
@autorize_hose
def other_function(message):
    bot.send_message(message.chat.id, 'Додаткові можливості Флеркена', reply_markup=keyboard.other_key(message.from_user.id))


@bot.message_handler(content_types=['text'])
@autorize_hose
def some_func(message):
    global text_message
    text_message = message.text
    if message.text.split('\n')[0].rstrip() == f'@{bot.get_me().username} _add_list':
        bot.send_message(message.chat.id, 'Секундочку...')
        try:
            engine.add_to_list(message.text)
            bot.send_message(message.chat.id, 'Добавлено\U0001F91F')
        except IndexError:
            bot.send_message(message.chat.id, 'Невірний формат вводу, спробуй ще раз')

    elif message.text.split('\n')[0].rstrip() == f'@{bot.get_me().username} _time':
        engine.change_time_null(message.text)
        bot.send_message(message.chat.id, 'Час змінено\U0001F91F')

    # WorkProgress    
    elif message.text.split('\n')[0].rstrip() == f'@{bot.get_me().username} _wp':
        result = handler_wp.handler_wp(message.text, message.from_user.id)
        if result == '' or not result:
            work_progress_db.update_work_progress(message.from_user.id, message.text)
            bot.send_message(message.chat.id, '\U0001F9A5Все зійшлось\U0001F9A5', reply_markup=keyboard.confirm())
        else:
            if result == True:
                bot.send_message(message.chat.id, result[0])
            work_progress_db.update_work_progress(message.from_user.id, message.text)
            bot.send_message(message.chat.id, result)
        
    else:
        try:
            bot.send_message(message.chat.id, f'{message.text}', reply_markup=keyboard.action_menu_categories(message.text))
        except TypeError:
            bot.send_message(users['Назар'], 'Поламалось на "keyboard.action_menu_categories"')


@bot.callback_query_handler(func=lambda call: True)
def handler_mes(call):
    
    if call.data.split('_')[-1] == 'back' and len(call.data.split('_')) == 3:
        bot.edit_message_text(text_message, call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.action_menu_categories(text_message))
    
    elif call.data.split('_')[:2] == 'list_order'.split('_'):
        result = engine.list_copy_and_battery(call.data.split('_')[-1], text_message)
        bot.edit_message_text(result, call.message.chat.id, message_id=call.message.message_id)
    
    elif call.data == 'confirm_button':
        user_id = call.from_user.id
        for key, value in users.items():
            if value == user_id:
                user = key 
        wp_result = work_progress_db.select_work_progress(user_id)
        work_progress_finnaly = f"{user}\n{wp_result}"
        bot.send_message(-740139442, work_progress_finnaly)
        bot.answer_callback_query(call.id, '\U0001F916Відправив\U0001F91F')

    elif call.data == 'reset_data_user':
        user_id = call.from_user.id
        work_progress_db.delete_user_work_progress(user_id)
        bot.answer_callback_query(call.id, '\U0001F32AДанi скинуті в 0\U000026A1')

    elif call.data == 'reset_all_data_user':
        user_id = call.from_user.id
        user_confirm_list = [users['Назар'], users['Ваня']]
        if user_id in user_confirm_list:
            work_progress_db.reset_data_base()
            bot.answer_callback_query(call.id, 'Очищено')
        else:
            bot.answer_callback_query(call.id, 'Тобі не можна це робити, шланг')

    elif call.data == 'clean_worksheet':
        engine.clean_worksheet()
        bot.send_message(call.message.chat.id, 'Додатковий список очищено!')

    elif call.data.split('_')[:-1] == 'ref_parts'.split('_'):
        if call.data.split('_')[-1] == 'min':
            result = engine.list_ref_parts(1)
            for res in result[:-1]:
                bot.send_message(call.message.chat.id, res)
            else:
                bot.send_message(call.message.chat.id, result[-1])
        else:
            result = engine.list_ref_parts()
            for res in result[:-1]:
                bot.send_message(call.message.chat.id, res)
            else:
                bot.send_message(call.message.chat.id, result[-1])

    elif call.data.split('_')[-1] == 'back':
        markup_key = keyboard.button_inine(('_').join(call.data.split('_')[:-2]))
        bot.edit_message_text(f'{text_message}:  {markup_key[1]}', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_key[0])

    elif len(call.data.split('_')) == 6 or call.data.split('_')[1] == 'search':
        bot.edit_message_text(random.choice(expect), call.message.chat.id, message_id=call.message.message_id)
        result_main = engine.main(call.data)

        if call.data.split('_')[1] == 'take':
            try:
                bot.edit_message_text(result_main[0], call.message.chat.id, message_id=call.message.message_id)
                if len(result_main) > 2:
                    work_progress_db.tabble_for_hose(call.from_user.id, result_main[2])
                if result_main[1]:
                    bot.send_message(-674239373, f'{call.from_user.first_name}: {result_main[0]}')
            except TypeError:
                bot.edit_message_text('Ой, шось сталось', call.message.chat.id, message_id=call.message.message_id)

        elif call.data.split('_')[1] == 'search':
            bot.edit_message_text(result_main, call.message.chat.id, message_id=call.message.message_id)

    else:
        markup_key = keyboard.button_inine(call.data)
        bot.edit_message_text(f'{text_message}:  {markup_key[1]}', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_key[0])


if __name__ == '__main__':

    null_time = 'null_time'
    reset_time = 'reset_time'

    time_bud = iphone_db.time_base(null_time)
    time_reset_db_users = iphone_db.time_base(reset_time)

    threading.Thread(target=engine.main_time, args=((time_bud, bot, null_time))).start() #список відсутніх позицій в 10:00

    threading.Thread(target=engine.main_time, args=((time_reset_db_users, bot, reset_time))).start() #ресет бази даних

    bot.polling(non_stop=True, timeout=600)
