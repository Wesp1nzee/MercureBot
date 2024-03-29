from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from keyboards.inlain_admin import ikb_adm
from admin_filter import AdminFilter 
import psutil
from database.datacoonect import db

router = Router()


@router.message(CommandStart(), AdminFilter)
async def start_command_admin(message: Message):

    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_total_gib = ram.total / (1024**3)
    ram_used_gib = ram.used / (1024**3)  

    performance_info = f"<code>CPU Usage: {cpu_usage}%\nRAM Total: {ram_total_gib:.3f} GiB\nRAM Used: {ram_used_gib:.3f} GiB</code>"

    await message.answer(
        f"""Привет, {message.from_user.id}!\n\nТы являешься админом!\n\nВот статистика по серверу:\n\n{performance_info}\nКол-во пользователей: {await db.count_user_for_admin()}""",
        reply_markup= await ikb_adm.create_keyboard_menu_start()
    )

@router.callback_query(F.data == "update", AdminFilter)
async def update_admin(callback: CallbackQuery):

    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_total_gib = ram.total / (1024**3)
    ram_used_gib = ram.used / (1024**3)  
    performance_info = f"<code>CPU Usage: {cpu_usage}%\nRAM Total: {ram_total_gib:.3f} GiB\nRAM Used: {ram_used_gib:.3f} GiB</code>"

    await callback.message.edit_text(
        f"""Привет, {callback.from_user.id}!\n\nТы являешься админом!\n\nВот статистика по серверу:\n\n{performance_info}\nКол-во пользователей: {await db.count_user_for_admin()}""",
        reply_markup= await ikb_adm.create_keyboard_menu_start()
    )
    