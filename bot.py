from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from lexicon.dict_task_number import container_inf, container_phy
from keyboards.main_menu import set_main_menu
from config import Config, load_config

from router.conect_hendlers_user import connect_client
from router.connect_hendlers_admin import connect_admin
from middleware.logger_middlewares import LoggerMiddleware
from middleware.throttling_middleware import ThrottlingMiddleware

import logging
import sys

from aiohttp import web



WEB_SERVER_HOST = "127.0.0.1"
# Port for incoming request from reverse proxy. Should be any available port
WEB_SERVER_PORT = 8080
# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = "/webhook"
# Secret key to validate requests from Telegram (optional)
# Base URL for webhook will be used to generate webhook URL for Telegram,
# in this example it is used public DNS with HTTPS support
BASE_WEBHOOK_URL = "https://87ac-83-246-166-23.ngrok-free.app"

async def on_startup(bot: Bot) -> None:

    await container_inf.create_container()
    await container_phy.create_container()
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")


def main() -> None:
    config: Config = load_config()
    
    redis = Redis(host="localhost")
    dp = Dispatcher(storage=RedisStorage(redis=redis))

    connect_admin(dp)
    connect_client(dp)
    dp.update.outer_middleware(LoggerMiddleware())
    dp.update.outer_middleware(ThrottlingMiddleware())
    dp.startup.register(on_startup)

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Create aiohttp.web.Application instance
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
