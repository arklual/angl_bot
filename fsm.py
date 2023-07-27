from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ChangeGPT_Params(StatesGroup):
    ChangeTokens = State()
    ChangeTemp = State()