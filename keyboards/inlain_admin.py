from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class IKB_Admin:
    """Клавиатура для админов"""
    async def create_keyboard_menu_start(self):
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Статистика', callback_data='static'),
            ]
        ])
    
ikb_adm = IKB_Admin()