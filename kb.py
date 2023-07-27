from aiogram import types

def menu_keyboard(cur_lang):
    if cur_lang == 'ru': 
        main_menu = types.InlineKeyboardMarkup(row_width=5)
        main_menu.add(types.InlineKeyboardButton('Перейти в режим "Грамматика"', callback_data='grammar_mode'))
        main_menu.add(types.InlineKeyboardButton('Перейти в режим "Произношение"', callback_data='pron_mode'))
        main_menu.add(types.InlineKeyboardButton('Перейти в режим "Свободный Диалог"', callback_data='talk_mode'))
        main_menu.add(types.InlineKeyboardButton('Поменять язык на Русский', callback_data='ru_lang'))
        main_menu.add(types.InlineKeyboardButton('Поменять язык на Английский', callback_data='en_lang'))
    elif cur_lang == 'en':
        main_menu = types.InlineKeyboardMarkup(row_width=5)
        main_menu.add(types.InlineKeyboardButton('Turn on "Grammar" mode', callback_data='grammar_mode'))
        main_menu.add(types.InlineKeyboardButton('Turn on "Pronounciation" mode', callback_data='pron_mode'))
        main_menu.add(types.InlineKeyboardButton('Turn on "Free Talk" mode', callback_data='talk_mode'))
        main_menu.add(types.InlineKeyboardButton('Change language to RU', callback_data='ru_lang'))
        main_menu.add(types.InlineKeyboardButton('Change language to EN', callback_data='en_lang'))
        
