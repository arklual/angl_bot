from aiogram import Dispatcher
import basic_handlers
import payments
import admin
import dialog_handler
import user_profile


async def register_all_handlers(dp: Dispatcher):
    await payments.register_handlers(dp)
    await payments.register_callbacks(dp)
    await profile.register_callbacks(dp)
    await admin.register_handlers(dp)
    await admin.register_callbacks(dp)
    await basic_handlers.register_handlers(dp)
    await basic_handlers.register_callbacks(dp)
    await dialog_handler.register_handlers(dp)
