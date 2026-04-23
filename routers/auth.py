from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.types import Message

from states.users import UserForm

router = Router()


@router.message(Command("register"))
async def register_handle(message: Message, state: FSMContext):
    message_text = "Хорошо давай начнем регистрацию!\n\nВведите свое имя:"
    await message.answer(message_text)
    await state.set_state(UserForm.name)


@router.message(UserForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично!\n\nВведите вашу почту:")
    await state.set_state(UserForm.email)


@router.message(UserForm.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Отлично!\n\nВведите ваш пароль:")
    await state.set_state(UserForm.password)
 

@router.message(UserForm.password)
async def process_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data: dict = await state.get_data()
    user_data = f"name: {data["name"]}\nemail: {data["email"]}\npassword: {data["password"]}"
    message_text = f"Ваши данные\n{user_data}"
    await message.answer(message_text)
    await state.clear()
