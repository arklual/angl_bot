from aiogram import types
from utils import get_all_modes

async def menu_keyboard(cur_lang):
    modes = await get_all_modes()
    if cur_lang == 'ru': 
        main_menu = types.InlineKeyboardMarkup(row_width=5)
        for mode in modes:
            main_menu.add(types.InlineKeyboardButton(f'Перейти в режим "{mode["verbose_name_ru"]}"', callback_data=f'change_mode_{mode["name"]}'))
        main_menu.add(types.InlineKeyboardButton('Купить подписку', callback_data='subscribe'))
        main_menu.add(types.InlineKeyboardButton('Поменять язык на Русский', callback_data='ru_lang'))
        main_menu.add(types.InlineKeyboardButton('Поменять язык на Английский', callback_data='en_lang'))
        return main_menu
    elif cur_lang == 'en':
        main_menu = types.InlineKeyboardMarkup(row_width=5)
        for mode in modes:
            main_menu.add(types.InlineKeyboardButton(f'Turn on "{mode["verbose_name_ru"]}" mode', callback_data=f'change_mode_{mode["name"]}'))
        main_menu.add(types.InlineKeyboardButton('Subscribe', callback_data='subscribe'))
        main_menu.add(types.InlineKeyboardButton('Change language to RU', callback_data='ru_lang'))
        main_menu.add(types.InlineKeyboardButton('Change language to EN', callback_data='en_lang'))
        return main_menu
        
