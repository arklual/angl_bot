import json
import aiofiles
from aiogram import Dispatcher
from aiogram.types import *
from settings import ADMINS_ID
import utils
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import admin_new_mode_form

class ChangeVerboseNameRuForm(StatesGroup):
    verbose_name_ru = State()
    name_before = State()
class ChangeVerboseNameEnForm(StatesGroup):
    verbose_name_en = State()
    name_before = State()
class ChangeNameForm(StatesGroup):
    name = State()
    name_before = State()
class ChangePromptForm(StatesGroup):
    prompt = State()
    name_before = State()
class ChangeMaxTokensForm(StatesGroup):
    max_tokens = State()
    name_before = State()
class ChangeTemperatureForm(StatesGroup):
    temperature = State()
    name_before = State()
class ChangeTopP(StatesGroup):
    top_p = State()
    name_before = State()
class ChangePresencePenalty(StatesGroup):
    presence_penalty = State()
    name_before = State()
class ChangeFrequencyPenalty(StatesGroup):
    frequency_penalty = State()
    name_before = State()
class ChangeVoiceMale(StatesGroup):
    voice_id = State()
    name_before = State()
class ChangeVoiceFemale(StatesGroup):
    voice_id = State()
    name_before = State()
class ChangeWhitelist(StatesGroup):
    whitelist = State()

async def admin(message: Message):
    if str(message.from_user.id) not in ADMINS_ID:
        await message.answer('Вы не админ')
        return
    keyboard = InlineKeyboardMarkup()
    modes = await utils.get_all_modes()
    for mode in modes:
        keyboard.add(InlineKeyboardButton(f'Посмотреть/отредактировать {mode["verbose_name_ru"]}', callback_data=f'admin_mode_{mode["name"]}'))
    keyboard.add(InlineKeyboardButton('Добавить режим', callback_data='admin_add_mode'))
    await message.answer('Что вы хотите сделать?', reply_markup=keyboard)

async def admin_callback(callback: CallbackQuery):
    if str(callback.from_user.id) not in ADMINS_ID:
        await callback.message.answer('Вы не админ')
        return
    keyboard = InlineKeyboardMarkup()
    modes = await utils.get_all_modes()
    for mode in modes:
        keyboard.add(InlineKeyboardButton(f'Посмотреть/отредактировать {mode["verbose_name_ru"]}', callback_data=f'admin_mode_{mode["name"]}'))
    keyboard.add(InlineKeyboardButton('Добавить режим', callback_data='admin_add_mode'))
    await callback.message.answer('Что вы хотите сделать?', reply_markup=keyboard)
    await callback.message.delete()

async def mode_info(callback: CallbackQuery):
    await callback.answer()
    mode = callback.data.split('dmin_mode_')[-1]
    mode = await utils.get_mode(mode)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Изменить whitelist', callback_data='admin_change_whitelist'))
    kb.add(InlineKeyboardButton('Изменить промпт', callback_data=f'admin_change_prompt_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить температуру', callback_data=f'admin_change_temperature_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить max_tokens', callback_data=f'admin_change_max_tokens_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить top_p', callback_data=f'admin_change_top_p_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить presence_penalty', callback_data=f'admin_change_presence_penalty_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить frequency_penalty', callback_data=f'admin_change_frequency_penalty_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить ID мужского голоса', callback_data=f'admin_change_voice_male_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить ID женского голоса', callback_data=f'admin_change_voice_female_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить команду', callback_data=f'admin_change_name_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить название на русском', callback_data=f'admin_change_verbose_name_ru_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Изменить название на английском', callback_data=f'admin_change_verbose_name_en_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Удалить этот режим', callback_data=f'admin_delete_mode_{mode["name"]}'))
    kb.add(InlineKeyboardButton('Назад', callback_data='admin'))
    await callback.message.answer(f'<b>Текущий промпт:</b> {mode["prompt"]}\n\n<b>Текущая температура:</b> {mode["temperature"]}\n<b>Максимальное число токенов:</b> {mode["max_tokens"]}\n\
<b>Top_p:</b> {mode["top_p"]}\n<b>Tresence_penalty:</b> {mode["presence_penalty"]}\n<b>Frequency_penalty:</b> {mode["frequency_penalty"]}\n\
<b>ID женского голоса:</b> {mode["voice_id_female"]}\n<b>ID мужского голоса:</b> {mode["voice_id_male"]}\n<b>Команда:</b> /{mode["name"]}\n\
<b>Название на русском:</b> {mode["verbose_name_ru"]}\n<b>Название на английском:</b> {mode["verbose_name_en"]}', reply_markup=kb)
    await callback.message.delete()

async def change_prompt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_prompt_')[-1])
    await callback.message.answer(f'<b>Текущий промпт:</b> {mode_before["prompt"]}\n\nВведите новый промпт')
    await state.set_state(ChangePromptForm.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_prompt_')[-1])
    await state.set_state(ChangePromptForm.prompt)

async def procces_new_prompt(message: Message, state: FSMContext):
    await state.update_data(prompt=message.text)
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'prompt', data['prompt'])
    await message.answer('Промпт успешно изменён!')

