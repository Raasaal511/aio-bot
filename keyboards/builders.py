from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build_reply_keyboard(items: list[str]):
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)