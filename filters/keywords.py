from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ContainsKeywordFilter(BaseFilter):
    def __init__(self, keyword: str):
        self.keyword = keyword

    async def __call__(self, message: Message) -> bool:
        return self.keyword in message.text.lower()


class WorkingHoursFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        current_hour = datetime.now().hour
        print(current_hour)
        return 9 <= current_hour < 18
