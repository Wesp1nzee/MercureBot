from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.inlain_admin import ikb_adm
from admin_filter import AdminFilter 
import psutil

router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart(), AdminFilter)
async def start_command(message: Message):

    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_total_gib = ram.total / (1024**3)
    ram_used_gib = ram.used / (1024**3)  

    performance_info = f"<code>CPU Usage: {cpu_usage}%\nRAM Total: {ram_total_gib:.3f} GiB\nRAM Used: {ram_used_gib:.3f} GiB</code>"

    await message.answer(
        f"""Привет, {message.chat.id}!\n\n Ты являешься админом!\n\nВот статистика по серверу:\n\n {performance_info}""",
        reply_markup= await ikb_adm.create_keyboard_menu_start()
    )
    