from aiogram import Dispatcher
from settings import PAYMENT_TOKEN_TEST
from aiogram.types import *


PRICE = LabeledPrice(label='Подписка на 1 месяц', amount=500*100) # 500 rub
async def subscribe(message: Message):
    if PAYMENT_TOKEN_TEST.split(':')[1] == "TEST":
        await message.answer('Тестовый платеж')
    await message.bot.send_invoice(
        message.chat.id,
        title="Подписка на бота",
        description='Активация подписки на бота на 1 месяц',
        provider_token=PAYMENT_TOKEN_TEST,
        currency='rub',
        photo_url='https://media.istockphoto.com/id/679762242/ru/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F/%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81%D0%BC%D0%B5%D0%BD-%D0%B8%D0%BB%D0%B8-%D1%82%D0%BE%D1%80%D0%B3%D0%BE%D0%B2%D0%B5%D1%86-%D0%BD%D0%B0-%D1%84%D0%BE%D0%BD%D0%B4%D0%BE%D0%B2%D0%BE%D0%BC-%D1%80%D1%8B%D0%BD%D0%BA%D0%B5-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D1%8E%D1%89%D0%B8%D0%B9-%D0%B7%D0%B0-%D1%81%D1%82%D0%BE%D0%BB%D0%BE%D0%BC.jpg?s=1024x1024&w=is&k=20&c=OsEncaxRjp-sbXTQUGF7XtFfSHvG03Cvu1JNl8kis7Y=',
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=[PRICE],
        start_parameter='one-month-subscription',
        payload='test-invoice-payload'
    )

async def subscribe_c(callback: CallbackQuery):
    await callback.answer()
    if PAYMENT_TOKEN_TEST.split(':')[1] == "TEST":
        await callback.message.answer('Тестовый платеж')
    await callback.bot.send_invoice(
        callback.message.chat.id,
        title="Подписка на бота",
        description='Активация подписки на бота на 1 месяц',
        provider_token=PAYMENT_TOKEN_TEST,
        currency='rub',
        photo_url='https://media.istockphoto.com/id/679762242/ru/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F/%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81%D0%BC%D0%B5%D0%BD-%D0%B8%D0%BB%D0%B8-%D1%82%D0%BE%D1%80%D0%B3%D0%BE%D0%B2%D0%B5%D1%86-%D0%BD%D0%B0-%D1%84%D0%BE%D0%BD%D0%B4%D0%BE%D0%B2%D0%BE%D0%BC-%D1%80%D1%8B%D0%BD%D0%BA%D0%B5-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D1%8E%D1%89%D0%B8%D0%B9-%D0%B7%D0%B0-%D1%81%D1%82%D0%BE%D0%BB%D0%BE%D0%BC.jpg?s=1024x1024&w=is&k=20&c=OsEncaxRjp-sbXTQUGF7XtFfSHvG03Cvu1JNl8kis7Y=',
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=[PRICE],
        start_parameter='one-month-subscription',
        payload='test-invoice-payload'
    )

async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

async def successful_payment(message: Message):
    payment_info = message.successful_payment.to_python()
    for k, v in  payment_info.items():
        print(f"{k} = {v}")
    # Добавлять пользователя в бд + считать срок окончания подписки
    await message.answer(f'Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!')

async def register_handlers(dp: Dispatcher):
    dp.register_message_handler(subscribe, commands=['subscribe'])
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)

async def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(subscribe_c, lambda callback:  callback.data == "subscribe")