from aiogram import Router, exceptions
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent
from logs import logger

router = Router()


@router.error(ExceptionTypeFilter(exceptions.CallbackAnswerException))
async def error_handler1(event: ErrorEvent) -> None:
    logger.error(
        f"\n\taiogram ошибка: CallbackAnswerException - Исключение для ответа на обратный вызов"
        f"\n\tevent ошибка: {event.exception}"
        f"\n\n\tCallback: {event.update.callback_query}"
        f"\n\tUpdate: {event.update}\n"
    )


@router.error(ExceptionTypeFilter(exceptions.TelegramNotFound))
async def error_handler2(event: ErrorEvent) -> None:
    logger.error(
        f"\n\taiogram ошибка: TelegramNotFound - Чат / Пользователь / Сообщение не найдено"
        f"\n\tevent ошибка: {event.exception}"
        f"\n\n\tMessage: {event.update.message}"
        f"\n\tUpdate: {event.update}\n"
    )


@router.error(ExceptionTypeFilter(exceptions.TelegramRetryAfter))
async def error_handler3(event: ErrorEvent) -> None:
    logger.warning(
        f"\n\taiogram ошибка: TelegramRetryAfter - Слишком высокая интенсивность отправки сообщении, надо подождать - "
        f"{str(event.exception).split()[-7]} сек."
        f"\n\tevent ошибка: {event.exception}"
        f"\n\n\tMessage: {event.update.message}"
        f"\n\tUpdate: {event.update}\n"
    )


@router.error(ExceptionTypeFilter(exceptions.TelegramBadRequest))
async def error_handler4(event: ErrorEvent) -> None:
    logger.exception(
        f"\n\taiogram ошибка: TelegramBadRequest - Неверный запрос"
        f"\n\tevent ошибка: {event.exception}"
        f"\n\n\tMessage: {event.update.message}"
        f"\n\tUpdate: {event.update}\n"
    )


@router.error(ExceptionTypeFilter(exceptions.TelegramUnauthorizedError))
async def error_handler5(event: ErrorEvent) -> None:
    logger.exception(
        f"\n\taiogram ошибка: TelegramUnauthorizedError - Токен бота стал не действителен"
        f"\n\tevent ошибка: {event.exception}"
        f"\n\n\tUpdate: {event.update}\n"
    )


@router.error(ExceptionTypeFilter(exceptions.TelegramForbiddenError))
async def error_handler6(event: ErrorEvent) -> None:
    logger.exception(
        f"\n\taiogram ошибка: TelegramForbiddenError - Бота исключили из чата"
        f"\n\tevent ошибка: {event.exception}"
        f"\n\n\tUpdate: {event.update}\n"
    )


@router.error()
async def error_handler(event: ErrorEvent) -> None:
    logger.exception(
        f"\n\taiogram ошибка: Неизвестная ошибка"
        f"\n\tevent ошибка: {event.exception}"
        f"\n\n\tUpdate: {event.update}\n"
    )
