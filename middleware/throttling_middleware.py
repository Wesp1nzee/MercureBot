from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from cachetools import TTLCache
from config import Config, load_config

config: Config = load_config()
CACHE = TTLCache(maxsize=10000, ttl=0.5)  # Максимальный размер кэша - 10000 ключей, а время жизни ключа - 5 секунд

class ThrottlingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data['event_from_user']
        admin_ids: int = config.tg_bot.admin_ids
        
        if user.id != admin_ids:
            if user.id in CACHE:
                return

            CACHE[user.id] = True

        return await handler(event, data)