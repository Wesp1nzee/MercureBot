from typing import Union

from keyboards.inlain_users import ikb
from fsm import StateMachine
from lexicon.lexicon import LEXICON_PHYSICS

from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest


router = Router()


@router.message(Command(commands="physics"))
@router.callback_query(F.data == "back_physics", StateMachine.theory_physics)
@router.callback_query(F.data == "back_physics", StateMachine.task_selection_physics)
@router.callback_query(F.data == "physics:section", StateMachine.menu)
async def callbacks_profile(query_message: Union[CallbackQuery, Message], state: FSMContext):

    if isinstance(query_message, CallbackQuery):
        await query_message.message.edit_text(
            text=LEXICON_PHYSICS["introduction"],    
            reply_markup = await ikb.create_keyboard_physics()
        )
        await query_message.answer()

    if isinstance(query_message, Message):
        await query_message.answer(
            text=LEXICON_PHYSICS["introduction"],      
            reply_markup = await ikb.create_keyboard_physics()
        )
        try:
            await query_message.delete()
            
        except TelegramBadRequest:
            pass
    
    await state.set_state(StateMachine.physics)


@router.callback_query(F.data.startswith('physics_theory'), StateMachine.physics)
async def callbacks_physics_themes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
            text=LEXICON_PHYSICS["theory"],
            reply_markup = await ikb.create_kb_themes_physics()
        )
    await callback.answer()
    await state.set_state(StateMachine.theory_physics)