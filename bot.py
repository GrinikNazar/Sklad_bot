import engine
import keyboard
import iphone_db
import conf
import telebot
import threading
import random
import handler_wp
import work_progress_db
import os
import scores_handler
import score_table_change
import excel_statistic

bot = telebot.TeleBot(conf.config['token'])

сhat_work_progress = conf.сhat_work_progress
chat_history_parts = conf.chat_history_parts

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


#для відправки в бот повідомлення про виключення/помилку
def bot_error_message(user_id, message, bot = bot):
    bot.send_message(user_id, message)


def autorize_hose(func):
    def wrapper(message):
        if message.from_user.id in users.values():
            if message.chat.id == сhat_work_progress and message.text.split('\n')[0].rstrip() == '@FlarkenCatBot _wp':
                result = func(message)
            elif message.chat.id == сhat_work_progress: #для авторизованих користувачів
                return None
            else:
                result = func(message)
        elif message.from_user.id not in users.values() and message.chat.id == сhat_work_progress: #для не авторизованих
            return None
        else:
            result = bot.send_message(message.chat.id, 'Ти не авторизований, та й таке \U0001F4A9')
            bot.send_message(users['Назар'], f'Спроба запуску бота:\n{message.from_user.first_name}\n{message.from_user.username}\n{message.from_user.id}')
        return result
    return wrapper


def get_smile_and_uk_name(call):
    message_description = iphone_db.ret_uk_request(call.data.split('_')[0])
    smile = iphone_db.get_smiles_from_db(call.data.split('_')[0])
    return f'{smile}{message_description}'


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
    user_firs_name = message.from_user.first_name
    user_nick_name = message.from_user.username
    user_id = message.from_user.id
    bot.send_message(users['Назар'], f'{user_firs_name}: {user_id}', reply_markup=keyboard.add_user(user_firs_name, user_nick_name, user_id))
    bot.send_message(users['Ваня'], f'{user_firs_name}: {user_id}', reply_markup=keyboard.add_user(user_firs_name, user_nick_name, user_id))

    if message.from_user.id != message.chat.id:
        bot.send_message(users['Назар'], f'id чату:{message.chat.id}')
        bot.send_message(users['Ваня'], f'id чату:{message.chat.id}')


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


@bot.message_handler(commands=['user_delete'])
@autorize_hose
def delete_users_from_bot(message):
    if message.from_user.id == users['Ваня'] or message.from_user.id == users['Назар']:
        bot.send_message(message.chat.id, 'Список користувачів \U0001F4DD', reply_markup=keyboard.users_list_to_delete())
    else:
        bot.send_message(message.chat.id, 'У тебе немає доступу \U0001F4A9')


@bot.message_handler(commands=['update_score'])
@autorize_hose
def update_score_table(message):
    if message.from_user.id == users['Ваня'] or message.from_user.id == users['Назар']:
        score_table_change.main()
        bot.send_message(message.chat.id, 'Дані оновлені')
    else:
        bot.send_message(message.chat.id, 'У тебе немає доступу \U0001F4A9')


