from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import *
from settings import ADMINS_ID
import aiofiles
import utils

class NewModeForm(StatesGroup):
    verbose_name_ru = State()
    verbose_name_en = State()
    name = State()
    prompt = State()
    temperature = State()
    max_tokens = State()
    top_p = State()
    presence_penalty = State()
    frequency_penalty = State()
    voice_id_female = State()
    voice_id_male = State()

async def admin(message: Message):
    if str(message.from_user.id) not in ADMINS_ID:
        await message.answer('Вы не админ')
        return
    keyboard = InlineKeyboardMarkup()
    modes = await utils.get_all_modes()
    for mode in modes:
        keyboard.add(InlineKeyboardButton(f'Посмотреть/отредактировать {mode["verbose_name"]}', callback_data=f'admin_mode_{mode["verbose_name"]}'))
    keyboard.add(InlineKeyboardButton('Добавить режим', callback_data='admin_add_mode'))
    await message.answer('Что вы хотите сделать?', reply_markup=keyboard)

async def add_mode(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите название режима на русском')
    await state.set_state(NewModeForm.verbose_name_ru)

async def procces_verbose_name_ru(message: Message, state: FSMContext):
    await state.update_data(verbose_name_ru=message.text)
    await message.answer('Введите название режима на английском')
    await state.set_state(NewModeForm.verbose_name_en)

async def procces_verbose_name_en(message: Message, state: FSMContext):
    await state.update_data(verbose_name_en=message.text)
    await message.answer('Введите команду для запуска (без / и без пробела). Пример правильного ввода:\ngrammar')
    await state.set_state(NewModeForm.name)

async def procces_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите промпт')
    await state.set_state(NewModeForm.prompt)

async def procces_prompt(message: Message, state: FSMContext):
    await state.update_data(prompt=message.text)
    await message.answer('Введите температуру (Внимание: здесь и далее дробные значения записывать через точку, а не запятую)')
    await state.set_state(NewModeForm.temperature)

async def procces_temperature(message: Message, state: FSMContext):
    await state.update_data(temperature=message.text)
    await message.answer('Введите максимальное число токенов')
    await state.set_state(NewModeForm.max_tokens)

async def procces_max_tokens(message: Message, state: FSMContext):
    await state.update_data(max_tokens=message.text)
    await message.answer('Введите значение параметра top_p')
    await state.set_state(NewModeForm.top_p)

async def procces_top_p(message: Message, state: FSMContext):
    await state.update_data(top_p=message.text)
    await message.answer('Введите значение параметра presence_penalty')
    await state.set_state(NewModeForm.presence_penalty)

async def procces_presence_penalty(message: Message, state: FSMContext):
    await state.update_data(presence_penalty=message.text)
    await message.answer('Введите значение параметра frequency_penalty')
    await state.set_state(NewModeForm.frequency_penalty)

async def procces_frequency_penalty(message: Message, state: FSMContext):
    await state.update_data(frequency_penalty=message.text)
    await message.answer('Введите id женского голоса для этого режима')
    await state.set_state(NewModeForm.voice_id_female)

async def procces_voice_id_female(message: Message, state: FSMContext):
    await state.update_data(voice_id_female=message.text)
    await message.answer('Введите id мужского голоса для этого режима')
    await state.set_state(NewModeForm.voice_id_male)

async def procces_voice_id_male(message: Message, state: FSMContext):
    await state.update_data(voice_id_male=message.text)
    data = await state.get_data()
    await utils.add_mode(**data)
    await state.finish()
    await message.answer('Режим успешно добавлен!')

async def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_message_handler(procces_verbose_name_ru, state=NewModeForm.verbose_name_ru)
    dp.register_message_handler(procces_verbose_name_en, state=NewModeForm.verbose_name_en)
    dp.register_message_handler(procces_name, state=NewModeForm.name)
    dp.register_message_handler(procces_prompt, state=NewModeForm.prompt)
    dp.register_message_handler(procces_temperature, state=NewModeForm.temperature)
    dp.register_message_handler(procces_max_tokens, state=NewModeForm.max_tokens)
    dp.register_message_handler(procces_top_p, state=NewModeForm.top_p)
    dp.register_message_handler(procces_presence_penalty, state=NewModeForm.presence_penalty)
    dp.register_message_handler(procces_frequency_penalty, state=NewModeForm.frequency_penalty)
    dp.register_message_handler(procces_voice_id_female, state=NewModeForm.voice_id_female)
    dp.register_message_handler(procces_voice_id_male, state=NewModeForm.voice_id_male)


async def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(add_mode, lambda callback:  callback.data =='admin_add_mode')