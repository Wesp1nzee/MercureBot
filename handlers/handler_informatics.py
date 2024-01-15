from typing import Union
import logging

from keyboards.inlain import IKB
from handlers.db import users_db_condition
from lexicon.lexicon import LEXICON_INFORMATIC

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.enums import ParseMode 
from aiogram.utils.markdown import hide_link 
from aiogram.filters import Command

router = Router()
#Пользователь выбрал информатику
@router.message(Command(commands="informatics"))
@router.callback_query(F.data == 'informatics:section')
async def callbacks_profile(query_message: Union[CallbackQuery, Message]):
    if isinstance(query_message, CallbackQuery):
        users_db_condition[query_message.from_user.id].update({"section":"informatics"})
        await query_message.message.edit_text(
            "Тут ты можешь выбрать конспект или задачи ОГЭ",    
            reply_markup = await IKB.create_kb_informatics()
        )
        await query_message.answer()

    if isinstance(query_message, Message):
        users_db_condition[query_message.from_user.id].update({"section":"informatics"})
        await query_message.answer(
            "Тут ты можешь выбрать конспект или задачи ОГЭ",    
            reply_markup = await IKB.create_kb_informatics()
        )
        await query_message.delete()
    
@router.callback_query(F.data == 'informatics_theory')
async def callbacks_profile(callback: CallbackQuery):
    await callback.message.edit_text(
        f"{LEXICON_INFORMATIC['theory']}",
        reply_markup = await IKB.create_kb_informatics_url()
    )