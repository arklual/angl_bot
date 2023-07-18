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
import os
import json
import random
import openai

openai.api_key = OPEAI_TOKEN

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

async def has_cursed_word(text):
    words = text.split(' ')
    cursed_words = []
    async with aiofiles.open('stop_words.txt', 'r') as fp:
        cursed_words = (await fp.read()).split()
    for word in words:
        if word in cursed_words:
            return True
    return False

async def text_to_speech_send(chat_id, text):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               "Authorization": CYBERVOICE_TOKEN}

    body = {'voice_id': 1,
            'text': text,
            'format': 'mp3'}

    url = "https://api.voice.steos.io/v1/get/tts"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(body)) as response:
            data = await response.json()
            await bot.send_voice(chat_id, data['audio_url'])

async def is_context_exist(chat_id):
    files = os.listdir()
    for file in files:
        if 'data/'+str(chat_id)+'.json' == file:
            return True
    return False

async def append_messages(chat_id, messages):
    data = []
    async with aiofiles.open('data/'+str(chat_id)+'.json', 'r') as fp:
        data = json.loads(await fp.read())
    data['messages'] += messages
    await create_new_context(chat_id=chat_id, context=data)

async def get_context(chat_id):
    async with aiofiles.open('data/'+str(chat_id)+'.json', 'r') as fp:
        data = json.loads(await fp.read())
        return data

async def create_new_context(chat_id, context):
    '''
    FORMAT:
    {
        messages: [
            {
                "from": "user",
                "message": "..."
            },
            {
                "from": "assistant",
                "message": "..."
            }
        ],
        mode: '...'
    }
    '''
    async with aiofiles.open('data/'+str(chat_id)+'.json', 'w') as fp:
        await fp.write(json.dumps(context))
    
async def get_prompt(mode):
    async with aiofiles.open('prompt_'+mode+'.txt', 'r') as fp:
        return await fp.read()
###################ADMIN MENU######################################

class PromtFreeForm(StatesGroup):
    prompt = State()
class PromtPronForm(StatesGroup):
    prompt = State()
class PromtGramForm(StatesGroup):
    prompt = State()

@dp.message_handler(commands=['admin'])
async def admin(message: Message):
    if str(message.from_user.id) not in ADMINS_ID:
        await message.answer('Вы не админ')
        return
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Изменить промпт свободного диалога', callback_data='change_prompt_free'))
    keyboard.add(InlineKeyboardButton('Изменить промпт произношения', callback_data='change_prompt_pron'))
    keyboard.add(InlineKeyboardButton('Изменить промпт грамматики', callback_data='change_prompt_gram'))
    await message.answer('Что вы хотите сделать?', reply_markup=keyboard)

@dp.callback_query_handler(text='change_prompt_free')
async def change_prompt_free(callback: CallbackQuery):
    if str(callback.from_user.id) not in ADMINS_ID:
        await callback.message.answer('Только админ может менять промпт')
        return
    await callback.message.answer('Отправьте новый промпт')
    await PromtFreeForm.prompt.set()

@dp.message_handler(state=PromtFreeForm.prompt)
async def process_new_prompt_free(message: Message, state: FSMContext):
    prompt = message.text
    await state.finish()
    async with aiofiles.open('prompt_free.txt', 'w') as fp:
        await fp.write(prompt)
    await message.answer('Промпт успешно обновлён!')

@dp.callback_query_handler(text='change_prompt_gram')
async def change_prompt_gram(callback: CallbackQuery):
    if str(callback.from_user.id) not in ADMINS_ID:
        await callback.message.answer('Только админ может менять промпт')
        return
    await callback.message.answer('Отправьте новый промпт')
    await PromtGramForm.prompt.set()

@dp.message_handler(state=PromtGramForm.prompt)
async def process_new_prompt_gram(message: Message, state: FSMContext):
    prompt = message.text
    await state.finish()
    async with aiofiles.open('prompt_grammar.txt', 'w') as fp:
        await fp.write(prompt)
    await message.answer('Промпт успешно обновлён!')

@dp.callback_query_handler(text='change_prompt_pron')
async def change_prompt_pron(callback: CallbackQuery):
    if str(callback.from_user.id) not in ADMINS_ID:
        await callback.message.answer('Только админ может менять промпт')
        return
    await callback.message.answer('Отправьте новый промпт')
    await PromtPronForm.prompt.set()

@dp.message_handler(state=PromtPronForm.prompt)
async def process_new_prompt_free(message: Message, state: FSMContext):
    prompt = message.text
    await state.finish()
    async with aiofiles.open('prompt_pronoun.txt', 'w') as fp:
        await fp.write(prompt)
    await message.answer('Промпт успешно обновлён!')

####################HANDLIG DIALOG#####################################
@dp.message_handler()
async def handle_all_messages(message: Message):
    if await has_cursed_word(message.text):
        await message.answer('Прошу вести корректный диалог или Попробуйте сформулировать ответ без использования запрещенных слов, мы не поддерживаем беседы на данную тему\n\n-----\n\nI ask you to conduct a correct dialogue or try to formulate an answer without using forbidden words. We do not support conversations on this topic')
        return
    data = []
    user_id = message.from_user.id
    if await is_context_exist(user_id):
        context = await get_context(user_id)
    else:
        context = {
            'messages':[],
            'mode': 'grammar'
        }
        await create_new_context(message.from_user.id, context)
    mode = context['mode']
    data.append({"role": "system", "content": await get_prompt(mode)})
    for m in context['messages']:
        data.append({"role": m['from'], "content": m['message']})
    data.append({"role": "user", "content": message.text})
    await append_messages(user_id, [{'from': 'user', "message": message.text}])
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=data
    )
    response = completion['choices'][0]['message']['content']
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)
    await append_messages(user_id, [{"from": "assistant", "message": response}])



executor.start_polling(dp)