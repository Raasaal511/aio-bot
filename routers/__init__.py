from aiogram import Router

# from routers.start import router as start_router
# from routers.specials import router as special_router
# from routers.handle_callback import router as callback_router
# from routers.group_games import router as game_router
# from routers.keywords import router as keyword_router
from routers.chat_member import router as chat_router
from routers.auth import router as auth_router
from routers.inline_movies import router as inline_router
from routers.movies import router as movie_router
from routers.payment import router as payment_router
# from middlewares.slowing import SlowMiddleware

router = Router()

# game_router.message.middleware(SlowMiddleware(delay=2))
# start_router.message.middleware(SlowMiddleware(delay=5))

router.include_routers(
    # start_router,
    # special_router,
    # callback_router,
    # game_router,
    # keyword_router,
    inline_router,
    movie_router,
    chat_router,
    auth_router,
    payment_router,
)