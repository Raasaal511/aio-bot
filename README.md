# Урок: бот “Фильмотека” — добавление фильмов (FSM) + поиск через Inline mode (aiogram 3)

Этот файл — **конспект урока**, который можно объяснять. Логика такая:
1) сначала фиксируем, **что уже есть** в проекте  
2) затем добавляем **2 фичи**:  
   - команда `/add_movie` (FSM) — добавляем фильмы в SQLite  
   - Inline mode `@BotName query` — ищем фильмы и отправляем “карточку” текстом  
3) в конце проверяем и разбираем типовые ошибки

---

## 1) Что мы уже имеем в проекте (стартовая точка)

### 1.1 Запуск бота
- Файл `bot.py` создаёт `Bot` и `Dispatcher`, подключает роутеры и запускает polling.

### 1.2 Как подключаются роутеры
- Файл `routers/__init__.py` создаёт общий `router` и подключает другие роутеры через `router.include_routers(...)`.
- Важно: если вы написали файл-роутер, но **не подключили** его в `routers/__init__.py`, обработчики **никогда** не сработают.

### 1.3 Состояния (FSM)
- Файл `states/movies.py` уже содержит `StatesGroup` `AddMovie`:
  - `title`, `year`, `genre`, `rating`, `poster_url`

### 1.4 База данных (SQLite)
- Файл `db.py` использует `aiosqlite`.
- Таблица `movies` создаётся через `init_db()`:
  - `id`, `title`, `year`, `genre`, `rating`, `poster_url`

### 1.5 Что пока НЕ готово
- `routers/movies.py` — заготовка, FSM не реализован.
- Inline mode обработчика пока нет.

---

## 2) Теория: Inline mode vs Inline keyboard (объяснить 30 секунд)

### Inline mode (inline queries)
- Пользователь пишет **в любом чате**: `@username_бота запрос`
- Telegram присылает вашему боту событие `InlineQuery`
- Бот отвечает списком вариантов (результатов)

### Inline keyboard
- Это кнопки под сообщением (`InlineKeyboardMarkup`)
- Это **не** inline mode и **не** включается через BotFather `/setinline`

---

## 3) Подготовка окружения (чтобы урок “запустился”)

### 3.1 Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.2 `.env` с токеном

Создайте `.env` в корне:

```env
BOT_TOKEN=123456:ABCDEF_your_token_here
```

В `config.py` токен берётся из `BOT_TOKEN`.

---

## 4) Часть A — добавление фильма через FSM (`/add_movie`)

Цель: пользователь пишет `/add_movie`, а бот по шагам спрашивает поля фильма и сохраняет в SQLite.

### 4.1 Что такое FSM в этом проекте
FSM — это “диалог по шагам”. Состояния у нас уже есть в `states/movies.py` (`AddMovie.title`, `AddMovie.year` и т.д.).

### 4.2 Какой код нужно написать в `routers/movies.py`

Ниже — **минимальный хороший пример**: простая валидация, сохранение в БД и очистка состояния.

Создайте/заполните `routers/movies.py` так:

```python
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db import create_movie
from states.movies import AddMovie

router = Router()


@router.message(Command("add_movie"))
async def cmd_add_movie(message: Message, state: FSMContext):
    await message.answer("Добавим фильм.\n\nВведите название:")
    await state.set_state(AddMovie.title)


@router.message(AddMovie.title)
async def add_movie_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text.strip())
    await message.answer("Год выпуска (например 1999):")
    await state.set_state(AddMovie.year)


@router.message(AddMovie.year)
async def add_movie_year(message: Message, state: FSMContext):
    try:
        year = int(message.text.strip())
    except ValueError:
        await message.answer("Год должен быть числом. Пример: 1999. Попробуйте ещё раз:")
        return

    await state.update_data(year=year)
    await message.answer("Жанр (например Sci-Fi):")
    await state.set_state(AddMovie.genre)


@router.message(AddMovie.genre)
async def add_movie_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text.strip())
    await message.answer("Рейтинг (например 8.7):")
    await state.set_state(AddMovie.rating)


@router.message(AddMovie.rating)
async def add_movie_rating(message: Message, state: FSMContext):
    try:
        rating = float(message.text.replace(",", ".").strip())
    except ValueError:
        await message.answer("Рейтинг должен быть числом. Пример: 8.7. Попробуйте ещё раз:")
        return

    await state.update_data(rating=rating)
    await message.answer("Ссылка на постер (или '-' если нет):")
    await state.set_state(AddMovie.poster_url)


@router.message(AddMovie.poster_url)
async def add_movie_poster(message: Message, state: FSMContext):
    poster = message.text.strip()
    poster_url = "" if poster == "-" else poster

    data = await state.get_data()
    movie_id = await create_movie(
        title=data["title"],
        year=data["year"],
        genre=data["genre"],
        rating=data["rating"],
        poster_url=poster_url,
    )

    await message.answer(
        "Готово! Фильм добавлен.\n\n"
        f"id: {movie_id}\n"
        f"{data['title']} ({data['year']}) — {data['genre']} ⭐ {data['rating']}"
    )
    await state.clear()
```

