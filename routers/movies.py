from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db import create_movie
from states.movies import AddMovie

router = Router()


@router.message(Command("add_movie"))
async def add_movie(message: Message, state: FSMContext):
    await message.answer("Добавим фильм.\n\nВведите название:")
    await state.set_state(AddMovie.title)


@router.message(AddMovie.title)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await message.answer("Год выпуска (например 1999):")
    await state.set_state(AddMovie.year)


@router.message(AddMovie.year)
async def add_year(message: Message, state: FSMContext):
    try:
        year = int(message.text.strip())
        await state.update_data(year=year)
        await message.answer("Жанр (например Боевик):")
        await state.set_state(AddMovie.genre)

    except ValueError:
        await message.answer("Год должен быть числом. Пример: 1999. Попробуйте ещё раз:")
        return
    

@router.message(AddMovie.genre)
async def add_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text.strip())
    await message.answer("Рейтинг (например 8.7):")
    await state.set_state(AddMovie.rating)


@router.message(AddMovie.rating)
async def add_rating(message: Message, state: FSMContext):
    try:
        rating = float(message.text.replace(",", ".").strip())
        await state.update_data(rating=rating)
        await message.answer("Ссылка на постер (или '-' если нет):")
        await state.set_state(AddMovie.poster_url)
    
    except ValueError:
        await message.answer("Рейтинг должен быть числом. Пример: 8.7. Попробуйте ещё раз:")
        return
    

@router.message(AddMovie.poster_url)
async def add_poster(message: Message, state: FSMContext):
    poster = message.text.strip()
    poster_url = "" if poster == "-" else poster

    data = await state.get_data()
    title, year, genre, rating = data["title"], data["year"], data["genre"], data["rating"]
    await create_movie(
        title=title,
        year=year,
        genre=genre,
        rating=rating,
        poster_url=poster_url,
    )
    await message.answer(
        "Готово! Фильм добавлен.\n"
        "Описание фильма:\n\n"
        f"{title} ({year}) — {genre} ⭐ {rating}"
    )
    await state.clear()