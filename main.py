import aiogram
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import *
import aioschedule
import aiofiles
import json
import datetime
from handler_regitrator import register_all_handlers

bot = aiogram.Bot(TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)


async def check_subscribers():
    subscribers = []
    async with aiofiles.open('payments.json', 'r', encoding='utf-8') as fp:
        subscribers = json.loads(await fp.read())
    new_subscribers = []
    for subscriber in subscribers:
        if datetime.datetime.today() <= datetime.datetime.strptime(
                subscriber['date_exp'], '%d/%m/%Y'):
            new_subscribers.append(subscriber)
    async with aiofiles.open('payments.json', 'w', encoding='utf-8') as fp:
        await fp.write(json.dumps(new_subscribers, ensure_ascii=False))

async def clean_whitelist():
    async with aiofiles.open('whitelist.json', 'w', encoding='utf-8') as fp:
        await fp.write('[]')

async def on_start(_):
    aioschedule.every(1).day.at("00:00").do(check_subscribers)
    aioschedule.every(1).day.at("00:00").do(clean_whitelist)
    await register_all_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_start, skip_updates=True)
