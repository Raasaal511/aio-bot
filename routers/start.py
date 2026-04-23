from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    kb = [
        [KeyboardButton(text="С пюрешкой")],
        [KeyboardButton(text="Без пюрешки")],
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=kb,
        input_field_placeholder="Способ подачи",
        resize_keyboard=True,
        )
    await message.answer("Как подать котлеты?", reply_markup=markup)


@router.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: Message):
    await message.answer(text="ДА ПЮРЕ ЭТО ЖЕ ИМБА!")


@router.message(F.text.lower() == "без пюрешки")
async def without_puree(message: Message):
    await message.answer(text="ТАКЖЕ НИКТО НЕ ЕСТ!! :(")


@router.message(Command("reply_builder"))
async def reply_builder(message: Message):
    builder= ReplyKeyboardBuilder()
    for i in range(1, 17):
        btn = KeyboardButton(text=str(i))
        builder.add(btn)
    builder.adjust(4)
    await message.answer(
        "Выберите число:", 
        reply_markup=builder.as_markup(resize_keyboard=True)
        )
