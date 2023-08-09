import random
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from aiogram.types import *
from kb import menu_keyboard
import utils
from strings import *
import aiofiles
import json



async def add_user(data, user_id, referer_id=None):
    new_entry = {"user_id": user_id, "referer_id": referer_id}
    data.append(new_entry)
    async with aiofiles.open('referals.json', mode="w", encoding='utf-8') as file:
        await file.write(json.dumps(data, indent=4, ensure_ascii=False))
  

async def start(message: Message):
    data = []
    async with aiofiles.open('referals.json', mode="r", encoding='utf-8') as file:
        data = json.loads(await file.read())
    user_id = message.from_user.id
    user_exists = any(entry["user_id"] == user_id for entry in data)
    if not user_exists:
      start_command = message.text
      referer_id = start_command[7:]
      if referer_id:
        referer_id = int(referer_id)
        if referer_id != user_id:
          await add_user(data, user_id, referer_id)
          await message.bot.send_message(int(referer_id), 'По вашей ссылке зарегистрировался новый пользователь')
        else:
          await add_user(data, user_id, None)
          await message.answer("Нельзя регистрироваться по своей реферальной ссылке")
      else:
        await add_user(data, user_id, None)

    context = {
        'messages':[],
        'mode': 'grammar',
        'is_male_voice': True,
    }
    lang = utils.get_user_language(message.from_user.id)
    
    # Отправляем приветственное сообщение на текущем языке
    if lang == "en":
      async with aiofiles.open("./images/start_en.jpg", 'rb') as fp:
        await message.bot.send_photo(message.from_user.id, await fp.read(), caption=START_MESSAGES_EN[random.randint(0, 
len(START_MESSAGES_EN)-1)], reply_markup=await menu_keyboard('en'))
    elif lang == "ru":
        async with aiofiles.open("./images/start_ru.jpg", 'rb') as fp:
            await message.bot.send_photo(message.from_user.id, await fp.read(), caption=START_MESSAGES_RU[random.randint(0, len(START_MESSAGES_RU)-1)], reply_markup=await menu_keyboard('ru'))
    await utils.create_new_context(message.from_user.id, context)

async def reset(message: Message):
    context = await utils.get_context(message.from_user.id) 
    await utils.create_new_context(message.from_user.id, {'messages': [], 'mode': 'grammar', 'is_male_voice': context['is_male_voice'],})
    lang = utils.get_user_language(message.from_user.id)

    # Отправляем приветственное сообщение на текущем языке
    if lang == "en":
        await message.answer("You have started a new session")
    elif lang == "ru":
        await message.answer("Вы начали новую сессию")

async def help(message: Message):
    lang = utils.get_user_language(message.from_user.id)
    if lang == "en":
        async with aiofiles.open("./images/helper_icon_en.jpg", 'rb') as fp:
            await message.bot.send_photo(message.from_user.id, await fp.read(), caption=HELP_MESSAGE_EN)
    elif lang == "ru":
        async with aiofiles.open("./images/helper_icon.jpg", 'rb') as fp:
            await message.bot.send_photo(message.from_user.id, await fp.read(), caption=HELP_MESSAGE_RU)

async def menu(message: Message):
    lang = utils.get_user_language(message.from_user.id)
    if lang == "en":
        async with aiofiles.open("./images/helper_icon_en.jpg", 'rb') as fp:
            await message.bot.send_photo(message.from_user.id, await fp.read(), caption="Main Menu\n Here you change modes and language", reply_markup=await menu_keyboard('en'))
    elif lang == "ru":
        async with aiofiles.open("./images/helper_icon.jpg", 'rb') as fp:
            await message.bot.send_photo(message.from_user.id, await fp.read(), "Главное меню", reply_markup=await menu_keyboard('ru'))

async def help_callback(callback:CallbackQuery):
    await callback.answer()
    lang = utils.get_user_language(callback.from_user.id)
    if lang == "en":
        async with aiofiles.open("./images/helper_icon_en.jpg", 'rb') as fp:
            await callback.bot.send_photo(callback.from_user.id, await fp.read(), caption=HELP_MESSAGE_EN)
    elif lang == "ru":
        async with aiofiles.open("./images/helper_icon.jpg", 'rb') as fp:
            await callback.bot.send_photo(callback.from_user.id, await fp.read(), caption=HELP_MESSAGE_RU)
    
async def tutorial(message:Message):
  lang = utils.get_user_language(message.from_user.id)
  if lang == "en":
    await message.answer('Tutorial')
  elif lang == "ru":
    await message.answer('Туториал')

async def tutorial_callback(callback: CallbackQuery):
  await callback.answer()
  lang = utils.get_user_language(callback.from_user.id)
  if lang == "en":
    await callback.message.answer('Tutorial')
  elif lang == "ru":
    await callback.message.answer('Туториал')
  

