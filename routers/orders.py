from aiogram import Router, F

from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from states.orders import OrderFood
from keyboards.builders import build_reply_keyboard
from keyboards.buttons import food_names, food_sizes

router = Router()


@router.message(StateFilter(None), Command("food"))
async def order_hanlde(message: Message, state: FSMContext): 
    await message.answer(
        text="Выберите блюдо:", 
        reply_markup=build_reply_keyboard(food_names)
        )
    await state.set_state(OrderFood.food_name)


@router.message(OrderFood.food_name, F.in_(food_names))
async def food_name_choice(message: Message, state: FSMContext): 
    await state.update_data(food=message.text)
    await message.answer(
        text="Спасибо теперь выбери размер порции:", 
        reply_markup=build_reply_keyboard(food_sizes)
        )
    await state.set_state(OrderFood.food_size)


@router.message(OrderFood.food_name)
async def food_inccorect_choice(message: Message):
    await message.answer(
        text="Такого блюда нет в списке выберите другое:", 
        reply_markup=build_reply_keyboard(food_names)
        )
    

@router.message(OrderFood.food_size, F.text.in_(food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"Вы выбрали {message.text.lower()} порцию {user_data['food']}.\n"
             f"Попробуйте теперь заказать напитки: /drinks",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(...)


@router.message(OrderFood.food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого размера порции.\n\n"
             "Пожалуйста, выберите один из вариантов из списка ниже:",
        reply_markup=build_reply_keyboard(food_sizes)
    )


...
