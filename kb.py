from aiogram import types

langMenu = types.InlineKeyboardMarkup(row_width=2)
langMenu.add(types.InlineKeyboardButton('Русский', 'ru_lang'))
langMenu.add(types.InlineKeyboardButton('English', 'en_lang'))
