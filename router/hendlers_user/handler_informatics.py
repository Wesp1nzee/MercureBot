from typing import Union

from keyboards.inlain_users import ikb
from lexicon.lexicon import LEXICON_INFORMATIC
from fsm import StateMachine

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


router = Router()


@router.message(Command(commands="informatics"))
@router.callback_query(F.data == "back_informatics", StateMachine.theory_informatics)
@router.callback_query(
    F.data == "back_informatics", StateMachine.task_selection_informatics
)
@router.callback_query(F.data == "informatics:section", StateMachine.menu)
async def informatics(query_message: Union[CallbackQuery, Message], state: FSMContext):

    if isinstance(query_message, CallbackQuery):
        await query_message.message.edit_text(
            text=LEXICON_INFORMATIC["introduction"],
            reply_markup=await ikb.create_kb_informatics(),
        )
        await query_message.answer()
    if isinstance(query_message, Message):
        await query_message.answer(
            text=LEXICON_INFORMATIC["introduction"],
            reply_markup=await ikb.create_kb_informatics(),
        )

        try:
            await query_message.delete()
        except TelegramBadRequest:
            pass
    await state.set_state(StateMachine.informatics)


@router.callback_query(F.data == "informatics_theory", StateMachine.informatics)
async def informatics_theory(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        text=LEXICON_INFORMATIC["theory"],
        reply_markup=await ikb.create_kb_informatics_url(),
    )

    await state.set_state(StateMachine.theory_informatics)
