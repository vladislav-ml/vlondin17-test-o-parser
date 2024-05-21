from typing import Any, Awaitable, Callable, Dict

import aiomysql
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from tg_bot.other.db_connect import Request


class DbSession(BaseMiddleware):

    def __init__(self, connector: aiomysql.pool.Pool):
        super().__init__()
        self.connector = connector

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.connector.acquire() as connect:
            data['request'] = Request(connect)
            return await handler(event, data)
