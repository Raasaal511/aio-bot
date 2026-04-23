from aiogram import Router
from aiogram.types import Message

# from filters.keywords import ContainsKeywordFilter, WorkingHoursFilter

router = Router()


# @router.message(ContainsKeywordFilter(keyword="python"))
# async def keyword_contains_handle(message: Message):
#     await message.answer("YOU SAY PYHTON!")


# @router.message(ContainsKeywordFilter(keyword="python"), WorkingHoursFilter())
# async def cmd_python_off_work(message: Message):
#     await message.answer("Python в рабочее время!")


# @router.message(ContainsKeywordFilter(keyword="python"))
# async def cmd_python_work(message: Message):
#     await message.answer("Python и в нерабочее время?")

