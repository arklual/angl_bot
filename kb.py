from aiogram import types

langMenu = types.InlineKeyboardMarkup(row_width=2)
langMenu.add(types.InlineKeyboardButton('Русский', callback_data='ru_lang'))
langMenu.add(types.InlineKeyboardButton('English', callback_data='en_lang'))
