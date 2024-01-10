import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import handler_menu, handler_oge, handler_physics, start_command
from keyboards.main_menu import set_main_menu
from TOKEN import API_


BOT_TOKEN = API_
logger = logging.getLogger(__name__)

async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    bot = Bot(token=API_, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(start_command.router, handler_menu.router, handler_physics.router, handler_oge.router)
    await set_main_menu(bot)
    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())