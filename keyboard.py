from telebot import types
import iphone_db

#функція створення клавіатури для вибору моделей і кольорів
def button_inine(call):

    title_message = ''

    markup = types.InlineKeyboardMarkup()
    #добавити модель
    if len(call.split('_')) == 2:
        title_message += 'Вибір моделі'
        markup.row(*[types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}') for key in iphone_db.choise_models(call.split('_')[0])])
        markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))

    #добавити підмодель
    elif len(call.split('_')) == 3:
        title_message += 'Вибір моделі'
        fr_db_data = iphone_db.choise_submodels(call.split('_')[0], call.split('_')[-1])
        if not fr_db_data:
            markup.row(*[types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}_nocolor') for key in fr_db_data])
        else:
            markup.row(*[types.InlineKeyboardButton(f'{key}', callback_data=f'{call}_{key}') for key in fr_db_data])
        markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))

    #Добавити кольори
    elif len(call.split('_')) == 4:
        string_color = iphone_db.choise_colors(call.split('_')[0], call.split('_')[-1])
        if string_color:
            title_message += 'Вибір кольору чи підпункту'
            string_color = string_color.split('\r\n')
            markup.row(*[types.InlineKeyboardButton(f'{color_mod.title()}', callback_data=f'{call}_{color_mod}') for color_mod in string_color])
            markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))
        else:
            title_message += 'Кількість'
            markup.row(types.InlineKeyboardButton(f'1', callback_data=f'{call}_nocolor_1'))
            markup.add(*[types.InlineKeyboardButton(f'{i}', callback_data=f'{call}_nocolor_{i}') for i in range(2, 11)])
            markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))

    #добавити кількість
    elif len(call.split('_')) == 5:
        title_message += 'Кількість'
        markup.row(types.InlineKeyboardButton(f'1', callback_data=f'{call}_1'))
        markup.add(*[types.InlineKeyboardButton(f'{i}', callback_data=f'{call}_{i}') for i in range(2, 11)])
        markup.row(types.InlineKeyboardButton('Назад', callback_data=f'{call}_back'))

    #функція повертає клавіатуру в залежності від умов
    return (markup, title_message)


#функція для створення клавіатури
def action_menu_categories(message):
    change_categories = iphone_db.gen_keyboard(message[1:])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Взяти', callback_data=f'{change_categories}_take'), types.InlineKeyboardButton('Знайти', callback_data=f'{change_categories}_search'))
    return markup