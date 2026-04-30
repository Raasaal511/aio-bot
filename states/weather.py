from aiogram.fsm.state import State, StatesGroup


class WeatherState(StatesGroup):
    city = State()