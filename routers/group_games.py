from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji

from aiogram.types import Message
from aiogram.filters.command import Command


router = Router()


@router.message(
        F.chat.type.in_(["group", "supergroup"]),
        Command("dice"))
async def dice_in_group_handle(messsage: Message):
    print(messsage.from_user.id)
    await messsage.answer_dice(emoji=DiceEmoji.DICE)


@router.message(
        F.chat.type.in_(["group", "supergroup"]),
        Command("basketball"))
async def basketball_in_group_handle(messsage: Message):
    await messsage.answer_dice(emoji=DiceEmoji.BASKETBALL)
