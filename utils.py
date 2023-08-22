import json
import os
import tempfile
import aiofiles
import aiohttp
from urllib.request import urlopen
import openai
from pydub import AudioSegment
from aiogram.types import *
import tiktoken
from aiogram.dispatcher import FSMContext

from settings import OPENAI_TOKEN, CYBERVOICE_TOKEN

openai.api_key = OPENAI_TOKEN


async def change_mode(user_id, mode):
    data = {}
    async with aiofiles.open(f'data/{user_id}.json', 'r',
                             encoding='utf-8') as file:
        data = json.loads(await file.read())
    data['mode'] = mode
    await create_new_context(user_id, data)


async def change_voice_gender(user_id, is_male):
    data = {}
    async with aiofiles.open(f'data/{user_id}.json', 'r',
                             encoding='utf-8') as file:
        data = json.loads(await file.read())
    data['is_male_voice'] = is_male
    await create_new_context(user_id, data)


async def has_cursed_word(text):
    words = text.split(' ')
    cursed_words = []
    async with aiofiles.open('stop_words.txt', 'r', encoding='utf-8') as fp:
        cursed_words = (await fp.read()).split(',')
    for word in words:
        if word in cursed_words:
            return True
    return False


async def text_to_speech_send(bot, chat_id, text, reply_markup=None):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": CYBERVOICE_TOKEN
    }
    context = await get_context(chat_id)
    if context['is_male_voice']:
        voice_id = (await get_mode(context['mode']))['voice_id_male']
    else:
        voice_id = (await get_mode(context['mode']))['voice_id_female']
    body = {'voice_id': voice_id, 'text': text, 'format': 'mp3'}

    url = "https://api.voice.steos.io/v1/get/tts"
    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                headers=headers,
                                data=json.dumps(
                                    body, ensure_ascii=False)) as response:
            data = await response.json()
            data = urlopen(data['audio_url']).read()
            f = tempfile.NamedTemporaryFile(delete=False)
            f.write(data)
            AudioSegment.from_mp3(f.name).export(
                f'answers/result{chat_id}.ogg', format='ogg')
            f.close()
            with open(f'answers/result{chat_id}.ogg', 'rb') as fp:
                if reply_markup:
                    await bot.send_voice(chat_id,
                                         fp,
                                         reply_markup=reply_markup)
                else:
                    await bot.send_voice(chat_id, fp)
            os.remove(f'answers/result{chat_id}.ogg')


async def get_voices():
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": CYBERVOICE_TOKEN
    }

    url = "https://api.voice.steos.io/v1/get/voices"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data['voices']


async def is_context_exist(chat_id):
    files = os.listdir(path='data')
    for file in files:
        if str(chat_id) + '.json' == file:
            return True
    return False


async def append_messages(chat_id, messages):
    data = []
    async with aiofiles.open('data/' + str(chat_id) + '.json',
                             'r',
                             encoding='utf-8') as fp:
        data = json.loads(await fp.read())
    data['messages'] += messages
    await create_new_context(chat_id=chat_id, context=data)


