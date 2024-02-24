import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from lexicon.dict_task_number import container
from keyboards.main_menu import set_main_menu
from config import API_
from database.datacoonect import db
from database.cache import cache
from router.conect_hendlers_user import connect_client
from router.connect_hendlers_admin import connect_admin

loop = asyncio.get_event_loop()
logger = logging.getLogger(__name__)

async def main():
    #Создаем соеденение с БД
    await db.create_connection(loop)
    await container.create_container()
    cache.create_cache()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    
    bot = Bot(token=API_, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())

    connect_admin(dp)
    connect_client(dp)

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