### 4.3 Важная мысль для объяснения
- FSM хранит промежуточные данные в `FSMContext`.
- Мы не “собираем строку”, а постепенно делаем `state.update_data(...)`.
- В конце берём `state.get_data()` → сохраняем в БД → `state.clear()`.

---

## 5) Часть B — подключаем Telegram Inline mode (поиск фильмов)

Цель: пользователь вводит `@BotName matrix` и получает варианты фильмов из БД.

### 5.1 Включить Inline mode в BotFather
Inline mode не работает “по умолчанию”, его нужно включить:

1) Откройте BotFather  
2) `/setinline`  
3) выберите вашего бота  
4) задайте placeholder, например: `Поиск фильмов…`

### 5.2 Функция поиска в БД (`db.py`)

Смысл: мы хотим найти фильмы по подстроке в `title`, ограничить количество и (опционально) поддержать `offset`.

Пример функции:

```python
async def search_movies(text: str, limit: int = 10, offset: int = 0) -> list[dict]:
    pattern = f"%{text.strip()}%"
    # Подсказки (сделай X → получишь Y):
    # - WHERE title LIKE pattern
    # - LIMIT limit    → максимум limit результатов (inline не должен отдавать всё)
    # - OFFSET offset  → следующая “страница” результатов (для next_offset)
    #
    # Дальше по шагам заводим переменные:
    # db      → подключение к базе (aiosqlite.connect)
    # cursor  → результат db.execute(...)
    # rows    → список строк из cursor.fetchall()
    # result  → список dict

    # result = [dict(r) for r in rows]
    # return result
```

### 5.3 Inline роутер: `routers/inline_movies.py`

Создайте файл `routers/inline_movies.py`:

```python
from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from db import search_movies

router = Router()


@router.inline_query()
async def inline_movies(query: InlineQuery):
    text = (query.query or "").strip()
    if not text:
        await query.answer(results=[], cache_time=1, is_personal=True)
        return

    # Telegram присылает offset как строку
    try:
        offset = int(query.offset) if query.offset else 0
    except ValueError:
        offset = 0

    limit = 10
    movies = await search_movies(text=text, limit=limit, offset=offset)

    results = []
    for m in movies:
        title = m["title"]
        year = m.get("year")
        genre = m.get("genre")
        rating = m.get("rating")

        shown_title = f"{title}" + (f" ({year})" if year else "")
        description = " • ".join([p for p in [genre, (f"⭐ {rating}" if rating is not None else None)] if p])
        card_text = f"🎬 {shown_title}\n{description}".strip()

        results.append(
            InlineQueryResultArticle(
                id=str(m["id"]),
                title=shown_title,
                description=description,
                input_message_content=InputTextMessageContent(message_text=card_text),
            )
        )

    next_offset = ""
    if len(movies) == limit:
        next_offset = str(offset + limit)

    await query.answer(
        results=results,
        cache_time=1,
        is_personal=True,
        next_offset=next_offset,
    )
```

### 5.4 Что важно объяснить ученику
- `InlineQueryResultArticle` — самый простой тип результата, “железобетонный” для начала.
- `cache_time=1` для разработки, чтобы изменения быстро “подхватывались”.
- `next_offset` — простой способ пагинации (Telegram будет вызывать вас снова с offset).

---

## 6) Подключение роутеров (самая частая ошибка новичков)

После того как файлы `routers/movies.py` и `routers/inline_movies.py` готовы, их надо подключить в `routers/__init__.py`.

Схема:

```python
from routers.movies import router as movies_router
from routers.inline_movies import router as inline_movies_router

router.include_routers(
    # ...
    movies_router,
    inline_movies_router,
)
```

Если этого не сделать — бот “как будто работает”, но `/add_movie` и inline не реагируют.

---

## 7) Проверка (как показывать на уроке)

1) Запустите бота:

```bash
python bot.py
```

2) В личке боту выполните `/add_movie` и добавьте 1–2 фильма  
3) В любом чате (можно “Избранное”) введите:
   - `@YourBotName matrix`
4) Должны появиться варианты. Выберите — отправится текстовая карточка.

---

## 8) Типовые проблемы (и как их объяснить)

### Inline mode не показывается при `@BotName`
- Inline не включён в BotFather (`/setinline`) или введён неверный username.

### Команда `/add_movie` не работает
- `movies_router` не подключён в `routers/__init__.py`.

### Inline ничего не возвращает
- `inline_movies_router` не подключён в `routers/__init__.py`.
- В БД нет фильмов (вы ещё не добавили их через FSM).
- Таблица `movies` не создана (не вызвали `init_db()` хотя бы один раз).

