from aiogram import types
from utils import get_all_modes


async def menu_keyboard(cur_lang):
    modes = await get_all_modes()
    if cur_lang == 'ru':
        main_menu = types.InlineKeyboardMarkup(row_width=5)
        main_menu.add(
            types.InlineKeyboardButton('Меню пользователя',
                                       callback_data='user_profile'))
        main_menu.add(
            types.InlineKeyboardButton('Помощь', callback_data='help'))
        main_menu.add(
            types.InlineKeyboardButton('Как пользоваться',
                                       callback_data='tutorial'))
        for mode in modes:
            main_menu.add(
                types.InlineKeyboardButton(
                    f'Перейти в режим "{mode["verbose_name_ru"]}"',
                    callback_data=f'change_mode_{mode["name"]}'))
        main_menu.add(
            types.InlineKeyboardButton('Сменить голос', callback_data='voice'))
        main_menu.add(
            types.InlineKeyboardButton('Поменять язык на Русский',
                                       callback_data='ru_lang'))
        main_menu.add(
            types.InlineKeyboardButton('Поменять язык на Английский',
                                       callback_data='en_lang'))
        return main_menu
    elif cur_lang == 'en':
        main_menu = types.InlineKeyboardMarkup(row_width=5)
        main_menu.add(
            types.InlineKeyboardButton('User menu',
                                       callback_data='user_profile'))
        main_menu.add(types.InlineKeyboardButton('Help', callback_data='help'))
        main_menu.add(
            types.InlineKeyboardButton('Tutorial', callback_data='tutorial'))
        for mode in modes:
            main_menu.add(
                types.InlineKeyboardButton(
                    f'Turn on "{mode["verbose_name_en"]}" mode',
                    callback_data=f'change_mode_{mode["name"]}'))
        main_menu.add(
            types.InlineKeyboardButton('Change voice', callback_data='voice'))
        main_menu.add(
            types.InlineKeyboardButton('Change language to RU',
                                       callback_data='ru_lang'))
        main_menu.add(
            types.InlineKeyboardButton('Change language to EN',
                                       callback_data='en_lang'))
        return main_menu


def profile_kb_if_subed(cur_lang, user_id):
    kb = types.InlineKeyboardMarkup()
    if cur_lang == 'ru':
        kb.add(
            types.InlineKeyboardButton(
                'Поделиться реф. ссылкой',
                url=
                f'https://t.me/share/url?url=t.me/SkillbuddyBot?start={user_id}&text=SkillBuddy'
            ))
    elif cur_lang == "en":
        kb.add(
            types.InlineKeyboardButton(
                'Share referal link',
                url=f'https://t.me/share/url?url=t.me/SkillbuddyBot?start={user_id}&text=SkillBuddy'
            ))
    return kb


def profile_kb_if_unsubed(cur_lang):
    kb = types.InlineKeyboardMarkup()
    if cur_lang == 'ru':
        kb.add(
            types.InlineKeyboardButton('Купить подписку', callback_data="subscribe"))
    elif cur_lang == "en":
        kb.add(types.InlineKeyboardButton('Subscribe', callback_data="subscribe"))
    return kb
