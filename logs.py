from typing import Any, Awaitable, Callable, Dict

from aiomysql import DataError

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.datacoonect import db


class LoggerMiddleware(BaseMiddleware):
    """Logs the updates."""

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        chat = data["event_chat"] 
        message = event.message 
        query = event.callback_query 

        if message:
            try:  
                await db.add_log(
                    chat_id=chat.id,
                    user_id=user.id,
                    user_full_name=user.full_name,
                    telegram_object="message",
                    content=message.text
                    )
                
            except DataError:
                await db.add_log(
                    chat_id=chat.id,
                    user_id=user.id,
                    user_full_name=user.full_name,
                    telegram_object="message",
                    content=message.text[:100]
                    )

        if query:
            await db.add_log(
                chat_id=chat.id,
                user_id=user.id,
                user_full_name=user.full_name,
                telegram_object="query",
                content=query.data
                )

        return await handler(event, data)
