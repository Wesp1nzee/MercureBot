from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.inlain import ikb
from admin_filter import AdminFilter 


router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart(), AdminFilter)
async def start_command(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}!\n\n Ты являешься админом!",
        reply_markup= await ikb.create_keyboard_menu_start()
    )

    