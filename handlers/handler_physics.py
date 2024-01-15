from typing import Union

from keyboards.inlain import IKB
from handlers.db import users_db_condition
from lexicon.lexicon import generate_tasks_string

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.enums import ParseMode 
from aiogram.utils.markdown import hide_link 
from aiogram.filters import Command


router = Router()
#Пользователь выбрал физику
@router.message(Command(commands="physics"))
@router.callback_query(F.data == 'physics:section')
async def callbacks_profile(query_message: Union[CallbackQuery, Message]):
    if isinstance(query_message, CallbackQuery):
        users_db_condition[query_message.from_user.id].update({"section":"physics"})
        await query_message.message.edit_text(
            "Тут ты можешь выбрать конспект или задачи ОГЭ",    
            reply_markup = await IKB.create_keyboard_physics()
        )
        await query_message.answer()

    if isinstance(query_message, Message):
        users_db_condition[query_message.from_user.id].update({"section":"physics"})
        await query_message.answer(
            "Тут ты можешь выбрать конспект или задачи ОГЭ",    
            reply_markup = await IKB.create_keyboard_physics()
        )
        await query_message.delete()


@router.callback_query(F.data.startswith('physics_theory'))
async def callbacks_physics_themes(callback: CallbackQuery):
    await callback.message.edit_text(
            "Это все темы которые будт на ОГЭ 2024 году:",    
            reply_markup = await IKB.create_kb_themes_physics()
        )
    await callback.answer()
