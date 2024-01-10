from keyboards.inlain import IKB
from dictionar.dictionaries import glavu, lesson_content_dict
from handlers.db import users_db_condition
from lexicon.lexicon import generate_tasks_string

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode 
from aiogram.utils.markdown import hide_link 
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()
#
@router.callback_query(F.data == 'physics:section')
async def callbacks_profile(callback: CallbackQuery ):
    await callback.message.edit_text(
        "Тут ты можешь выбрать конспект или задачи ОГЭ",    
        reply_markup = await IKB.create_keyboard_physics()
    )
    await callback.answer()

    
