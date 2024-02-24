from typing import Union

from keyboards.inlain import ikb
from fsm import StateMachine
from callback_factory import FactoryTask

from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.enums import ParseMode 
from aiogram.utils.markdown import hide_link 
from aiogram.filters import Command


router = Router()
#Пользователь выбрал физику
@router.message(Command(commands="physics"))
@router.callback_query(F.data == "back_physics")
@router.callback_query(F.data == "physics:section", StateMachine.menu)
async def callbacks_profile(query_message: Union[CallbackQuery, Message], state: FSMContext):

    if isinstance(query_message, CallbackQuery):
        await query_message.message.edit_text(
            "Тут ты можешь выбрать конспект или задачи ОГЭ",    
            reply_markup = await ikb.create_keyboard_physics()
        )
        await query_message.answer()

    if isinstance(query_message, Message):
        await query_message.answer(
            "Тут ты можешь выбрать конспект или задачи ОГЭ",    
            reply_markup = await ikb.create_keyboard_physics()
        )
        await query_message.delete()
    
    await state.set_state(StateMachine.physics)


@router.callback_query(F.data.startswith('physics_theory'), StateMachine.physics)
async def callbacks_physics_themes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
            "Это все темы которые будт на ОГЭ 2024 году:",    
            reply_markup = await ikb.create_kb_themes_physics()
        )
    await callback.answer()
