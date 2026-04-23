import aiosqlite

PATH_DB = "movies.db"


async def init_db():
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER,
                genre TEXT,
                rating REAL,
                poster_url TEXT
            )
        """)
        await db.commit()


async def create_movie(
    title: str,
    year: int,
    genre: str,
    rating: float,
    poster_url: str,
):
    async with aiosqlite.connect(PATH_DB) as db:
        await db.execute(
            """
            INSERT INTO movies(title, year, genre, rating, poster_url) 
            VALUES (?, ?, ?, ?, ?)
            """, (title, year, genre, rating, poster_url)
        )
        await db.commit()


async def search_movies(text: str, limit: int = 10, offset: int = 0) -> list[dict]:
    pattern = f"%{text.strip()}%"
    async with aiosqlite.connect(PATH_DB) as db:
        db.row_factory = aiosqlite.Row

        if pattern.lower() != "all-movies":
            cursor = await db.execute("""
                SELECT * FROM movies
                WHERE title LIKE ?
                LIMIT ?
                OFFSET ?                             
                """, (pattern, limit, offset))
            result = await cursor.fetchall()
        else:
            cursor = await db.execute("""
                    SELECT * FROM movies
                    LIMIT ?
                    OFFSET ?
                """, (limit, offset))
            result = await cursor.fetchall()

        movies = [dict(res) for res in result]
        return movies

