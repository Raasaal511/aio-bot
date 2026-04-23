from aiogram.fsm.state import State, StatesGroup


class OrderFood(StatesGroup):
    food_name = State()
    food_size = State()
