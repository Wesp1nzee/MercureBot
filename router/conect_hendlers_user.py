from aiogram import Dispatcher

from .hendlers_user import handler_mistake_message, handler_oge_physics, handler_physics, start_command, handler_menu, handler_informatics, hendler_oge_informatics, handler_profil


def connect_client(dp: Dispatcher):
    """Подключение клиентских routers"""
    dp.include_router(handler_informatics.router)
    dp.include_router(handler_profil.router)
    dp.include_router(hendler_oge_informatics.router)
    dp.include_router(handler_oge_physics.router)
    dp.include_router(handler_physics.router)
    dp.include_router(start_command.router)
    dp.include_router(handler_mistake_message.router)
    dp.include_router(handler_menu.router)
    
    