async def ru_lang(callback_query: CallbackQuery):
    utils.set_user_language(callback_query.from_user.id, 'ru')
    await callback_query.answer("Ваш язык теперь русский")
    await callback_query.message.answer("Главное меню", reply_markup=await menu_keyboard('ru'))
    await callback_query.message.delete()

async def en_lang(callback_query: CallbackQuery):
    utils.set_user_language(callback_query.from_user.id, 'en')
    await callback_query.answer("Your lang have been changed to English")
    await callback_query.message.answer("Main Menu\nHere you change modes and language", reply_markup=await menu_keyboard('en'))
    await callback_query.message.delete()

async def voice(message: Message):
    lang = utils.get_user_language(message.from_user.id)
    if lang == "en":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton('Male', callback_data='male_voice'))
        kb.add(InlineKeyboardButton('Female', callback_data='female_voice'))
        await message.answer("Choose gender of voice", reply_markup=kb)
    elif lang == "ru":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton('Мужской', callback_data='male_voice'))
        kb.add(InlineKeyboardButton('Женский', callback_data='female_voice'))
        await message.answer("Выберите пол голоса", reply_markup=kb)

async def voice_callback(callback: CallbackQuery):
    await callback.answer()
    lang = utils.get_user_language(callback.from_user.id)
    if lang == "en":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton('Male', callback_data='male_voice'))
        kb.add(InlineKeyboardButton('Female', callback_data='female_voice'))
        await callback.message.answer("Choose gender of voice", reply_markup=kb)
    elif lang == "ru":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton('Мужской', callback_data='male_voice'))
        kb.add(InlineKeyboardButton('Женский', callback_data='female_voice'))
        await callback.message.answer("Выберите пол голоса", reply_markup=kb)

async def male_voice(callback: CallbackQuery):
    lang = utils.get_user_language(callback.from_user.id)
    if lang == "en":
        await callback.answer('Now the gender of voice is male')
    if lang == "ru":
        await callback.answer('Сейчас пол голоса мужской')
    await utils.change_voice_gender(callback.from_user.id, True)

async def female_voice(callback: CallbackQuery):
    lang = utils.get_user_language(callback.from_user.id)
    if lang == "en":
        await callback.answer('Now the gender of voice is female')
    if lang == "ru":
        await callback.answer('Сейчас пол голоса женский')
    await utils.change_voice_gender(callback.from_user.id, False)



async def change_mode(message: Message):
    names = await utils.get_all_modes_name()
    mode = message.text.strip('/')
    if mode not in names:
        lang = utils.get_user_language(message.from_user.id)
        if lang == "en":
            await message.answer('This command doesn\'t exist')
        if lang == "ru":
            await message.answer('Такой команды нет')
        return
    lang = utils.get_user_language(message.from_user.id)
    mode = await utils.get_mode(mode)
    if lang == "en":
        await message.answer(f'Now the mode of dialog is "{mode["verbose_name_en"]}"')
    elif lang == "ru":
        await message.answer(f'Включен режим "{mode["verbose_name_ru"]}"')
    await utils.change_mode(message.from_user.id, mode['name'])

async def change_mode_callback(callback: CallbackQuery):
    await callback.answer()
    mode = callback.data.split('hange_mode_')[-1]
    lang = utils.get_user_language(callback.from_user.id)
    mode = await utils.get_mode(mode)
    if lang == "en":
        await callback.message.answer(f'Now the mode of dialog is "{mode["verbose_name_en"]}"')
    elif lang == "ru":
        await callback.message.answer(f'Включен режим "{mode["verbose_name_ru"]}"')
    await utils.change_mode(callback.from_user.id, mode['name'])

async def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(reset, commands=['reset'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(menu, commands=['menu'])
    dp.register_message_handler(tutorial, commands=['tutorial'])
    dp.register_message_handler(voice, commands=['voice'])
    dp.register_message_handler(change_mode, lambda m: m.text.startswith('/') and not m.reply_to_message)
    

async def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(ru_lang, lambda callback_query: callback_query.data == 'ru_lang')
    dp.register_callback_query_handler(en_lang, lambda callback_query: callback_query.data == 'en_lang')
    dp.register_callback_query_handler(help_callback, lambda callback: callback.data == 'help')
    dp.register_callback_query_handler(tutorial_callback, lambda callback: callback.data == 'tutorial')
    dp.register_callback_query_handler(voice_callback, lambda callback:  callback.data == 'voice')
    dp.register_callback_query_handler(change_mode_callback, lambda callback:  callback.data.startswith("change_mode_"))
    dp.register_callback_query_handler(female_voice, lambda callback_query: callback_query.data == 'female_voice')
    dp.register_callback_query_handler(male_voice, lambda callback_query: callback_query.data == 'male_voice')
