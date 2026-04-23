from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from db import search_movies

router = Router()


@router.inline_query()
async def inline_movies(query: InlineQuery):
    text = query.query.strip()
    if not text:
        await query.answer(results=[], cache_time=1, is_personal=True)
        return
    try:
        offset = int(query.offset) if query.offset else 0
    except ValueError:
        offset = 0

    limit = 10 
    movies = await search_movies(text=text, limit=limit, offset=offset)
    
    results = []
    for movie in movies:
        title = movie["title"]
        year = movie["year"]
        genre = movie["genre"]
        rating = movie["rating"]
        poster = movie["poster_url"]
    
        shown_title = f"{title}" + (f" ({year})" if year else "")
        description = " • ".join([p for p in [genre, f"⭐ {rating}"] if p])
        card_text = f"🎬 {shown_title}\n{description}".strip()
        
        inline_articale = InlineQueryResultArticle(
                id=str(movie["id"]),
                title=shown_title,
                description=description,
                thumbnail_url=poster,
                thumbnail_height=200,
                thumbnail_width=300,
                input_message_content=InputTextMessageContent(message_text=card_text),
            )
        results.append(inline_articale)

    next_offset = ""
    if len(movies) == limit:
        next_offset = str(offset + limit)

    await query.answer(
        results=results,
        cache_time=10,
        is_personal=True,
        next_offset=next_offset,
    )