async def get_context(chat_id):
    async with aiofiles.open('data/' + str(chat_id) + '.json',
                             'r',
                             encoding='utf-8') as fp:
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
        mode: '...',
        is_male_voice: true,
    }
    '''
    async with aiofiles.open('data/' + str(chat_id) + '.json',
                             'w',
                             encoding='utf-8') as fp:
        await fp.write(json.dumps(context, ensure_ascii=False))


async def request_to_gpt(user_id, text):
    data = []
    if await is_context_exist(user_id):
        context = await get_context(user_id)
    else:
        return "Вы ещё не начали диалог"
    mode = context['mode']
    data_in_str = ''
    mode_info = await get_mode(mode)
    prompt = mode_info['prompt']
    data_in_str += prompt
    data.append({"role": "system", "content": prompt})
    for m in context['messages']:
        data.append({"role": m['from'], "content": m['message']})
        data_in_str += m['message']
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(data_in_str))
    if num_tokens >= 3900:
        data[0] = {"role": "system", "content": 'summarize all this dialog'}
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=data,
        )
        response = completion['choices'][0]['message']['content']
        context = await get_context(user_id)
        num_tokens = len(encoding.encode(response))
        context = {
            'messages': [{
                "role": 'user',
                "content": response
            }],
            'mode': mode,
            'is_male_voice': context['is_male_voice']
        }
        await create_new_context(user_id, context)
        data.append({"role": "system", "content": prompt})
        num_tokens += len(encoding.encode(prompt))
        for m in context['messages']:
            data.append({"role": m['from'], "content": m['message']})
            num_tokens += len(encoding.encode(m['message']))
    data.append({"role": "user", "content": text})
    await append_messages(user_id, [{'from': 'user', "message": text}])
    temp = mode_info['temperature']
    tokens = mode_info['max_tokens']
    top_p = mode_info['top_p']
    presence_penalty = mode_info['presence_penalty']
    frequency_penalty = mode_info['frequency_penalty']
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=data,
        max_tokens=tokens,
        temperature=temp,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty)
    response = completion['choices'][0]['message']['content']
    await append_messages(user_id, [{
        "from": "assistant",
        "message": response
    }])
    return response


async def get_all_modes_name():
    names = []
    async with aiofiles.open('modes.json', 'r', encoding='utf-8') as fp:
        data = json.loads(await fp.read())
        for i in data:
            names.append(i['name'])
    return names


async def get_all_modes():
    data = []
    async with aiofiles.open('modes.json', 'r', encoding='utf-8') as fp:
        data = json.loads(await fp.read())
    return data


async def get_mode(mode):
    async with aiofiles.open('modes.json', 'r', encoding='utf-8') as fp:
        data = json.loads(await fp.read())
        for i in data:
            if i['name'] == mode:
                return i


async def delete_mode(mode):
    data = []
    async with aiofiles.open('modes.json', 'r', encoding='utf-8') as fp:
        data = json.loads(await fp.read())
        for m in data:
            if m['name'] == mode:
                data.remove(m)
                break
    async with aiofiles.open("modes.json", "w", encoding='utf-8') as fp:
        await fp.write(json.dumps(data, ensure_ascii=False))


async def update_mode(mode, param, value):
    data = []
    async with aiofiles.open('modes.json', 'r', encoding='utf-8') as fp:
        data = json.loads(await fp.read())
        for i, m in enumerate(data):
            if m['name'] == mode:
                data[i][param] = value
                break
    async with aiofiles.open("modes.json", "w", encoding='utf-8') as fp:
        await fp.write(json.dumps(data, ensure_ascii=False))


async def add_mode(verbose_name_ru: str, verbose_name_en: str, name: str,
                   voice_id_female: int, voice_id_male: int, prompt: str,
                   temperature: float, max_tokens: int, top_p: float,
                   presence_penalty: float, frequency_penalty: float):
    data = []
    async with aiofiles.open('modes.json', 'r', encoding='utf-8') as fp:
        data = json.loads(await fp.read())
    data.append({
        "name": name,
        "verbose_name_ru": verbose_name_ru,
        "verbose_name_en": verbose_name_en,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
        "voice_id_female": voice_id_female,
        "voice_id_male": voice_id_male,
    })
    async with aiofiles.open("modes.json", "w", encoding='utf-8') as fp:
        await fp.write(json.dumps(data, ensure_ascii=False))


# LANGUAGE THINGS
def load_user_languages():
    try:
        with open("user_languages.json", "r") as f:
            user_languages = json.load(f)
    except FileNotFoundError:
        user_languages = {}
    return user_languages


# Сохраняем настройки в файл user_languages.json
def save_user_languages(user_languages):
    with open("user_languages.json", "w") as f:
        json.dump(user_languages, f)


# Получение текущего языка для пользователя
def get_user_language(chat_id):
    user_languages = load_user_languages()
    return user_languages.get(str(chat_id),
                              "en")  # Возвращаем "en" если язык не задан


# Изменение языка для пользователя
def set_user_language(chat_id, new_lang):
    user_languages = load_user_languages()
    user_languages[str(chat_id)] = new_lang
    save_user_languages(user_languages)


#___________________________________________
