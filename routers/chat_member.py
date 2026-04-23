from aiogram import Router, F
from aiogram.filters.chat_member_updated import (ChatMemberUpdatedFilter, 
                                                 MEMBER,
                                                 KICKED, 
                                                 JOIN_TRANSITION)
from aiogram.filters.command import Command, CommandStart
from aiogram.types import ChatMemberUpdated, Message

router = Router()

router.my_chat_member.filter(F.chat.type == "private")
router.message.filter(F.chat.type == "private")

user_ids: set = set()


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def bot_add_to_group(event: ChatMemberUpdated):
    print("Бота добавили в чат!")
    user_id: int = event.jo
    user_ids.update(user_id)


@router.my_chat_member(ChatMemberUpdatedFilter(KICKED))
async def bot_blocked(event: ChatMemberUpdated):
    print(f"{event.from_user.username} заблокировал бота :(")
    user_id: int = event.from_user.id
    user_ids.discard(user_id)


@router.my_chat_member(ChatMemberUpdatedFilter(MEMBER))
async def bot_added_to_chat(event: ChatMemberUpdated):
    print("Бота добавили в чат!")
    user_id: int = event.from_user.id
    user_ids.update(user_id)


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_ids.add(message.from_user.id) 
    await message.answer("Привет!")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Доступные команды:\n/start - начать\n/help - помощь")


@router.message(Command("users"))
async def handle_users(message: Message):
    users = "\n".join(f"ID: {user_id}" for user_id in user_ids)
    return await message.answer(users)


# @router.message(F.text)
# async def handle_message(message: Message):
#     user_id: int = message.from_user.id
#     if user_id in user_ids:
#         await message.answer(f"Получил ваше сообщение: {message.text}")
#     else:
#         await message.answer("Вы не в списке разрешенных пользователей")