async def change_temperature(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_temperature_')[-1])
    await callback.message.answer(f'<b>Текущая температура:</b> {mode_before["temperature"]}\nВведите новую температуру (десятичные дроби записывать через точку)')
    await state.set_state(ChangeTemperatureForm.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_temperature_')[-1])
    await state.set_state(ChangeTemperatureForm.temperature)

async def procces_new_temperature(message: Message, state: FSMContext):
    await state.update_data(temperature=float(message.text))
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'temperature', data['temperature'])
    await message.answer('Температура успешно изменена!')


async def change_max_tokens(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_max_tokens_')[-1])
    await callback.message.answer(f'<b>max_tokens:</b> {mode_before["max_tokens"]}\nВведите новое значение max_tokens')
    await state.set_state(ChangeMaxTokensForm.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_max_tokens_')[-1])
    await state.set_state(ChangeMaxTokensForm.max_tokens)

async def procces_new_max_tokens(message: Message, state: FSMContext):
    await state.update_data(max_tokens=int(message.text))
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'max_tokens', data['max_tokens'])
    await message.answer('Значение max_tokens успешно изменено!')

async def change_top_p(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_top_p_')[-1])
    await callback.message.answer(f'<b>top_p:</b> {mode_before["top_p"]}\nВведите новое значение top_p (десятичные дроби записывать через точку)')
    await state.set_state(ChangeTopP.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_top_p_')[-1])
    await state.set_state(ChangeTopP.top_p)

async def procces_new_top_p(message: Message, state: FSMContext):
    await state.update_data(top_p=float(message.text))
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'top_p', data['top_p'])
    await message.answer('Значение top_p успешно изменено!')


async def change_presence_penalty(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_presence_penalty_')[-1])
    await callback.message.answer(f'<b>presence_penalty:</b> {mode_before["presence_penalty"]}\nВведите новое значение presence_penalty (десятичные дроби записывать через точку)')
    await state.set_state(ChangePresencePenalty.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_presence_penalty_')[-1])
    await state.set_state(ChangePresencePenalty.presence_penalty)


async def procces_new_presence_penalty(message: Message, state: FSMContext):
    await state.update_data(presence_penalty=float(message.text))
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'presence_penalty', data['presence_penalty'])
    await message.answer('Значение presence_penalty успешно изменено!')

async def change_frequency_penalty(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_frequency_penalty_')[-1])
    await callback.message.answer(f'<b>frequency_penalty:</b> {mode_before["frequency_penalty"]}\nВведите новое значение frequency_penalty (десятичные дроби записывать через точку)')
    await state.set_state(ChangeFrequencyPenalty.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_frequency_penalty_')[-1])
    await state.set_state(ChangeFrequencyPenalty.frequency_penalty)

async def procces_new_frequency_penalty(message: Message, state: FSMContext):
    await state.update_data(frequency_penalty=float(message.text))
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'frequency_penalty', data['frequency_penalty'])
    await message.answer('Значение frequency_penalty успешно изменено!')

async def change_voice_male(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_voice_male_')[-1])
    await callback.message.answer(f'<b>ID мужского голоса:</b> {mode_before["voice_id_male"]}\nВведите ID нового мужского голоса')
    await state.set_state(ChangeVoiceMale.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_voice_male_')[-1])
    await state.set_state(ChangeVoiceMale.voice_id)

async def procces_new_voice_male(message: Message, state: FSMContext):
    await state.update_data(voice_id=int(message.text))
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'voice_id_male', data['voice_id'])
    await message.answer('Мужской голос успешно изменён!')

async def change_voice_female(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_voice_female_')[-1])
    await callback.message.answer(f'<b>ID женского голоса:</b> {mode_before["voice_id_female"]}\nВведите ID нового женского голоса')
    await state.set_state(ChangeVoiceFemale.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_voice_female_')[-1])
    await state.set_state(ChangeVoiceFemale.voice_id)

async def procces_new_voice_female(message: Message, state: FSMContext):
    await state.update_data(voice_id=int(message.text))
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'voice_id_female', data['voice_id'])
    await message.answer('Женский голос успешно изменён!')

async def change_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_name_')[-1])
    await callback.message.answer(f'<b>Команда:</b> {mode_before["name"]}\nВведите новую команду для запуска (в названии не должно быть пробелов, в начале / писать не надо)')
    await state.set_state(ChangeNameForm.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_name_')[-1])
    await state.set_state(ChangeNameForm.name)

async def procces_new_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'name', data['name'])
    await message.answer('Команда для запуска успешна изменена!')

async def change_verbose_name_ru(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_verbose_name_ru_')[-1])
    await callback.message.answer(f'<b>Название на русском:</b> {mode_before["verbose_name_ru"]}\nВведите новое название на русском')
    await state.set_state(ChangeVerboseNameRuForm.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_verbose_name_ru_')[-1])
    await state.set_state(ChangeVerboseNameRuForm.verbose_name_ru)

async def procces_new_verbose_name_ru(message: Message, state: FSMContext):
    await state.update_data(verbose_name_ru=message.text)
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'verbose_name_ru', data['verbose_name_ru'])
    await message.answer('Название на русском успешно изменено!')

async def change_verbose_name_en(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode_before = await utils.get_mode(callback.data.split('dmin_change_verbose_name_en_')[-1])
    await callback.message.answer(f'<b>Название на английском:</b> {mode_before["verbose_name_en"]}\nВведите новое название на английском')
    await state.set_state(ChangeVerboseNameEnForm.name_before)
    await state.update_data(name_before=callback.data.split('dmin_change_verbose_name_en_')[-1])
    await state.set_state(ChangeVerboseNameEnForm.verbose_name_en)

async def procces_new_verbose_name_en(message: Message, state: FSMContext):
    await state.update_data(verbose_name_en=message.text)
    data = await state.get_data()
    await state.finish()
    await utils.update_mode(data['name_before'],'verbose_name_en', data['verbose_name_en'])
    await message.answer('Название на английском успешно изменено!')

async def delete_mode(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mode = callback.data.split('dmin_delete_mode_')[-1]
    await utils.delete_mode(mode)
    await callback.message.answer("Режим удалён")
    await callback.message.delete()

async def change_whitelist(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите новый список telegram_id, каждый с новой строки')
    await state.set_state(ChangeWhitelist.whitelist)

async def process_whitelist(message: Message, state: FSMContext):
    await state.update_data(whitelist=message.text)
    wl = message.text.splitlines()
    await state.finish()
    async with aiofiles.open('whitelist.json', 'w', encoding='utf-8') as fp:
        await fp.write(json.dumps([{
            'id': tid,
        } for tid in wl],ensure_ascii=False))
    await message.answer('Готово!')


async def register_handlers(dp: Dispatcher):
    dp.register_message_handler(procces_new_prompt, state=ChangePromptForm.prompt)
    dp.register_message_handler(procces_new_temperature, state=ChangeTemperatureForm.temperature)
    dp.register_message_handler(procces_new_max_tokens, state=ChangeMaxTokensForm.max_tokens)
    dp.register_message_handler(procces_new_top_p, state=ChangeTopP.top_p)
    dp.register_message_handler(procces_new_presence_penalty, state=ChangePresencePenalty.presence_penalty)
    dp.register_message_handler(procces_new_frequency_penalty, state=ChangeFrequencyPenalty.frequency_penalty)
    dp.register_message_handler(procces_new_voice_male, state=ChangeVoiceMale.voice_id)
    dp.register_message_handler(procces_new_voice_female, state=ChangeVoiceFemale.voice_id)
    dp.register_message_handler(procces_new_name, state=ChangeNameForm.name)
    dp.register_message_handler(procces_new_verbose_name_ru, state=ChangeVerboseNameRuForm.verbose_name_ru)
    dp.register_message_handler(procces_new_verbose_name_en, state=ChangeVerboseNameEnForm.verbose_name_en)
    dp.register_message_handler(process_whitelist, state=ChangeWhitelist.whitelist)
    dp.register_message_handler(admin, commands=['admin'])
    await admin_new_mode_form.register_handlers(dp)

async def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(admin_callback, lambda c: c.data == 'admin')
    dp.register_callback_query_handler(change_whitelist, lambda c: c.data == 'admin_change_whitelist')
    dp.register_callback_query_handler(change_prompt, lambda c: c.data.startswith('admin_change_prompt_'))
    dp.register_callback_query_handler(change_temperature, lambda c: c.data.startswith('admin_change_temperature_'))
    dp.register_callback_query_handler(change_max_tokens, lambda c: c.data.startswith('admin_change_max_tokens_'))
    dp.register_callback_query_handler(change_top_p, lambda c: c.data.startswith('admin_change_top_p_'))
    dp.register_callback_query_handler(change_presence_penalty, lambda c: c.data.startswith('admin_change_presence_penalty_'))
    dp.register_callback_query_handler(change_frequency_penalty, lambda c: c.data.startswith('admin_change_frequency_penalty_'))
    dp.register_callback_query_handler(change_voice_male, lambda c: c.data.startswith('admin_change_voice_male_'))
    dp.register_callback_query_handler(change_voice_female, lambda c: c.data.startswith('admin_change_voice_female_'))
    dp.register_callback_query_handler(change_name, lambda c: c.data.startswith('admin_change_name_'))
    dp.register_callback_query_handler(change_verbose_name_ru, lambda c: c.data.startswith('admin_change_verbose_name_ru_'))
    dp.register_callback_query_handler(change_verbose_name_en, lambda c: c.data.startswith('admin_change_verbose_name_en_'))
    dp.register_callback_query_handler(delete_mode, lambda c: c.data.startswith('admin_delete_mode_'))
    dp.register_callback_query_handler(mode_info, lambda c: c.data.startswith('admin_mode_'))
    await admin_new_mode_form.register_callbacks(dp)