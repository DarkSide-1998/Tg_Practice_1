import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message

from string import ascii_lowercase as al, ascii_uppercase as au, digits as dig


class IsValidField(BaseFilter):
    def __init__(self, allow_chars: str, min_len: int, max_len: int) -> None:
        self.allow_chars = allow_chars
        self.min_len = min_len
        self.max_len = max_len
        
    async def __call__(self, message: Message) -> None:
        return self.min_len <= len(message.text) <= self.max_len and all(ch in al + au + dig + self.allow_chars for ch in message.text)


class IsValidNumber(BaseFilter):
    def __init__(self, min_num: int, max_num: int) -> None:
        self.min_num = min_num
        self.max_num = max_num
        
    async def __call__(self, message: Message) -> None:
        if message.text.strip().isdigit():
            return self.min_num <= int(message.text) <= self.max_num
        else:
            return False