from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from aiogram.types import *
import utils
import aiofiles
import json
from payments import check_subscription
from kb import *
from strings import get_ref_link_text

async def read_json():
    async with aiofiles.open('referals.json', mode="r",encoding='utf-8') as file:
        content = await file.read()
        data = json.loads(content)
    return data

async def get_user_by_id(data, user_id):
    for entry in data:
        if entry["user_id"] == user_id:
            return entry
    return None

async def profile(callback: CallbackQuery):
  data = await read_json()
  await callback.answer()
  user_entry = await get_user_by_id(data, callback.from_user.id)
  is_subed = await check_subscription(callback.from_user.id)
  lang = utils.get_user_language(callback.from_user.id)
  if not is_subed:  
    if lang == 'ru':
      await callback.message.answer("""Вы не подписаны""", reply_markup = profile_kb_if_unsubed('ru'))
    elif lang == 'en':
      await callback.message.answer("""You are not subscribed. """, reply_markup = profile_kb_if_unsubed('en'))
  else:
    if lang == 'ru':
      await callback.message.answer(f"У вас осталось {is_subed} дней в подписке.\nВаша реф. ссылка: https://t.me/SkillbuddyBot?start={callback.from_user.id}", reply_markup=profile_kb_if_subed('ru', callback.from_user.id))
    elif  lang == 'en':
      await callback.message.answer(f"Days left in your subscription: {is_subed} days\Your referal link: https://t.me/SkillbuddyBot?start={callback.from_user.id}", reply_markup=profile_kb_if_subed('en', callback.from_user.id))

async def share_ref_link(callback: CallbackQuery):
  await callback.answer()
  kb = InlineKeyboardMarkup()
  lang = utils.get_user_language(callback.from_user.id)
  if lang == 'ru':
    msg = 'Выберите текст:\n'
  elif lang == 'en':
    msg = 'Choose the text:\n'
  btns = []
  for i in range(1, 10):   
    ref_text = get_ref_link_text(i-1, f"https://t.me/SkillbuddyBot?start={callback.from_user.id}")
    msg += f'{i}. {ref_text}\n'
    btns.append(InlineKeyboardButton(text=str(i), url=f'https://t.me/share/url?text={ref_text}'))
  kb.row(*btns)
  await callback.message.answer(msg, reply_markup=kb)



async def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(profile, lambda callback_query: callback_query.data == 'user_profile')
    dp.register_callback_query_handler(share_ref_link, lambda callback_query: callback_query.data == 'share_ref_link')