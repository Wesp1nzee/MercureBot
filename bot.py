import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import  handler_oge_physics, handler_physics, start_command, handler_menu, handler_informatics, hendler_oge_informatics
from keyboards.main_menu import set_main_menu
from TOKEN import API_


logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    
    bot = Bot(token=API_, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(start_command.router, handler_physics.router, handler_oge_physics.router, handler_informatics.router, hendler_oge_informatics.router)
    dp.include_routers(handler_menu.router)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())