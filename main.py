import aiogram
from aiogram.utils import executor
from aiogram.types import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import *
from strings import *
import aiofiles
import aiohttp
import json
import random


bot = aiogram.Bot(TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)


#############TEST###########

@dp.message_handler(commands=['test'])
async def test(message: Message):
    await text_to_speech_send(message.from_user.id, 'This is test audio message!')

#####BASIC HANDLERS###############

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(START_MESSAGES[random.randint(0, len(START_MESSAGES)-1)])

@dp.message_handler(commands=['stop'])
async def stop(message: Message):
    pass

@dp.message_handler(commands=['reset'])
async def reset(message: Message):
    pass

@dp.message_handler(commands=['help'])
async def help(message: Message):
    pass

@dp.message_handler(commands=['menu'])
async def menu(message: Message):
    pass

@dp.message_handler(commands=['voice'])
async def voice(message: Message):
    pass

@dp.message_handler(commands=['grammar'])
async def grammar(message: Message):
    pass

@dp.message_handler(commands=['pronunciation'])
async def pronunciation(message: Message):
    pass

@dp.message_handler(commands=['talk'])
async def talk(message: Message):
    pass

###################TOOLS###########################################


async def text_to_speech_send(chat_id, text):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               "Authorization": CYBERVOICE_TOKEN}

    body = {'voice_id': 1,
            'text': text,
            'format': 'mp3'}

    url = "https://api.voice.steos.io/v1/get/tts"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(body)) as response:
            print(await response.text())
            data = await response.json()
            await bot.send_voice(chat_id, data['audio_url'])


###################ADMIN MENU######################################

class PromtForm(StatesGroup):
    prompt = State()

@dp.message_handler(commands=['admin'])
async def admin(message: Message):
    if str(message.from_user.id) not in ADMINS_ID:
        await message.answer('Вы не админ')
        return
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Изменить промпт', callback_data='change_prompt'))
    await message.answer('Что вы хотите сделать?', reply_markup=keyboard)

@dp.callback_query_handler(text='change_prompt')
async def change_prompt(callback: CallbackQuery):
    if str(callback.from_user.id) not in ADMINS_ID:
        await callback.message.answer('Только админ может менять промпт')
        return
    await callback.message.answer('Отправьте новый промпт')
    await PromtForm.prompt.set()

@dp.message_handler(state=PromtForm.prompt)
async def process_new_prompt(message: Message, state: FSMContext):
    prompt = message.text
    await state.finish()
    async with aiofiles.open('prompt.txt', 'w') as fp:
        await fp.write(prompt)
    await message.answer('Промпт успешно обновлён!')


executor.start_polling(dp)