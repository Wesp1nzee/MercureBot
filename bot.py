import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from lexicon.dict_task_number_inf import container_inf
from lexicon.dict_task_number_phy import container_phy
from keyboards.main_menu import set_main_menu
from config import API_, ADMIN_IDS
from database.datacoonect import db

from router.conect_hendlers_user import connect_client
from router.connect_hendlers_admin import connect_admin
from logger_middlewares import LoggerMiddleware
from logs import logger
from database.conteiner_fileid import container_fileid

loop = asyncio.get_event_loop()

async def main():
    #Создаем соеденение с БД
    await db.create_connection(loop)
    await container_inf.create_container()
    await container_phy.create_container()
    await container_fileid.create_container_inf()
    await container_fileid.create_container_phy()

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')
    
    bot = Bot(token=API_, parse_mode='HTML')
    redis = Redis(host='localhost')
    dp = Dispatcher(storage = RedisStorage(redis=redis))

    await bot.send_message(chat_id=ADMIN_IDS[0], text="Бот запущен!")

    connect_admin(dp)
    connect_client(dp)
    dp.update.outer_middleware(LoggerMiddleware())

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    


