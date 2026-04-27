from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery

from utils.payment_message import START_MESSAGE, PRICE
from config import bot_settings

router = Router()

@router.message(Command("premium_info"))
async def info_premium_handle(messsage: Message):
    await messsage.answer(START_MESSAGE)


@router.message(Command("buy"))
async def payment_handle(message: Message):
    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title="Преиум подписка",
        description="Новый контент",
        payload="premium-access",
        provider_token=bot_settings.PAYMENT_TOKEN,
        currency="RUB",
        prices=PRICE,
    )


@router.pre_checkout_query()
async def chechout_handle(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(lambda message: message.successful_payment is not None)
async def successful_payment_handle(message: Message):
    await message.answer("Payment successful!")