@bot.message_handler(content_types=['text'])
@autorize_hose
def some_func(message):
    if message.text.split('\n')[0].rstrip() == f'@{bot.get_me().username} _add_list':
        bot.send_message(message.chat.id, 'Секундочку...')
        try:
            engine.add_to_list(message.text)
            bot.send_message(message.chat.id, 'Добавлено\U0001F91F')
        except IndexError:
            bot.send_message(message.chat.id, 'Невірний формат вводу, спробуй ще раз')

    # WorkProgress    
    elif message.text.split('\n')[0].rstrip() == f'@{bot.get_me().username} _wp':
        result = handler_wp.handler_wp(message.text, message.from_user.id)
        if result == '' or not result:
            work_progress_db.update_work_progress(message.from_user.id, message.text)
            null_result_scores = scores_handler.main_scores(message.from_user.id, 'return-null-scores') # Показує інформацію за які роботи не нараховані бали
            res_string = 'Список робіт за які не нараховані бали:\n'
            if null_result_scores:
                for value in null_result_scores:
                    res_string += f'{value}\n'
                res_string = res_string.rstrip()
                bot.send_message(message.chat.id, res_string, reply_markup=keyboard.confirm())
            else:
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
        bot.edit_message_text(get_smile_and_uk_name(call), call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.action_menu_categories(get_smile_and_uk_name(call)))
    
    elif call.data.split('_')[:2] == 'list_order'.split('_'):
        result = engine.list_copy_and_battery(call.data.split('_')[-1], iphone_db.get_smiles_from_db(call.data.split('_')[-1]))
        bot.edit_message_text(result, call.message.chat.id, message_id=call.message.message_id)
    
    elif call.data == 'confirm_button':
        user_id = call.from_user.id
        for key, value in users.items():
            if value == user_id:
                user = key
        
        # TODO: поправив конфірм
        iphone_db.write_confirm_user(user_id)

        begin = excel_statistic.get_user_score_when_came_to_point(user_id)

        work_progress_finnaly = scores_handler.main_scores(user_id)
        work_progress_finnaly = f"{user}\n{work_progress_finnaly}"
        bot.send_message(сhat_work_progress, work_progress_finnaly)
        bot.send_message(call.message.chat.id, '\U0001F916Відправив\U0001F91F')
        # TODO: Ексепшн виникає можливо черех застарілий call.id - якщо хтось повторно не згенерував повідомлення з прогресом і нажав конфірм на раніше створене повідомлення
        # bot.answer_callback_query(call.id, '\U0001F916Відправив\U0001F91F')
        
        end = excel_statistic.get_user_score_when_came_to_point(user_id)

        result_statistic = excel_statistic.compare_scores(user, begin, end)
        if result_statistic:
            bot.send_message(сhat_work_progress, result_statistic)
        

    elif call.data == 'reset_data_user':
        user_id = call.from_user.id
        work_progress_db.delete_user_work_progress(user_id)
        bot.edit_message_text('\U0001F32AДанi скинуті в 0\U000026A1', call.message.chat.id, message_id=call.message.message_id)

    elif call.data == 'reset-data-from-bot':
        user_id = call.from_user.id
        string_for_bot_back_up = ''
        tuple_result_db_select = work_progress_db.select_back_up_parts(user_id)
        if len(tuple_result_db_select[0]) == 0:
            bot.edit_message_text('Ти ще нічого з бота не брав!', call.message.chat.id, message_id=call.message.message_id)
        else:
            for string in tuple_result_db_select[1]:
                string_for_bot_back_up += string + '\n'
            string_for_bot_back_up = string_for_bot_back_up.rstrip()
            bot.edit_message_text(string_for_bot_back_up, call.message.chat.id, message_id=call.message.message_id)
            engine.search_parts_for_add_like_back_up(tuple_result_db_select[0]) #повернути на місце всі запчастини
            work_progress_db.delete_from_back_up_parts(user_id) #очистка даних по запчастинах які взяли з бота
            bot.send_message(call.message.chat.id, 'Дані очищені і повернуті на місце')

    elif call.data == 'reset_all_data_user':
        user_id = call.from_user.id
        user_confirm_list = [users['Назар'], users['Ваня']]
        if user_id in user_confirm_list:
            work_progress_db.reset_data_base()
            bot.edit_message_text('\U0001F32AОчищено\U000026A1', call.message.chat.id, message_id=call.message.message_id)
        else:
            bot.answer_callback_query(call.id, 'Тобі не можна це робити')

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

    elif call.data.split('_')[0] == 'add-user-to-bot':
        user_name = call.data.split('_')[1]
        user_nick_name = call.data.split('_')[2]
        user_id = int(call.data.split('_')[-1])
        last_name = ''
        last_name = user_nick_name if user_name == 'None' else user_name
        answer_db_request = iphone_db.write_new_user_to_data_base(last_name, user_id)
        bot.answer_callback_query(call.id, answer_db_request)

    elif call.data.split('_')[0] == 'delete-user-from-bot':
        user_name = call.data.split('_')[1]
        user_id = int(call.data.split('_')[-1])
        bot.edit_message_text(f'Дійсно видалити користувача {user_name} ???', call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard.user_delete_confirm_button(user_name, user_id))

    elif call.data.split('_')[0] == 'delete-user-from-bot-yes-or-no':
        result = call.data.split('_')[1]
        user_name = call.data.split('_')[2]
        user_id = int(call.data.split('_')[-1])
        if result == 'yes':
            iphone_db.delete_from_db_users(user_id)
            bot.edit_message_text(f'Користувача {user_name} видалено!', call.message.chat.id, message_id=call.message.message_id)
        else:
            bot.edit_message_text(f'Фух, пронесло \U0001F628', call.message.chat.id, message_id=call.message.message_id)

    elif call.data.split('_')[-1] == 'back':
        markup_key = keyboard.button_inine(('_').join(call.data.split('_')[:-2]))
        bot.edit_message_text(f'{get_smile_and_uk_name(call)}:  {markup_key[1]}', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_key[0])

    elif len(call.data.split('_')) == 6 or call.data.split('_')[1] == 'search':
        bot.edit_message_text(random.choice(expect), call.message.chat.id, message_id=call.message.message_id)
        result_main = engine.main(call.data)

        if call.data.split('_')[1] == 'take':
            try:
                bot.edit_message_text(result_main[0], call.message.chat.id, message_id=call.message.message_id)
                if len(result_main) > 2:
                    work_progress_db.tabble_for_hose(call.from_user.id, result_main[2])
                    work_progress_db.write_backup_parts(call.from_user.id, result_main[3])
                if result_main[1]:
                    if chat_history_parts:
                        bot.send_message(chat_history_parts, f'{call.from_user.first_name}: {result_main[0]}')
            except TypeError:
                bot.edit_message_text('Ой, шось сталось', call.message.chat.id, message_id=call.message.message_id)

        elif call.data.split('_')[1] == 'search':
            bot.edit_message_text(f"{iphone_db.get_smiles_from_db(call.data.split('_')[0])}{result_main[0]}", call.message.chat.id, message_id=call.message.message_id)
            try:
                for res_m in result_main[1:]:
                    bot.send_message(call.message.chat.id, res_m)
            except IndexError:
                pass

    else:
        markup_key = keyboard.button_inine(call.data)
        bot.edit_message_text(f'{get_smile_and_uk_name(call)}:  {markup_key[1]}', call.message.chat.id, message_id=call.message.message_id, reply_markup=markup_key[0])


if __name__ == '__main__':

    null_time = 'null_time'
    reset_time = 'reset_time'
    wp_reminder = 'wp_reminder'
    wp_reminder_2 = 'wp_reminder_2'

    time_bud = iphone_db.time_base(null_time)
    time_reset_db_users = iphone_db.time_base(reset_time)
    time_wp_reminder = iphone_db.time_base(wp_reminder)
    time_wp_reminder_2 = iphone_db.time_base(wp_reminder_2)

    threading.Thread(target=engine.main_time, args=((time_bud, bot, null_time))).start() #список відсутніх позицій в 10:00

    threading.Thread(target=engine.main_time, args=((time_reset_db_users, bot, reset_time))).start() #ресет бази даних о 23:59

    threading.Thread(target=engine.main_time, args=((time_wp_reminder, bot, wp_reminder))).start()

    threading.Thread(target=engine.main_time, args=((time_wp_reminder_2, bot, wp_reminder_2))).start()


    while True:
        try:
            bot.infinity_polling(timeout=10)
        except BaseException as err:
            continue
