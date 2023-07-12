import aiogram
from aiogram.utils import executor
from aiogram.types import *
from settings import *

bot = aiogram.Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = aiogram.Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: Message):
    pass

executor.start_polling(dp)