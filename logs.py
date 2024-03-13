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
        chat = data["event_chat"] 
        message = event.message 
        query = event.callback_query 
        try:
            if message.text:
                if not (message.text in "/start"):
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
        except AttributeError:
            print("AttributeError")


        # Проверяем, что переменная query не пустая
        if query:
            # Проверяем, содержится ли значение переменной query.data в строке 'informatics'
            if query.data.startswith('informatics') or query.data.startswith('task:informatics'):
                # Разбиваем значение переменной query.data по символу ":"

                parsed_query = query.data.split(":")

                # Проверяем, что первый элемент разбитого значения не равен "task"
                if not query.data.startswith('task:informatics'):
                    # Добавляем лог в базу данных с указанными параметрами
                    await db.add_log(
                        chat_id=chat.id,
                        user_id=user.id,
                        user_full_name=user.full_name,
                        telegram_object="query",
                        content='informatics'
                    )

                else:
                    # Получаем третий элемент разбитого значения и сохраняем его в переменную task_parsed_query
                    task_parsed_query = parsed_query[2]
                    # Добавляем лог в базу данных с указанными параметрами
                    await db.add_log(
                        chat_id=chat.id,
                        user_id=user.id,
                        user_full_name=user.full_name,
                        telegram_object="query",
                        content=f'informatics:{task_parsed_query}'
                    )

        # Проверяем, содержится ли значение переменной query.data в строке 'physics'
            if query.data.startswith('physics') or query.data.startswith('task:physics'):
                # Разбиваем данные запроса по ":"
                parsed_query = query.data.split(":")

                # Проверяем, не равна ли первая часть разобранного запроса "task"
                if not query.data.startswith('task:physics'):
                    # Добавляем запись в журнал в базу данных с общим содержанием 'physics'
                    await db.add_log(
                        chat_id=chat.id,
                        user_id=user.id,
                        user_full_name=user.full_name,
                        telegram_object="query",
                        content='physics'
                    )
                            
                else:
                    # Извлекаем информацию о задаче из разобранного запроса
                    task_parsed_query = parsed_query[2]
                    
                    # Добавляем запись в журнал в базу данных с извлеченной информацией о задаче
                    await db.add_log(
                        chat_id=chat.id,
                        user_id=user.id,
                        user_full_name=user.full_name,
                        telegram_object="query",
                        content=f'physics:{task_parsed_query}'
                    )


        return await handler(event, data)
