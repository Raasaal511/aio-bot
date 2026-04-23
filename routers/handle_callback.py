from random import randint

from aiogram import Router, F

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command("random"))
async def random_handle(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Click me", callback_data="rand"))
    await message.answer("Нажми, чтобы отправить число от 1 до 10",
                         reply_markup=builder.as_markup())
    

@router.callback_query(F.data == "rand")
async def send_rand_num(callback: CallbackQuery):
    await callback.answer(show_alert="Bot get rand num")
    await callback.message.answer(str(randint(1, 10)))
