import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from lexicon.dict_task_number_inf import container_inf
from lexicon.dict_task_number_phy import container_phy
from keyboards.main_menu import set_main_menu
from database.datacoonect import db
from config import Config, load_config

from router.conect_hendlers_user import connect_client
from router.connect_hendlers_admin import connect_admin
from logger_middlewares import LoggerMiddleware
from log import logger
from database.conteiner_fileid import container_fileid

loop = asyncio.get_event_loop()

async def main():
    config: Config = load_config()
    #Создаем соеденение с БД
    await db.create_connection(host=config.bd_bot.host,
                               port=config.bd_bot.port,
                               user=config.bd_bot.user,
                               password=config.bd_bot.password,
                               database=config.bd_bot.database,
                               loop=loop)
    await container_inf.create_container()
    await container_phy.create_container()
    await container_fileid.create_container_fileId()

    logger.info('Starting bot')
    
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    redis = Redis(host='localhost')
    dp = Dispatcher(storage = RedisStorage(redis=redis))

    await bot.send_message(chat_id=config.tg_bot.admin_ids, text="Бот запущен!")

    connect_admin(dp)
    connect_client(dp)
    dp.update.outer_middleware(LoggerMiddleware())

    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    


