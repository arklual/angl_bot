import aiogram
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import *
from handler_regitrator import register_all_handlers

bot = aiogram.Bot(TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)

async def on_start(_):
    await register_all_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_start, skip_updates=True)
