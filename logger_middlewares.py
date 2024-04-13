from typing import Any, Awaitable, Callable, Dict

from aiomysql import DataError

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.datacoonect import db


class LoggerMiddleware(BaseMiddleware):
    """Обновление логов"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        message = event.message
        query = event.callback_query
        # Проверяем, есть ли сообщение

        if message:
            # Проверяем, есть ли текст в сообщении

            if message.text:
                # Проверяем, что текст сообщения не равен "/start"

                if not (message.text in "/start"):
                    try:
                        # Пытаемся добавить лог в базу данных

                        await db.add_log(user_id=user.id, content=message.text)
                    except DataError:
                        # Если пользователь отправляет текст больше 100 символов

                        await db.add_log(user_id=user.id, content=message.text[:100])
        
        # Проверяем, что переменная query не пустая
        if query:
            await db.add_log(user_id=user.id, content=query.data)
        return await handler(event, data)
