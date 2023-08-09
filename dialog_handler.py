import traceback
from aiogram import Dispatcher
from aiogram.types import *
from payments import check_subscription
from utils import *
from strings import *
import langid
import os
import speech_recognition as sr


async def voice_handler(message: Message):
    is_subed = await check_subscription(message.from_user.id)
    if is_subed:
        file_id = message.voice.file_id
        file_info = await message.bot.get_file(file_id)
        file_path = file_info.file_path
        await message.bot.download_file(file_path,
                                        f"voices/voice{message.from_user.id}.oga")

        # Используйте ffmpeg для конвертации аудио из формата .oga в .wav
        os.system(
            f'ffmpeg -i voices/voice{message.from_user.id}.oga voices/voice{message.from_user.id}.wav'
        )

        # Загрузите аудиофайл и преобразуйте речь в текст
        r = sr.Recognizer()
        with sr.AudioFile(f'voices/voice{message.from_user.id}.wav') as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text, language='eng')
                if await has_cursed_word(text):
                    await text_to_speech_send(
                        message.bot, message.chat.id,
                        "Прошу вести корректный диалог или Попробуйте сформулировать ответ без использования запрещенных слов, мы не поддерживаем беседы на данную тему\n\n-----\n\nI ask you to conduct a correct dialogue or try to formulate an answer without using forbidden words. We do not support conversations on this topic"
                    )
                    return
                lang = list(langid.classify(text))[0]
                if lang != 'ru' and lang != 'en':
                    await text_to_speech_send(
                        message.bot, message.chat.id,
                        "Hey there! Looks like we speak different languages. Let's get back to English."
                    )
                    return
                response = await request_to_gpt(message.from_user.id, text)
                kb = ReplyKeyboardMarkup([
                    ['Проверить грамматику'],
                ],
                                        resize_keyboard=True,
                                        one_time_keyboard=True)
                await text_to_speech_send(message.bot,
                                        message.chat.id,
                                        response,
                                        reply_markup=kb)
            except Exception as e:
                traceback.print_exc()
                text = "Sorry, I did not get that"
                await message.answer(text)
            finally:
                os.system(f'rm voices/voice{message.from_user.id}.oga')
                os.system(f'rm voices/voice{message.from_user.id}.wav')
    else:
        await message.answer("У вас нет подписки")


async def handle_all_messages(message: Message):
    is_subed = await check_subscription(message.from_user.id)
    if is_subed:
        if await has_cursed_word(message.text):
            await message.answer(
                'Прошу вести корректный диалог или Попробуйте сформулировать ответ без использования запрещенных слов, мы не поддерживаем беседы на данную тему\n\n-----\n\nI ask you to conduct a correct dialogue or try to formulate an answer without using forbidden words. We do not support conversations on this topic'
            )
            return
        if message.reply_to_message and message.reply_to_message.text:
            if '/' in message.text:
                mode = message.text.replace('/', '')
                context = await get_context(message.from_user.id)
                await create_new_context(
                    message.from_user.id, {
                        'messages': [],
                        'mode': mode,
                        'is_male_voice': context['is_male_voice']
                    })
                await change_mode(message.from_user.id, mode)
                response = await request_to_gpt(message.from_user.id,
                                                message.reply_to_message.text)
                await message.answer(response)
                await create_new_context(message.from_user.id, context)
                return
        elif message.reply_to_message and message.reply_to_message.voice:
            if '/' in message.text:
                mode = message.text.replace('/', '')
                context = await get_context(message.from_user.id)
                await create_new_context(
                    message.from_user.id, {
                        'messages': [],
                        'mode': mode,
                        'is_male_voice': context['is_male_voice']
                    })
                await change_mode(message.from_user.id, mode)
                file_id = message.reply_to_message.voice.file_id
                file_info = await message.bot.get_file(file_id)
                file_path = file_info.file_path
                await message.bot.download_file(
                    file_path, f"voices/voice{message.from_user.id}.oga")

                # Используйте ffmpeg для конвертации аудио из формата .oga в .wav
                os.system(
                    f'ffmpeg -i voices/voice{message.from_user.id}.oga voices/voice{message.from_user.id}.wav'
                )

                # Загрузите аудиофайл и преобразуйте речь в текст
                r = sr.Recognizer()
                with sr.AudioFile(
                        f'voices/voice{message.from_user.id}.wav') as source:
                    audio_text = r.listen(source)
                    try:
                        text = r.recognize_google(audio_text, language='eng')
                        if await has_cursed_word(text):
                            await text_to_speech_send(
                                message.bot, message.chat.id,
                                "Прошу вести корректный диалог или Попробуйте сформулировать ответ без использования запрещенных слов, мы не поддерживаем беседы на данную тему\n\n-----\n\nI ask you to conduct a correct dialogue or try to formulate an answer without using forbidden words. We do not support conversations on this topic"
                            )
                            return
                    except Exception as e:
                        await message.answer("I didn't get it")
                response = await request_to_gpt(message.from_user.id, text)
                await create_new_context(message.from_user.id, context)
                await text_to_speech_send(message.bot, message.chat.id, response)
                return
        lang = list(langid.classify(message.text))[0]
        if lang != 'ru' and lang != 'en':
            await message.answer(
                "Hey there! Looks like we speak different languages. Let's get back to English."
            )
            return
        response = await request_to_gpt(message.from_user.id, message.text)
        kb = ReplyKeyboardMarkup([
            ['Check for grammar correctness'],
        ],
                                resize_keyboard=True,
                                one_time_keyboard=True)
        await message.answer(response,
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=kb)
    else:
        await message.answer("У вас нет подписки")


async def check_grammar_once(message: Message):
    is_subed = await check_subscription(message.from_user.id)
    if is_subed:
        context = await get_context(message.from_user.id)
        message_to_check = ""
        for i in context['messages'][::-1]:
            if i['from'] == 'user':
                message_to_check = i['message']
                break
        if message_to_check == "":
            await message.answer(
                "You didn\'t write anything."
            )
            return
        lang = list(langid.classify(str(message_to_check)))[0]
        if lang != 'ru' and lang != 'en':
            await message.answer(
                "Hey there! Looks like we speak different languages. Let's get back to English."
            )
            return
        await create_new_context(
            message.from_user.id, {
                'messages': [],
                'mode': 'grammar',
                'is_male_voice': context['is_male_voice']
            })
        response = await request_to_gpt(message.from_user.id,
                                        str(message_to_check))
        await create_new_context(message.from_user.id, context)
        await message.answer(response)
    else:
        await message.answer("У вас нет подписки")


async def register_handlers(dp: Dispatcher):
    dp.register_message_handler(check_grammar_once,
                                lambda m: m.text == 'Check for grammar correctness')
    dp.register_message_handler(voice_handler, content_types=['voice'])
    dp.register_message_handler(handle_all_messages)

