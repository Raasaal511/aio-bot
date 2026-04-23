from aiogram.fsm.state import State, StatesGroup


class AddMovie(StatesGroup):
    title = State()
    year = State()
    genre = State()
    rating = State()
    poster_url = State()
