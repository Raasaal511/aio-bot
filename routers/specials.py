from random import choice

from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, PhotoSize
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

router = Router()


@router.message(Command("special_buttons"))
async def special_buttons(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Запросить локацию", request_location=True),
        KeyboardButton(text="Запросить контакт", request_contact=True),

    )
    await message.answer("Выберите действие:", 
                         reply_markup=builder.as_markup(resize_keeboard=True))


@router.message(Command("profile_links"))
async def profile_links(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Ссылка на GitHub", 
            url="https://github.com/Raasaal511"
            ))
    builder.row(
        InlineKeyboardButton(
            text="Ссылка на Youtube",
            url="https://www.youtube.com/@rasulyusupov8599"
            ))
    await message.answer("Выберите ссылку:", 
                         reply_markup=builder.as_markup(resize_keeboard=True))
    

@router.message(Command("motivation"))
async def get_motivations(message: Message):
    text = [
        "Ты хорош",
        "Ты хороший друг",
        "Ты ок",
    ]
    access_users = (916119054,)
    print(message.from_user.id)
    if message.from_user.id in access_users:
        await message.answer(f"{choice(text)}")
    else:
        await message.answer("Тебе не отвечу")


@router.message(F.photo[-1].as_("largest_photo"))
async def get_photo_handle(message: Message, largest_photo: PhotoSize):
    print(largest_photo.width, largest_photo.height)
    await message.answer("This photo")
