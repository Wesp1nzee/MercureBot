import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.main_menu import set_main_menu
from config import API_
from database.datacoonect import db
from router.conect_hendlers import connect_client

loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)

async def main():
    #Создаем соеденение с БД
    await db.create_connection(loop)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    
    bot = Bot(token=API_, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())

    connect_client(dp)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


