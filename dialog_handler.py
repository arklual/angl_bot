import traceback
from aiogram import Dispatcher
from utils import *
from strings import *
import langid
import speech_recognition as sr 


async def voice_handler(message: Message):
    file_id = message.voice.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path 
    await message.bot.download_file(file_path, f"voices/voice{message.from_user.id}.oga")

    # Используйте ffmpeg для конвертации аудио из формата .oga в .wav
    os.system(f'ffmpeg -i voices/voice{message.from_user.id}.oga voices/voice{message.from_user.id}.wav')

    # Загрузите аудиофайл и преобразуйте речь в текст
    r = sr.Recognizer()
    with sr.AudioFile(f'voices/voice{message.from_user.id}.wav') as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language='eng')
            if await has_cursed_word(text):
                await text_to_speech_send(message.bot, message.chat.id, "Прошу вести корректный диалог или Попробуйте сформулировать ответ без использования запрещенных слов, мы не поддерживаем беседы на данную тему\n\n-----\n\nI ask you to conduct a correct dialogue or try to formulate an answer without using forbidden words. We do not support conversations on this topic")
                return
            lang = list(langid.classify(text))[0]
            if  lang != 'ru' and lang != 'en':
                await text_to_speech_send(message.bot, message.chat.id, "Hey there! Looks like we speak different languages. Let's go back to English.")
                return
            response = await request_to_gpt(message.from_user.id, text)
            await text_to_speech_send(message.bot, message.chat.id, response)
        except Exception as e:
            traceback.print_exc()
            text = "Sorry, I did not get that"
            await message.answer(text)
        finally:
            os.system(f'rm voices/voice{message.from_user.id}.oga')
            os.system(f'rm voices/voice{message.from_user.id}.wav')

async def handle_all_messages(message: Message):
    if await has_cursed_word(message.text):
        await message.answer('Прошу вести корректный диалог или Попробуйте сформулировать ответ без использования запрещенных слов, мы не поддерживаем беседы на данную тему\n\n-----\n\nI ask you to conduct a correct dialogue or try to formulate an answer without using forbidden words. We do not support conversations on this topic')
        return
    if message.reply_to_message and message.reply_to_message.text:
        if '/' in message.text:
            mode = message.text.replace('/', '')
            cur_mode = (await get_context(message.from_user.id))['mode']
            await change_mode(message.from_user.id, mode)
            response = await request_to_gpt(message.from_user.id, message.reply_to_message.text)
            await message.answer(response)
            await change_mode(message.from_user.id, cur_mode)
            return
    elif message.reply_to_message and message.reply_to_message.voice:
        if '/' in message.text:
            mode = message.text.replace('/', '')
            cur_mode = (await get_context(message.from_user.id))['mode']
            await change_mode(message.from_user.id, mode)
            file_id = message.voice.file_id
            file_info = await message.bot.get_file(file_id)
            file_path = file_info.file_path 
            await message.bot.download_file(file_path, f"voices/voice{message.from_user.id}.oga")

            # Используйте ffmpeg для конвертации аудио из формата .oga в .wav
            os.system(f'ffmpeg -i voices/voice{message.from_user.id}.oga voices/voice{message.from_user.id}.wav')

            # Загрузите аудиофайл и преобразуйте речь в текст
            r = sr.Recognizer()
            with sr.AudioFile(f'voices/voice{message.from_user.id}.wav') as source:
                audio_text = r.listen(source)
                try:
                    text = r.recognize_google(audio_text, language='eng')
                    if await has_cursed_word(text):
                        await text_to_speech_send(message.bot, message.chat.id, "Прошу вести корректный диалог или Попробуйте сформулировать ответ без использования запрещенных слов, мы не поддерживаем беседы на данную тему\n\n-----\n\nI ask you to conduct a correct dialogue or try to formulate an answer without using forbidden words. We do not support conversations on this topic")
                        return
                except Exception as e:
                    await message.answer("I didn't get it")
            response = await request_to_gpt(message.from_user.id, text)
            await change_mode(message.from_user.id, cur_mode)
            await text_to_speech_send(message.bot, message.chat.id, response)
            return
    lang = list(langid.classify(message.text))[0]
    if  lang != 'ru' and lang != 'en':
        await message.answer("Hey there! Looks like we speak different languages. Let's go back to English.")
        return
    response = await request_to_gpt(message.from_user.id, message.text)
    await message.answer(response, parse_mode=ParseMode.MARKDOWN)

async def register_handlers(dp: Dispatcher):
    dp.register_message_handler(voice_handler, content_types=['voice'])
    dp.register_message_handler(handle_all_messages)