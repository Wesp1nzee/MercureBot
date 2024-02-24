from aiogram import Dispatcher

from .hendlers_admin import start_command_admin


def connect_admin(dp: Dispatcher):
    """Подключение admin routers"""
    dp.include_router(start_command_admin.router)
    